from .hybrid_solver_api import QQVM_CMD

from quantagonia.runner import Runner
from quantagonia.runner_factory import HybridSolverConnectionType, RunnerFactory
from quantagonia.enums import HybridSolverServers

class QPuLPAdapter:
  """
  This class provides an adapter for solving optimization problems created using the PuLP modeling language as MIP.
  """

  @classmethod
  def getSolver(cls,
                connection : HybridSolverConnectionType,
                api_key : str = None,
                server : HybridSolverServers = HybridSolverServers.PROD,
                spec_dict : dict = None,
                keep_files : bool = False):
    """
    Returns a solver object for problem instances created with Pulp.

    The solver can submit a problem to the cloud and solved as MIP.

    Args:
        connection: Connection type. It is recommended to use `HybridSolverConnectionType.CLOUD`.
        api_key (optional): The Quantagonia API key used for the connection. Defaults to None.
        server (optional): The server used for the connection. It is recommended to use the default value: `HybridSolverServers.PROD`.
        spec_dict (optional): A solver specifications dictionary. Defaults to None.
        keep_files (optional): Whether to keep the generated input and output files. Defaults to False.

    Returns:
        A solver instance.
    """
    runner : Runner = RunnerFactory.getRunner(connection, api_key, server)
    solver = QQVM_CMD(runner=runner, spec_dict=spec_dict, keepFiles=keep_files)

    return solver
