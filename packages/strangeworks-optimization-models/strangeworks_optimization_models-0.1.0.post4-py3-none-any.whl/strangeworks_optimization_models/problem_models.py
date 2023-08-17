import ast
import base64
import json
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

import dill
import jijmodeling as jm
import numpy as np
from dimod import (
    BinaryQuadraticModel,
    ConstrainedQuadraticModel,
    DiscreteQuadraticModel,
)


class StrangeworksModelType(Enum):
    BinaryQuadraticModel = "BinaryQuadraticModel"
    ConstrainedQuadraticModel = "ConstrainedQuadraticModel"
    DiscreteQuadraticModel = "DiscreteQuadraticModel"
    JiJProblem = "JiJProblem"
    AquilaModel = "ndarray"
    QuboDict = "QuboDict"
    MPSFile = "MPSFile"


class StrangeworksModel(ABC):
    model: Any
    model_type: StrangeworksModelType
    model_options: dict | None = None
    strangeworks_parameters: dict | None = None

    @abstractmethod
    def to_str(self) -> str:
        ...

    @staticmethod
    @abstractmethod
    def from_str(
        model_str: str,
    ) -> (
        BinaryQuadraticModel | ConstrainedQuadraticModel | DiscreteQuadraticModel | jm.Problem | np.ndarray | dict | str
    ):
        ...


class StrangeworksRemoteModel(StrangeworksModel):
    """
    TODO
    A model that is stored remotely and can be downloaded.
    Should be able to pass around a file identifier and download the model when needed.
    Should instantiate the appropriate model class when downloaded.

    Implementation proposal:

    ```
    model_url: str
    model_type: str
    headers: dict = None

    def to_str(self) -> str:
        return self.model_url

    def from_str(self, model_url=None):
        if model_url is None:
            model_url = self.model_url
        model_res = requests.get(model_url, headers=self.headers)
        model_str = model_res.content.decode(encoding=model_res.encoding)
        return StrangeworksModel.from_model_str(model_str)
    ```
    """

    pass


class StrangeworksBinaryQuadraticModel(StrangeworksModel):
    def __init__(self, model: BinaryQuadraticModel):
        self.model = model
        self.model_type = StrangeworksModelType.BinaryQuadraticModel

    def to_str(self) -> str:
        return json.dumps(self.model.to_serializable())

    @staticmethod
    def from_str(model_str: str) -> BinaryQuadraticModel:
        return BinaryQuadraticModel.from_serializable(json.loads(model_str))


class StrangeworksConstrainedQuadraticModel(StrangeworksModel):
    def __init__(self, model: ConstrainedQuadraticModel):
        self.model = model
        self.model_type = StrangeworksModelType.ConstrainedQuadraticModel

    def to_str(self) -> str:
        cqm_file = self.model.to_file()
        cqm_bytes = base64.b64encode(cqm_file.read())
        return cqm_bytes.decode("ascii")

    @staticmethod
    def from_str(model_str: str) -> ConstrainedQuadraticModel:
        return ConstrainedQuadraticModel.from_file(base64.b64decode(model_str))


class StrangeworksDiscreteQuadraticModel(StrangeworksModel):
    def __init__(self, model: DiscreteQuadraticModel):
        self.model = model
        self.model_type = StrangeworksModelType.DiscreteQuadraticModel

    def to_str(self) -> str:
        cqm_file = self.model.to_file()
        cqm_bytes = base64.b64encode(cqm_file.read())
        return cqm_bytes.decode("ascii")

    @staticmethod
    def from_str(model_str: str) -> DiscreteQuadraticModel:
        dqm = DiscreteQuadraticModel.from_file(base64.b64decode(model_str))
        if isinstance(dqm, DiscreteQuadraticModel):
            return dqm
        else:
            raise TypeError("Unexpected type for DQM model")


class StrangeworksQuboDictModel(StrangeworksModel):
    def __init__(self, model: dict):
        self.model = model
        self.model_type = StrangeworksModelType.QuboDict

    def to_str(self) -> str:
        model_str_keys = {str(key): value for key, value in self.model.items()}
        return json.dumps(model_str_keys)

    @staticmethod
    def from_str(model_str: str) -> dict:
        model_str_keys = json.loads(model_str)
        return {ast.literal_eval(key): value for key, value in model_str_keys.items()}


class StrangeworksMPSFileModel(StrangeworksModel):
    def __init__(self, model: str):
        self.model = model
        self.model_type = StrangeworksModelType.MPSFile

    def to_str(self) -> str:
        with open(self.model, "r") as f:
            return f.read()

    @staticmethod
    def from_str(model_str: str) -> dict:
        model_str_keys = json.loads(model_str)
        return {ast.literal_eval(key): value for key, value in model_str_keys.items()}


class StrangeworksJiJProblem(StrangeworksModel):
    def __init__(self, model: jm.Problem):
        self.model = model
        self.model_type = StrangeworksModelType.JiJProblem

    def to_str(self) -> str:
        return base64.b64encode(jm.to_protobuf(self.model)).decode()

    @staticmethod
    def from_str(model_str: str) -> jm.Problem:
        return jm.from_protobuf(base64.b64decode(model_str))  # type: ignore


class StrangeworkAquilaProblem(StrangeworksModel):
    def __init__(self, model: np.ndarray):
        self.model = model
        self.model_type = StrangeworksModelType.AquilaModel

    def to_str(self) -> str:
        return base64.b64encode(dill.dumps(self.model)).decode()

    @staticmethod
    def from_str(model_str: str) -> np.ndarray:
        return np.array(dill.loads(base64.b64decode(model_str)))


class StrangeworksModelFactory:
    @staticmethod
    def from_model(model: Any) -> StrangeworksModel:
        if isinstance(model, StrangeworksModel):
            return model
        elif isinstance(model, BinaryQuadraticModel):
            return StrangeworksBinaryQuadraticModel(model=model)
        elif isinstance(model, ConstrainedQuadraticModel):
            return StrangeworksConstrainedQuadraticModel(model=model)
        elif isinstance(model, DiscreteQuadraticModel):
            return StrangeworksDiscreteQuadraticModel(model=model)
        elif isinstance(model, dict):
            return StrangeworksQuboDictModel(model=model)
        elif isinstance(model, jm.Problem):
            return StrangeworksJiJProblem(model=model)
        elif isinstance(model, np.ndarray):
            return StrangeworkAquilaProblem(model=model)
        elif isinstance(model, str):  # TODO should be an object from miplib or gurobi, string is too general
            return StrangeworksMPSFileModel(model=model)
        else:
            raise ValueError("Unsupported model type")

    @staticmethod
    def from_model_str(
        model_str: str, model_type: str, model_options: str | None = None, strangeworks_parameters: str | None = None
    ):
        """
        From a type and string representation of a model, return the appropriate
        StrangeworksModel. This is currently how we are deserializing models from
        into general native data formats.
        """
        m: BinaryQuadraticModel | ConstrainedQuadraticModel | DiscreteQuadraticModel | jm.Problem | np.ndarray | dict | str
        strangeworks_model_type = StrangeworksModelType(model_type)
        if strangeworks_model_type == StrangeworksModelType.BinaryQuadraticModel:
            m = StrangeworksBinaryQuadraticModel.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.ConstrainedQuadraticModel:
            m = StrangeworksConstrainedQuadraticModel.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.DiscreteQuadraticModel:
            m = StrangeworksDiscreteQuadraticModel.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.QuboDict:
            m = StrangeworksQuboDictModel.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.MPSFile:
            m = StrangeworksMPSFileModel.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.JiJProblem:
            m = StrangeworksJiJProblem.from_str(model_str)
        elif strangeworks_model_type == StrangeworksModelType.AquilaModel:
            m = StrangeworkAquilaProblem.from_str(model_str)
        else:
            raise ValueError("Unsupported model type")
        sm = StrangeworksModelFactory.from_model(m)
        sm.model_type = strangeworks_model_type
        sm.model_options = json.loads(model_options) if model_options else None
        sm.strangeworks_parameters = json.loads(strangeworks_parameters) if strangeworks_parameters else None
        return sm
