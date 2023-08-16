from quantagonia.enums import *
from quantagonia.qubo import *
from typing import List
import pulp
import copy

# PyQUBO
import pyqubo as pq

# D-Wave
from dimod import BinaryQuadraticModel, ConstrainedQuadraticModel
from dimod.vartypes import Vartype

# Qiskit
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.problems import *
from qiskit_optimization.problems.constraint import *
from qiskit_optimization.problems.quadratic_objective import ObjSense

###
# Base class
###

class QUBOAdapter:

  def __init__(self):
    self._original_vars = {}

  def getSolutionAsSample(self, qubo : QuboModel):
    sample = {}

    for _, v in qubo.vars.items():
      if v.name in self._original_vars:
        sample[v.name] = v.assignment

    return sample

###
# D-Wave QUBO adapter
#
# Note: D-Wave only allows minimization, so we follow their convention and
# minimize the resulting QUBOs as well
###

# treats the D-Wave BQM as {0, 1}-valued QUBO
class DWaveBQMAdapter(QUBOAdapter):
  """
  Adapter for converting a D-Wave :class:`dimod.BinaryQuadraticModel` (BQM) to a Quantagonia :class:`QuboModel`.

  Note:
      D-Wave only allows minimization, so we also set the sense to minimization in the QUBOs obtained from the conversion process.
  """

  def __init__(self):
    super().__init__()

  def convert(self, bqm : BinaryQuadraticModel) -> QuboModel:
    """
    Converts a D-Wave BQM to a :class:`QuboModel`.

    Args:
        bqm (:class:`dimod.BinaryQuadraticModel`) : The :class:`dimod.BinaryQuadraticModel` to be converted.

    Returns:
        QuboModel: The resulting :class:`QuboModel`.
    """
    self._original_vars = copy.copy(bqm.variables)

    qubo = QuboModel(HybridSolverOptSenses.MINIMIZE)

    # create variables
    for var_name in bqm.variables:
      qubo.addVariable(var_name)

    # add shift
    qubo.objective += bqm.offset

    # create linear terms
    for var, coeff in bqm.linear.items():
      qubo.objective += coeff * qubo.vars[var]

    # create quadratic terms
    for var_tpl, coeff in bqm.quadratic.items():
      qubo.objective += coeff * qubo.vars[var_tpl[0]] * qubo.vars[var_tpl[1]]

    return qubo

class DWaveCQMAdapter(QUBOAdapter):
  """
  Adapts a D-Wave :class:`dimod.ConstrainedQuadraticModel` to a Quantagonia :class:`QuboModel`.

  Args:
      penalty (float): The penalty parameter to use for the QUBO conversion.

  Note:
      D-Wave only allows minimization, so we also set the sense to minimization in the QUBOs obtained from the conversion process.
  """
  def __init__(self, penalty = 1e3):
    """
    Initializes a new instance of the :class:`DWaveCQMAdapter` class.

    Args:
        penalty (float): The penalty parameter to use for the QUBO conversion.
    """
    super().__init__()

    self.penalty = penalty

  def convert(self, cqm : ConstrainedQuadraticModel) -> QuboModel:
    """
    Converts a D-Wave CQM to a :class:`QuboModel`.

    Args:
        cqm (:class:`dimod.ConstrainedQuadraticModel`): A :class:`dimod.ConstrainedQuadraticModel` to be converted.

    Returns:
        QuboModel: The resulting :class:`QuboModel`.

    Raises:
        Exception: If the variables are non-binary or the constraints are non-linear.
    """
    self.checkCQMSupported(cqm)

    self._original_vars = copy.copy(cqm.variables)

    qubo = self.convertLinearConstraints(cqm)
    qubo = self.convertObjective(cqm, qubo)

    return qubo

  def checkCQMSupported(self, cqm : ConstrainedQuadraticModel):
    """
    Checks if the input CQM is supported by the converter.

    Args:
        cqm (:class:`dimod.ConstrainedQuadraticModel`) : The CQM to be checked.

    Returns:
        None.

    Raises:
        Exception: If the CQM has unsupported variables or constraints.
    """
    # check that all variables are binary
    for var in cqm.variables:
      if cqm.vartype(var) != Vartype.BINARY:
        raise Exception("Only binary variables are supported.")

    # check that all constraints are linear
    for _, constraint in cqm.constraints.items():
      if len(constraint.lhs.quadratic) > 0:
        raise Exception("Only linear constraints are supported.")

  def convertObjective(self, cqm : ConstrainedQuadraticModel, qubo : QuboModel):
    """
    Creates a :class:`QuboModel` from the objective function of a CQM.

    Args:
        cqm (:class:`dimod.ConstrainedQuadraticModel`): A CQM containing the objective function.
        qubo (QuboModel): A :class:`QuboModel` to add the objective function to.

    Returns:
        QuboModel: The QuboModel obtained by adding the converted objective function of the given CQM.
    """
    # add shift
    qubo.objective += cqm.objective.offset

    # linear terms
    for var_name, var_coeff in cqm.objective.linear.items():
      qubo.objective += var_coeff * qubo.vars[var_name]

    # quadratic terms
    for var_tpl, var_coeff in cqm.objective.quadratic.items():
      qubo.objective += var_coeff * qubo.vars[var_tpl[0]] * qubo.vars[var_tpl[1]]

    return qubo

  def convertLinearConstraints(self, cqm : ConstrainedQuadraticModel):
    """
    Converts the linear constraints of a CQM into a QuboModel.

    Args:
        cqm (:class:`dimod.ConstrainedQuadraticModel`): The CQM to be converted.

    Returns:
        :class:`QuboModel`: A :class:`QuboModel` representing the linear constraints of the CQM.

    Raises:
        Exception: If the variables of the CQM are non-binary or the constraints are not linear.
    """
    # create variables in PuLP format
    pulp_vars = {name : pulp.LpVariable(name, lowBound = 0, upBound = 1, cat = pulp.LpBinary) for name in cqm.variables}

    # create a MIP problem for the linear constraints
    mip = MIPIntermediate(pulp.LpMinimize, mip_vars = pulp_vars)
    mip.vars = copy.deepcopy(mip.mip_vars)

    for label, constraint in cqm.constraints.items():

      sense = pulp.const.LpConstraintEQ
      if constraint.sense.value == ">=":
        sense = pulp.const.LpConstraintGE
      elif constraint.sense.value == "<=":
        sense = pulp.const.LpConstraintLE

      mip_cons = MIPConstraint(label, {}, sense, constraint.rhs)

      for var_name, var_coeff in constraint.lhs.linear.items():
        mip_cons.coefficients[var_name] = var_coeff

      mip.constraints.append(mip_cons)

    # convert from IP to QUBO with a fixed penalty
    i2q = IP2Qubo(sense = HybridSolverOptSenses.MINIMIZE)

    # return QUBO (variables are the same as they were binary)
    i2q.fromIP(mip, mip_format = MIPSourceFormat.MIP_INTERMEDIATE)
    mdl = i2q.toQUBO(self.penalty)

    return mdl

###
# IBM / Qiskit QUBO adapter
#
# Note: Qiskit QP contains its sense (as opposed to D-Wave), hence we use
# that
###
class QiskitQPAdapter(QUBOAdapter):
  """
  Adapter to convert an IBM / Qiskit :class:`qiskit_optimization.QuadraticProgram` into a Quantagonia :class:`QuboModel`.
  """

  def __init__(self, penalty = 1e3):
    """
    Initializes a new instance of the :class:`QiskitQPAdapter` class.

    Args:
        penalty (float): The penalty as float, to use when converting linear constraints to QUBO. Defaults to 1e3.
    """
    super().__init__()

    self.penalty = penalty

  def convert(self, qp : QuadraticProgram) -> QuboModel:
    """
    Converts the given :class:`qiskit_optimization.QuadraticProgram` to a :class:`QuboModel`.

    Args:
        qp ( :class:`qiskit_optimization.QuadraticProgram`) : The :class:`qiskit_optimization.QuadraticProgram` to convert.

    Returns:
        QuboModel: The converted QUBO as :class:`QuboModel`.

    Raises:
        Exception: If the :class:`qiskit_optimization.QuadraticProgram` contains non-binary variables, or non-linear constraints.
    """
    self.checkQPSupported(qp)
    self.sense = qp.objective.sense

    self._original_vars = [var.name for var in qp.variables]

    qubo = self.convertLinearConstraints(qp)
    qubo = self.convertObjective(qp, qubo)

    return qubo

  def checkQPSupported(self, qp : QuadraticProgram):
    """
    Checks if the :class:`qiskit_optimization.QuadraticProgram` is supported by the converter. Allowed are binary variables and linear constraints.


    Args:
        qp ( :class:`qiskit_optimization.QuadraticProgram`) : The :class:`qiskit_optimization.QuadraticProgram` to check.

    Raises:
        Exception: If the :class:`qiskit_optimization.QuadraticProgram` contains non-binary variables, or non-linear constraints.
    """
    if qp.get_num_integer_vars() > 0:
      raise Exception("Only problems without integer variables are supported.")

    if qp.get_num_continuous_vars() > 0:
      raise Exception("Only problems without continuous variables are supported.")

    if qp.get_num_quadratic_constraints() > 0:
      raise Exception("Only problems without quadratic constraints are supported.")

  def convertObjective(self, qp : QuadraticProgram, qubo : QuboModel):
    """
    Converts the objective function of the given Qiskit :class:`qiskit_optimization.QuadraticProgram` to a :class:`QuboModel`.

    Args:
        qp (:class:`qiskit_optimization.QuadraticProgram`): The :class:`qiskit_optimization.QuadraticProgram` to convert.
        qubo (:class:`QuboModel`): The :class:`QuboModel` to convert the objective function to.

    Returns:
        QuboModel: The :class:`QuboModel` with the objective function corresponding to the :class:`qiskit_optimization.QuadraticProgram`.
    """
    # linear terms
    for var_name, var_coeff in qp.objective.linear.to_dict(use_name=True).items():
      qubo.objective += var_coeff * qubo.vars[var_name]

    # quadratic terms
    for var_tpl, var_coeff in qp.objective.quadratic.to_dict(use_name=True).items():
      qubo.objective += var_coeff * qubo.vars[var_tpl[0]] * qubo.vars[var_tpl[1]]

    return qubo

  def convertLinearConstraints(self, qp : QuadraticProgram):
    """
    Converts the linear constraints of the given Qiskit :class:`qiskit_optimization.QuadraticProgram` to a QUBO problem.

    Args:
        qp (:class:`qiskit_optimization.QuadraticProgram`) : The Qiskit QuadraticProgram to convert.

    Returns:
        QuboModel: The :class:`QuboModel` that corresponds to the given :class:`qiskit_optimization.QuadraticProgram`.
    """
    # create variables in PuLP format
    pulp_vars = {var.name : pulp.LpVariable(var.name, lowBound = 0, upBound = 1, cat = pulp.LpBinary) for var in qp.variables}

    # create a MIP problem for the linear constraints
    mip = MIPIntermediate(sense = pulp.LpMinimize if self.sense == ObjSense.MINIMIZE
      else pulp.LpMaximize, mip_vars = pulp_vars)
    mip.vars = copy.deepcopy(mip.mip_vars)

    for ix, lc in enumerate(qp.linear_constraints):

      sense = pulp.const.LpConstraintEQ
      if lc.sense == ConstraintSense.GE:
        sense = pulp.const.LpConstraintGE
      elif lc.sense == ConstraintSense.LE:
        sense = pulp.const.LpConstraintLE

      mip_cons = MIPConstraint(lc.name, {}, sense, lc.rhs)

      for var_name, var_coeff in lc.linear.to_dict(use_name=True).items():
        mip_cons.coefficients[var_name] = var_coeff

      mip.constraints.append(mip_cons)

    # convert from IP to QUBO with a fixed penalty
    i2q = IP2Qubo(sense = HybridSolverOptSenses.MINIMIZE if self.sense == ObjSense.MINIMIZE
                  else HybridSolverOptSenses.MAXIMIZE)

    # return QUBO (variables are the same as they were binary)
    i2q.fromIP(mip, mip_format = MIPSourceFormat.MIP_INTERMEDIATE)
    mdl = i2q.toQUBO(self.penalty)

    return mdl

###
# PyQUBO adapter
#
# Same as in the D-Wave adapter, pyqubo does not contain the sense explicitly,
# but always assumes minimization
###

class PyQUBOAdapter(QUBOAdapter):
  """
  A class that adapts a PyQUBO quadratic model to a Quantagonia :class:`QuboModel`.
  Note that pyqubo does not contain the sense explicitly, but always assumes minimization, so we also set the sense to minimization in the QUBOs obtained from the conversion process.
  """

  def __init__(self):
    super().__init__()

  def convert(self, pqm : pq.Model, constants = {}) -> QuboModel:
    """
    Converts a PyQUBO quadratic model to a :class:`QuboModel` that can be solved by Quantagonia solvers.

    Args:
      pqm (:class:`pyqubo.Model`) : A :class:`pyqubo.Model` to be converted.
      constants (dict) : A dictionary of constant values that can be used in the conversion.

    Returns:
      QuboModel: The resulting :class:`QuboModel`.
    """

    qubo = QuboModel(HybridSolverOptSenses.MINIMIZE)

    # guarantees that we only have terms of oders {1, 2}
    qmodel, shift = pqm.to_qubo(feed_dict = constants)

    # create objective from QUBO model
    for term in qmodel:
      if(term[0] == term[1]):
        # unary term
        v = qubo.addVariable(term[0], disable_warnings=True)
        qubo.objective += QuboTerm(qmodel[term], [v])
      else:
        # pairwise term
        v0 = qubo.addVariable(term[0], disable_warnings=True)
        v1 = qubo.addVariable(term[1], disable_warnings=True)
        qubo.objective += QuboTerm(qmodel[term], [v0, v1])

    if shift != 0:
      qubo.objective += shift

    return qubo
