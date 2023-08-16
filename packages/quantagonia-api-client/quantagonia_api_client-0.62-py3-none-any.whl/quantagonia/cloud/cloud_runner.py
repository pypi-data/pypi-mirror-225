from io import UnsupportedOperation
import sys, os
import asyncio
from time import sleep
from enum import Enum
from yaspin import yaspin
import uuid
from quantagonia.cloud.solver_log import SolverLog
from quantagonia.cloud.specs_https_client import SpecsHTTPSClient, JobStatus
from quantagonia.cloud.specs_enums import *
from quantagonia.runner import Runner
from quantagonia.enums import HybridSolverServers
from quantagonia.parser.log_parser import SolverLogParser
from quantagonia.parser.solution_parser import SolutionParser


class CloudRunner(Runner):
    """
    Runner subclass that provides functionality for submitting and solving QUBO and MIP instances to the cloud.
    The results are returned as dictionaries containing the keys 'solver_log', 'solution_file', and 'status'.

    Args:
        api_key (str): The API key string used to authenticate with the cloud.
        server (HybridSolverServers): (optional) The 'HybridSolverServers' to use for the hybrid solver service, defaults to the
            production server. Defaults to 'HybridSolverServers.PROD'.
        suppress_log (bool): (optional) Boolean indicating whether to suppress logging output from the runner, defaults to False.

    Attributes:
        https_client: The 'SpecsHTTPSClient' used for making requests to the hybrid solver service.
    """
    def __init__(self, api_key: str, server: HybridSolverServers = HybridSolverServers.PROD, suppress_log : bool = False):
        self.https_client = SpecsHTTPSClient(api_key=api_key, target_server=server)
        self.suppress_log = suppress_log
        self._error_symbol = "❌"

    def _solveParseArgs(self, batch_size : int, **kwargs):

        # default values
        poll_frequency: float = 1
        timeout: float = 14400
        new_incumbent_callback = None
        submit_callback = None

        # parse args
        if "poll_frequency" in kwargs:
            poll_frequency = kwargs["poll_frequency"]
        if "poll_frequency" in kwargs:
            timeout = kwargs["timeout"]
        if "new_incumbent_callback" in kwargs:
            new_incumbent_callback = kwargs["new_incumbent_callback"]
        if "submit_callback" in kwargs:
            submit_callback = kwargs["submit_callback"]

        solver_logs = [SolverLog() for ix in range(0, batch_size)]

        return poll_frequency, timeout, solver_logs, new_incumbent_callback, submit_callback

    def waitForJob(self, jobid: uuid, poll_frequency: float, timeout: float, solver_logs: list, batch_size : int, new_incumbent_callback = None) -> JobStatus:
        """
        Polls the status of a job identified by `jobid` until it reaches a final status or until the timeout is exceeded. The function updates the solver logs and calls the new incumbent callback function if a new incumbent is found in the batch item.

        Args:
            jobid: A UUID object that identifies the job to poll the status for.
            poll_frequency: The frequency (as float, in seconds) at which the function should poll for job status.
            timeout: The maximum amount of time (as float, in seconds) to wait for the job to finish before timing out.
            solver_logs: A list of `SolverLog` objects to update with the current log of the job.
            batch_size: The size of the batch for the job as an integer.
            new_incumbent_callback: (optional) A callback function to call if a new incumbent is found in the batch item. Defaults to None.

        Returns:
            JobStatus: A `JobStatus` enum value indicating whether the job has finished, terminated, or timed out.
        """
        printed_created = False
        printed_running = False
        spinner = yaspin()

        batch_num_incumbents = [0] * batch_size

        for t in range(0,int(timeout/poll_frequency)):

            sleep(poll_frequency)

            try:
                status = self.https_client.checkJob(jobid=jobid)
            except RuntimeError as runtime_e:
                sys.exit(f"{self._error_symbol} Unable to check job:\n\n{runtime_e}")

            if printed_running and not self.suppress_log:
                try:
                    logs = self.https_client.getCurrentLog(jobid=jobid)
                except RuntimeError as runtime_e:
                    sys.exit(f"{self._error_symbol} Unable to get log:\n\n{runtime_e}")

                for ix in range(0, batch_size):
                    solver_logs[ix].updateLog(logs[ix])

            # note: we do not give an error status to the job, but rather do
            # this on the batch item level (as part of getResults)
            if status == JobStatus.finished:
                return JobStatus.finished
            elif status == JobStatus.terminated:
                return JobStatus.terminated
            elif status == JobStatus.error:
                return JobStatus.error
            elif status == JobStatus.created:
                if not self.suppress_log:
                    if not printed_created:
                        printed_created = True
                        spinner.text = "Waiting for a free slot in the queue..."
                        spinner.start()
                        solver_logs[0].nextTimeAddNewLine()

            elif status == JobStatus.running:
                if not printed_running and not self.suppress_log:
                    printed_running = True
                    spinner.text = f"Job {jobid} unqueued, processing..."
                    spinner.ok("✔")
                    spinner.stop()
                    solver_logs[0].nextTimeAddNewLine()

                # check whether we got a new solution in any of the batch items
                if new_incumbent_callback is not None:
                    try:
                        batch_solutions = self.https_client.getCurrentSolution(jobid=jobid)
                    except RuntimeError as runtime_e:
                        sys.exit(f"{self._error_symbol}: " + str(runtime_e))

                    for ix in range(0, batch_size):
                        if int(batch_solutions[ix]["incumbents"]) > batch_num_incumbents[ix]:
                            new_incumbent_callback(ix, batch_solutions[ix]["objective"], batch_solutions[ix]["solution"])
                            batch_num_incumbents[ix] = int(batch_solutions[ix]["incumbents"])

        return JobStatus.timeout

    async def waitForJobAsync(self, jobid: uuid, poll_frequency: float, timeout: float, solver_logs: list, batch_size : int, new_incumbent_callback = None) -> JobStatus:
        """
        Asynchronously polls the status of a job identified by `jobid` until it reaches a final status or until the timeout is exceeded. The function updates the solver logs and calls the new incumbent callback function if a new incumbent is found in the batch item.

        Args:
            jobid: A UUID that identifies the job to poll the status for.
            poll_frequency: The frequency (as float, in seconds) at which the function should poll for job status.
            timeout: The maximum amount of time (as float, in seconds) to wait for the job to finish before timing out.
            solver_logs: A list of `SolverLog` objects to update with the current log of the job.
            batch_size: The size of the batch for the job as integer.
            new_incumbent_callback: (optional) A callback function to call if a new incumbent is found in the batch item. Defaults to None.

        Returns:
            JobStatus: A `JobStatus` enum value indicating whether the job has finished, terminated, or timed out.
        """

        printed_created = False
        printed_running = False
        spinner = yaspin()

        batch_num_incumbents = [0] * batch_size

        for t in range(0,int(timeout/poll_frequency)):

            await asyncio.sleep(poll_frequency)

            try:
                status = await self.https_client.checkJobAsync(jobid=jobid)
            except RuntimeError as runtime_e:
                sys.exit(f"{self._error_symbol} Unable to check job:\n\n{runtime_e}")

            if printed_running and not self.suppress_log:
                try:
                    logs = await self.https_client.getCurrentLogAsync(jobid=jobid)
                except RuntimeError as runtime_e:
                    sys.exit(f"{self._error_symbol}: " + str(runtime_e))
                for ix in range(0, batch_size):
                    solver_logs[ix].updateLog(logs[ix])

            if status == JobStatus.finished:
                return JobStatus.finished
            elif status == JobStatus.terminated:
                return JobStatus.terminated
            elif status == JobStatus.error:
                return JobStatus.error
            elif status == JobStatus.created:
                if not self.suppress_log:
                    if not printed_created:
                        printed_created = True
                        spinner.text = "Waiting for a free slot in the queue..."
                        spinner.start()
                        solver_logs[0].nextTimeAddNewLine()

            elif status == JobStatus.running:
                if not printed_running and not self.suppress_log:
                    printed_running = True
                    spinner.text = f"Job {jobid} unqueued, processing..."
                    spinner.ok("✔")
                    spinner.stop()
                    solver_logs[0].nextTimeAddNewLine()

                # check whether we got a new solution in any of the batch items
                if new_incumbent_callback is not None:
                    try:
                        batch_solutions = await self.https_client.getCurrentSolutionAsync(jobid=jobid)
                    except RuntimeError as runtime_e:
                        sys.exit(f"{self._error_symbol}: " + str(runtime_e))

                    for ix in range(0, batch_size):
                        if int(batch_solutions[ix]["incumbents"]) > batch_num_incumbents[ix]:
                            new_incumbent_callback(ix, batch_solutions[ix]["objective"], batch_solutions[ix]["solution"])
                            batch_num_incumbents[ix] = int(batch_solutions[ix]["incumbents"])

        return JobStatus.timeout

    def solve(self, problem_file: str, spec: dict, **kwargs):
        """
        Submits a QUBO or MIP instance to the cloud for solving.

        Args:
            problem_file (str): Path to problem file as string.
            spec (dict): A dictionary of solver options and parameters.

        Keyword arguments:
            submit_callback: (optional) Custom callback function that is called when a job is submitted. Defaults to None.
            poll_frequency (float): (optional) The frequency (as float, in seconds) at which the function should poll for job status. Defaults to 1.
            new_incumbent_callback: (optional) A callback function to call if a new incumbent is found in the batch item. Defaults to None.
            timeout (float): (optional) The maximum amount of time (as float, in seconds) to wait for the job to finish before timing out. Defaults to 14400.

        Returns:
            dict: Solver results as dictionary containing the keys 'solution_file', 'status', 'solver_log', 'sol_status', 'timing', 'objective', 'bound', 'absolute_gap', 'relative_gap', 'iterations', 'nodes', 'nodes_per_sec', 'best_node', 'best_time',	'num_quantum_solutions', 'solver_mix', and 'solution'.
        """
        res = self.solveBatched([problem_file], [spec], **kwargs)

        return res[0]

    ###
    # kwargs:
    # - submit_callback(jobid): called when job is submitted, receives jobid as parameter
    ###
    def solveBatched(self, problem_files: list, specs: list, **kwargs):
        """
        Submits a set of QUBO or MIP instances to the cloud for solving.

        Args:
            problem_files (List[str]): List of paths to problem files as string.
            specs (List[dict]): List of dictionaries of solver options and parameters.

        Keyword arguments:
            submit_callback: (optional) Custom callback function that is called when a job is submitted. Defaults to None.
            poll_frequency (float): (optional) The frequency (as float, in seconds) at which the function should poll for job status. Defaults to 1.
            new_incumbent_callback: (optional) A callback function to call if a new incumbent is found in the batch item. Defaults to None.
            timeout (float): (optional) The maximum amount of time (as float, in seconds) to wait for the job to finish before timing out. Defaults to 14400.

        Returns:
            List[Dict[str, Any]]: List of solver results. For each submitted instance it contains a dictionary with the keys 'solution_file','status', 'solver_log', 'sol_status', 'timing', 'objective', 'bound', 'absolute_gap', 'relative_gap', 'iterations', 'nodes', 'nodes_per_sec', 'best_node', 'best_time', 'num_quantum_solutions', 'solver_mix', and 'solution'.
        """
        batch_size = len(problem_files)
        poll_frequency, timeout, solver_logs, new_incumbent_callback, submit_callback = \
            self._solveParseArgs(batch_size, **kwargs)

        if not self.suppress_log:
            spinner = yaspin()
            spinner.start()
            spinner.text = "Submitting job to the Quantagonia cloud..."
            spinner.start()
        try:
            jobid = self.https_client.submitJob(problem_files=problem_files, specs=specs)
            if("submit_callback" in kwargs):
                kwargs["submit_callback"](jobid)
        except RuntimeError as runtime_e:
            if not self.suppress_log:
                spinner.text = "Cannot submit job"
                spinner.ok(self._error_symbol)
                spinner.stop()
            sys.exit(str(runtime_e))

        if not self.suppress_log:
            spinner.text = f"Queued job with jobid: {jobid} for execution in the Quantagonia cloud..."
            spinner.ok("✔")
            spinner.stop()

        status: JobStatus = self.waitForJob(jobid=jobid, poll_frequency=poll_frequency, timeout=timeout,
            solver_logs=solver_logs, batch_size=batch_size, new_incumbent_callback=new_incumbent_callback)

        if status is not JobStatus.finished:
            raise Exception(f"Job with jobid {jobid} error. Status of the job: {status}")
        else:
            if not self.suppress_log:
                print(f"Finished processing job {jobid}...")

        try:
            res = self.https_client.getResults(jobid=jobid)
        except RuntimeError as runtime_e:
            sys.exit(f"{self._error_symbol}: " + str(runtime_e))

        if not self.suppress_log:
            for ix in range(0, batch_size):
                solver_logs[ix].updateLog(res[ix]['solver_log'])

        # parse solver logs and add solution
        for ix in range(0, batch_size):
            # parse and add solve stats
            logparser = SolverLogParser(res[ix]["solver_log"])
            res[ix].update(logparser.get_all())
            # add solution
            res[ix]["solution"] = SolutionParser.parse(res[ix]["solution_file"])

        return res

    async def solveAsync(self, problem_file: str, spec: dict, **kwargs):
        """
        Asynchonously submits a QUBO or MIP instance to the cloud for solving.

        Args:
            problem_file (str): Path to problem file as string.
            spec (dict): A dictionary of solver options and parameters.

        Keyword arguments:
            submit_callback: (optional) Custom callback function that is called when a job is submitted. Defaults to None.
            poll_frequency (float): (optional) The frequency (as float, in seconds) at which the function should poll for job status. Defaults to 1.
            new_incumbent_callback: (optional) A callback function to call if a new incumbent is found in the batch item. Defaults to None.
            timeout (float): (optional) The maximum amount of time (as float, in seconds) to wait for the job to finish before timing out. Defaults to 14400.

        Returns:
            dict: Solver results as dictionary containing the keys 'solution_file','status', 'solver_log', 'sol_status', 'timing', 'objective', 'bound', 'absolute_gap', 'relative_gap', 'iterations', 'nodes', 'nodes_per_sec', 'best_node', 'best_time', 'num_quantum_solutions', 'solver_mix', and 'solution'.
        """
        res = await self.solveBatchedAsync([problem_file], [spec], **kwargs)
        return res[0]

    async def solveBatchedAsync(self, problem_files: list, specs: list, **kwargs):
        """
        Asynchronously submits a set of QUBO or MIP instances to the cloud for solving.

        Args:
            problem_files (List[str]): List of paths to problem files as string.
            specs (List[dict]): List of dictionaries of solver options and parameters.

        Keyword arguments:
            submit_callback: (optional) Custom callback function that is called when a job is submitted. Defaults to None.
            poll_frequency (float): (optional) The frequency (as float, in seconds) at which the function should poll for job status. Defaults to 1.
            new_incumbent_callback: (optional) A callback function to call if a new incumbent is found in the batch item. Defaults to None.
            timeout (float): (optional) The maximum amount of time (as float, in seconds) to wait for the job to finish before timing out. Defaults to 14400.

        Returns:
            List[Dict[str, Any]]: List of solver results. For each submitted instance it contains a dictionary containing the keys 'solution_file','status', 'solver_log', 'sol_status', 'timing', 'objective', 'bound', 'absolute_gap', 'relative_gap', 'iterations', 'nodes', 'nodes_per_sec', 'best_node', 'best_time', 'num_quantum_solutions', 'solver_mix', and 'solution'.
        """
        batch_size = len(problem_files)
        poll_frequency, timeout, solver_logs, new_incumbent_callback, submit_callback = \
            self._solveParseArgs(batch_size, **kwargs)

        if not self.suppress_log:
            spinner = yaspin()
            spinner.start()
            spinner.text = "Submitting job to the Quantagonia cloud..."
            spinner.start()
        try:
            jobid = await self.https_client.submitJobAsync(problem_files=problem_files, specs=specs)
        except RuntimeError as runtime_e:
            if not self.suppress_log:
                spinner.text = "Cannot submit job"
                spinner.ok(self._error_symbol)
                spinner.stop()
            sys.exit(str(runtime_e))

        if not self.suppress_log:
            spinner.text = f"Queued job with jobid: {jobid} for execution in the Quantagonia cloud..."
            spinner.ok("✔")
            spinner.stop()

        status: JobStatus = await self.waitForJobAsync(jobid=jobid, poll_frequency=poll_frequency, timeout=timeout,
            solver_logs=solver_logs, batch_size=batch_size, new_incumbent_callback=new_incumbent_callback)

        if status is not JobStatus.finished:
            raise Exception(f"Job with jobid {jobid} error. Status of the job: {status}")
        else:
            if not self.suppress_log:
                print(f"Finished processing job {jobid}...")

        try:
            res = self.https_client.getResults(jobid=jobid)
        except RuntimeError as runtime_e:
            sys.exit(f"{self._error_symbol}: " + str(runtime_e))
        if not self.suppress_log:
            for ix in range(0, batch_size):
                solver_logs[ix].updateLog(res[ix]['solver_log'])

        for ix in range(0, batch_size):
            # parse and add solve stats
            logparser = SolverLogParser(res[ix]["solver_log"])
            res[ix].update(logparser.get_all())
            # add solution
            res[ix]["solution"] = SolutionParser.parse(res[ix]["solution_file"])

        return res


    def interrupt_job(self, jobid: uuid):
        """
        Sends an interrupt signal to stop the execution of the specified job.

        Args:
            jobid (uuid): The UUID of the job to be interrupted.

        Returns:
            dict: A dictionary containing the response from the server.
        """
        resp = self.https_client.interrupt_job(jobid)
        return resp

    async def interrupt_job_async(self, jobid:uuid):
        """
        Asynchronously sends an interrupt signal to stop the execution of a submitted job.

        Args:
            jobid (uuid): The UUID of the job to be interrupted.

        Returns:
            dict: A dictionary containing the response from the server.
        """
        resp = await self.https_client.interruptJobAsync(jobid)
        return resp
