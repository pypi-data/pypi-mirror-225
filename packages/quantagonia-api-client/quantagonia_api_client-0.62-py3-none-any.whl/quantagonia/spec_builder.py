import os
import json
from enum import Enum
from abc import ABC
from typing import Dict
import warnings
from .enums import PriorityEnum

# set up warnings
def plain_warning(message, category, filename, lineno, line=None):
    return '%s: %s\n' % (category.__name__, message)

warnings.formatwarning = plain_warning


THIS_SCRIPT = os.path.dirname(os.path.abspath(__file__))

class ProblemType(Enum):
    MIP = 0
    QUBO = 1

class QuboSolverType(Enum):
    """This class is deprecated and to be removed soon."""
    COOK = 0
    METROPOLIS_HASTINGS = 1
    FVSDP = 2
    THROW_DICE = 3
    THROW_DICE_SDP_ROOT = 4
    THROW_DICE_SDP_ALL = 5
    THROW_DICE_SDP_ALL_NEWTON = 6
    NO_SOLVER_SDP_ALL = 7


class SpecBuilder(ABC):
    """
    Abstract spec builder base class for :class:`MIPSpecBuilder` and :class:`QUBOSpecBuilder`.
    """

    def __init__(self):
        self.spec = {"solver_config" : {}}

    def gets(self) -> str:
        return json.dumps(self.spec)

    def getd(self) -> Dict:
        """
        Returns currently set solver options as dictionary.

        Returns:
            dict: Dictionary containing solver options.
        """
        return self.spec

    def set_option(self, option: str, value) -> None:
        """
        Sets specified option to specified value.

        Arguments:
            option (str): Name of option.
            value (Any): value of option.

        Returns:
            None
        """
        self.spec["solver_config"][option] = value

    def set_time_limit(self, time_limit: float):
        """
        Sets time limit.

        We can set a time limit to interupt the solver after the given time and return the best found solution along with the optimality gap.
        The optimality gap tells you how much more potential there could be in the optimization process.

        Note that with ordinary quantum annealers you only retrieve a solution without knowing how far it might be away from an optimal solution.

        Returns:
            None

        Example::

            time_limit = 10 # seconds
            spec.set_time_limit(time_limit)
        """
        check_type("time_limit", time_limit, (float, int), type_name="numeric")
        check_numeric_value("time_limit", time_limit, lb=0)
        self.set_option("time_limit", time_limit)

    def set_priority(self, priority: PriorityEnum = PriorityEnum["MEDIUM"]):
        """
        Sets the queuing priority of the job.

        We can use this option to specify the priority of the job.
        Jobs with this option set to "LOW" give priority to "MEDIUM" which give priority to "HIGH".

        Arguments:
            priority (PriorityEnum): Enum specifying the priority.

        Returns:
            None
        """
        check_type("priority", priority, PriorityEnum)
        try:
            self.spec["processing"]["priority"] = priority
        except KeyError as e:
            self.spec["processing"] = {}
            self.spec["processing"]["priority"] = priority

    def set_exclusivity(self, exclusive: bool = False):
        """
        Sets the exclusivity of the job.

        If set to true, job is run in an exclusive and isolated environment.

        Arguments:
            exclusive (bool): Enables or disables exclusivity.

        Returns:
            None
        """
        check_type("exclusivity", exclusive, bool)
        try:
            self.spec["processing"]["exclusive"] = exclusive
        except KeyError as e:
            self.spec["processing"] = {}
            self.spec["processing"]["exclusive"] = exclusive


class MIPSpecBuilder(SpecBuilder):
    """A class for building Mixed Integer Programming (MIP) problem specifications.

        This class extends the `SpecBuilder` base class and sets the `problem_type` option to "MIP".

    """
    def __init__(self):
        """Initializes the MIPSpecBuilder object and sets the `problem_type` option to "MIP"."""
        super().__init__()
        self.spec["problem_type"] = "MIP"

    def set_heuristics(self, heuristics: float):
        """
        Sets the `mip_heuristic_effort` option to a float in range of [0, 1].

        The variable controls the percentage of time used on heuristics.

        Args:
            heuristics (float): A float.

        Returns:
            None.

        Raises:
            TypeError: If the `heuristics` argument is not a float.
            ValueError: If the `heuristics` argument is not within the valid range of [0, 1].

        """
        check_type("heuristics", heuristics, float)
        check_numeric_value("heuristics", heuristics, lb=0, ub=1)
        self.set_option("mip_heuristic_effort", heuristics)

class QUBOSpecBuilder(SpecBuilder):
    """
    A class for building Quadratic Unconstrained Binary Optimization (QUBO) problem specifications.

    This class extends the `SpecBuilder` base class and sets the `problem_type` option to "QUBO".

    """
    def __init__(self, type = None, spec_path = os.path.join(THIS_SCRIPT, "default_spec.json")):
        """
        Initializes a QUBO problem specification builder instance.

        This class extends the :class:`SpecBuilder` base class and sets the :code:`problem_type` option to "QUBO".

        Args:
            type (str): Deprecated and ignored. This argument is retained for backwards compatibility only.
            spec_path (str): Path to a specs JSON file. A default specs file will be used if argument is not provided.

        Returns:
            None.
        """
        super().__init__()
        self.spec["problem_type"] = "QUBO"

        if type:
            warnings.warn("Setting a specific QuboSolverType is deprecated and ignored. Instead, a default spec is loaded. Please do all modifications via the dedicated methods of the SpecBuilder.")

        # always read default spec
        with open(spec_path) as jsonf:
            self.spec["solver_config"] = json.load(jsonf)

    # general settings
    ###################################################################################
    def set_sense(self, sense: str):
        warnings.warn("Setting the sense via the spec is deprecated and ignored! " +\
                      "Set the sense in the .qubo file or via QuboModel.sense().")

    # termination settings
    ###################################################################################
    def set_max_num_nodes(self, max_num_nodes: int):
        """Limit the number of branch and bound nodes to be explored.

        Setting this number to 1 only solves the root node.
        This mimicks the behavior of ordinary (quantum) annealers which "only" return a solution without any quality assessment or proof of global optimality.
        When comparing to other quantum annealers, make sure to limit the number of nodes to 1.
        If the solution process is stopped after the maximum number of nodes is reached, our solver still returns an optimality gap which tells you how far away the true optimal solution potentially is.
        This is not the case with other ordinary (quantum) annealers.

        Args:
            max_num_nodes (int): An integer representing the maximum number of branch-and-bound nodes allowed. Should be greater than or equal to 1.

        Returns:
            None.

        Example::

            num_nodes = 1
            spec.set_max_num_nodes(num_nodes)
        """
        check_type("max_num_nodes", max_num_nodes, int)
        check_numeric_value("max_num_nodes", max_num_nodes, lb=1)
        self.set_option("max_num_nodes", max_num_nodes)

    def set_heuristics_only(self, heuristics_only: bool):
        """
        Only apply the root node primal heuristics and then terminate.

        This waits until *all* primal heuristics are finished and displays a table with
        objective value and runtime per heuristic.

        Args:
            heuristics_only (bool): Flag to enable or disable heuristics_only mode.
        Returns:
            None
        """
        check_type("heuristics_only", heuristics_only, bool)
        self.set_option("heuristics_only", heuristics_only)


    def set_absolute_gap(self, abs_gap: float):
        """
        Set the absolute gap for termination.

        Normally the solver terminates once the absolute gap reaches a default tolerance of 1e-9.
        The absolute gap is the difference between the objective value :math:`f∗` of the best solution found and the best bound :math:`fˉ​` on the objective value.
        Hence, the absolute gap tells you how much more the objective value could potentially increase if you continue the search.

        Args:
            abs_gap (float): A float representing the absolute gap for termination.

        Returns:
            None.

        Raises:
            ValueError: If :code:`abs_gap` is not a float or integer.

        Example::

            abs_gap = 1e-6
            spec.set_absolute_gap(abs_gap)
        """
        check_type("absolute_gap", abs_gap, (float, int), type_name="numeric")
        self.set_option("absolute_gap", abs_gap)

    def set_relative_gap(self, rel_gap: float):
        r"""
        Set the relative gap for termination.

        The solver terminates once the relative gap reaches the default tolerance of 0.01% or 1e-4.
        The relative gap is defined as :math:`|f^\ast - \bar{f}|\, /\,  |f^\ast|`,
        i.e., it is the improvement potential relative to the best-known objective value.


        Args:
            rel_gap (float): A float representing the relative gap for termination.

        Returns:
            None.

        Raises:
            ValueError: If :code:`rel_gap` is not a float or integer.

        Example::

            rel_gap = 1e-2
            spec.set_relative_gap(rel_gap)
        """
        check_type("relative_gap", rel_gap, (float, int), type_name="numeric")
        self.set_option("relative_gap", rel_gap)

    def set_objective_cutoff(self, cutoff_value: float):
        """
        Set a cutoff value for the objective.
        If incumbent reaches cutoff value, the solver terminates

        Args:
            cutoff_value (float): A float representing the cutoff value for the objective.

        Returns:
            None.

        Raises:
            ValueError: If :code:`cutoff_value` is not a float or integer.
        """
        check_type("objective_cutoff", cutoff_value, (float, int), type_name="numeric")
        self.set_option("primal_cutoff_value", cutoff_value)

    # presolve settings
    ###################################################################################
    def set_presolve(self, presolve: bool):
        """
        Enable or disable presolve.

        Args:
            presolve (bool): A boolean indicating whether to enable or disable presolve.

        Returns:
            None.

        Raises:
            ValueError: If :code:`presolve` is not a boolean.

        Example::

            spec.set_presolve(False)
        """
        check_type("presolve", presolve, bool)
        self.spec["solver_config"]["presolve"]["enabled"] = presolve

    def set_node_presolve(self, node_presolve: bool):
        """
        Enable or disable node presolve.

        Similar to the presolve on the full QUBO problem, our solver also performs some presolve routines for each sub-QUBO derived during the solution process.
        This behavior can be turned off.
        Args:
            node_presolve (bool): A boolean indicating whether to enable or disable node presolve.

        Returns:
            None.

        Raises:
            ValueError: If :code:`node_presolve` is not a boolean.

        Example::

            spec.set_node_presolve(False)
        """
        check_type("node_presolve", node_presolve, bool)
        self.set_option("node_presolve", node_presolve)

    def set_decomposition(self, decomposition: True):
        """
        Enable or disable decomposition of the QUBO matrix.

        Args:
            decomposition (bool): A boolean indicating whether to enable or disable decomposition of the QUBO matrix. The default value is True.

        Returns:
            None.

        Raises:
            ValueError: If :code:`decomposition` is not a boolean.
        """
        check_type("decomposition", decomposition, bool)
        self.spec["solver_config"]["presolve"]["decompose"] = decomposition

    # search strategy settings
    ###################################################################################
    def set_enumeration(self, enumeration: bool):
        """
        Enable or disable enumeration.

        During the solution process, our solver solves many smaller sub-QUBOs.
        If these sub-QUBOs are small enough, we explicitly enumerate the solution space of the sub-QUBO, because this can be done extremely fast for small sub-QUBOs.
        This behavior may be turned off.

        Args:
            enumeration (bool): A boolean indicating whether to enable or disable enumeration.

        Returns:
            None.

        Raises:
            ValueError: If :code:`enumeration` is not a boolean.

        Example::

            spec.set_enumeration(False)
        """

        check_type("enumeration", enumeration, bool)
        self.spec["solver_config"]["enumerate"]["enabled"] = enumeration

    def add_quantum_heuristic(self, heuristic):
        if "root_node_quantum_heuristics" not in self.spec["solver_config"]:
            self.spec["solver_config"]["root_node_quantum_heuristics"] = []
        self.spec["solver_config"]["root_node_quantum_heuristics"].append(heuristic)

def check_type(option_name, option_value, type, type_name=None):

    if not isinstance(option_value, type):
        if type_name is None:
            type_name = type.__name__
        raise ValueError(f"Value for {option_name} is set to {option_value} but must be a {type_name}.")

def check_numeric_value(option_name, option_value, lb=None, ub=None):
    if lb is not None and option_value < lb:
        raise ValueError(f"Value for {option_name} must be >= {lb}")
    if ub is not None and option_value > ub:
        raise ValueError(f"Value for {option_name} must be <= {ub}")
