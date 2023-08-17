import json

from pydantic import BaseModel, Field

from strangeworks_optimization_models.problem_models import StrangeworksModelFactory
from strangeworks_optimization_models.solution_models import StrangeworksSolutionFactory
from strangeworks_optimization_models.solver_models import StrangeworksSolverFactory


class StrangeworksOptimizationModel(BaseModel):
    model: str
    model_type: str
    model_options: str | None = None
    strangeworks_parameters: str | None = None

    def deserialize(self):
        """
        Build a StrangeworksModel from a StrangeworksOptimizationModel.
        """
        model = StrangeworksModelFactory.from_model_str(
            self.model,
            self.model_type,
            self.model_options,
            self.strangeworks_parameters,
        )
        return model

    @classmethod
    def from_model(cls, model):
        """
        Build pydantic model from any of the StrangeworksModelTypes.
        """
        strangeworks_model = StrangeworksModelFactory.from_model(model)  # Make sure this is a StrangeworksModel
        model_str = strangeworks_model.to_str()  # Serialize native data from StrangeworksModel to string
        model_type = strangeworks_model.model_type.value
        model_options = json.dumps(strangeworks_model.model_options)
        strangeworks_parameters = json.dumps(strangeworks_model.strangeworks_parameters)
        return cls(
            model=model_str,  # Serialize native data from StrangeworksModel to string
            model_type=model_type,
            model_options=model_options,
            strangeworks_parameters=strangeworks_parameters,
        )


class StrangeworksOptimizationSolver(BaseModel):
    solver: str | None = None
    solver_type: str | None = None
    solver_options: str | None = None
    strangeworks_parameters: str | None = None

    def deserialize(self):
        """
        Build a StrangeworksSolver from a StrangeworksOptimizationSolver.
        """
        solver = StrangeworksSolverFactory.from_solver_str(
            self.solver,
            self.solver_type,
            self.solver_options,
            self.strangeworks_parameters,
        )
        return solver

    @classmethod
    def from_solver(cls, solver):
        strangeworks_solver = StrangeworksSolverFactory.from_solver(solver)
        return cls(
            solver=strangeworks_solver.to_str(),
            solver_type=strangeworks_solver.solver_type.value,
            solver_options=json.dumps(strangeworks_solver.solver_options),
            strangeworks_parameters=json.dumps(strangeworks_solver.strangeworks_parameters),
        )


class StrangeworksOptimizationSolution(BaseModel):
    solution: str
    solution_type: str | None = None
    solution_options: str | None = None
    strangeworks_parameters: str | None = None

    def deserialize(self):
        """
        Build a StrangeworksSolution from a StrangeworksOptimizationSolution.
        """
        solution = StrangeworksSolutionFactory.from_solution_str(
            self.solution,
            self.solution_type,
            self.solution_options,
            self.strangeworks_parameters,
        )
        return solution

    @classmethod
    def from_solution(cls, solution):
        strangeworks_solution = StrangeworksSolutionFactory.from_solution(solution)
        return cls(
            solution=strangeworks_solution.to_str(),
            solution_type=strangeworks_solution.solution_type.value,
            solution_options=json.dumps(strangeworks_solution.solution_options),
            strangeworks_parameters=json.dumps(strangeworks_solution.strangeworks_parameters),
        )


class StrangeworksOptimizationJob(BaseModel):
    model: StrangeworksOptimizationModel = Field(...)
    solver: StrangeworksOptimizationSolver = Field(...)
    solution: StrangeworksOptimizationSolution | None = Field(None)
