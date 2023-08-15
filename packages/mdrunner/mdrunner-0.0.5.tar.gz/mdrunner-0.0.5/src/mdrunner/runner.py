from .model import Model
from .runner_protected import RunnerProtected
from typing import List, Dict


class Runner(RunnerProtected):
    """This class instantiates and run all models defined in the _models_to_run that is situated in a _model_package"""

    def __init__(self, model_package: 'python_package', models_to_run: 'Dict[ModelType, str]'):
        """
        _model_package:
            the imported python package of DimensioningModels to execute.
            The models imported using importlib e.g. using
            _model_package = importlib.import_module('models')
        _models_to_run:
            A dict with the selected model versions to run
            The user defined ModelType and the name of the class
            [ModelType, model_class_name]"""
        super().__init__(model_package, models_to_run)

    def add_input_to_model(self, params: Dict[str, any], model_type: 'ModelType'):
        """Import external Params to a model
        params :
            a dict with {name : value} pairs of type {str : any}
        model_type :
            the user defined ModelType of the receiving model"""
        try:
            model_instance = self.get_model_instance(model_type)
        except Exception as e:
            raise Exception(
                f"failed to get add model '{model_type}')") from e
        for name, val in params.items():
            try:
                model_instance.add_input(name, val)
            except Exception as e:
                raise Exception(
                    f"failed to add parameter '{name} =  {val}'"
                    f" to '{model_type}')") from e

    def run_models(self):
        """Run all registered models in the correct execution order"""
        for model in self.model_run_order:
            try:
                model._run()
            except Exception as e:
                raise Exception(f"failed to run model '{model.name}'") from e

    @property
    def input(self) -> Dict[str, any]:
        """Returns a dict with all model input parameters as.
        { 'model_type.input.param_name' : value }  of type (str:any)"""
        params = {}
        for name, model in self._created_models.items():
            params.update(model.get_model_interface_params_full_path(model.input))
        return params

    @property
    def output(self) -> Dict[str, any]:
        """Returns a dict with all model output parameters as.
        { 'model_type.output.param_name' : value }  of type (str:any)"""
        params = {}
        for name, model in self._created_models.items():
            params.update(model.get_model_interface_params_full_path(model.output))
        return params

    def models(self) -> Dict['ModelType', Model]:
        """Return a dict with the model type and instance
        { 'model_type_name' : model_instance }  of type (str:any)"""
        return self._created_models

    @property
    def model_run_order(self) -> 'List[Model]':
        """Return a list of models in the order of execution"""
        models = []
        for dependency_level in self._model_run_order:
            for model in dependency_level:
                models.append(model)
        return models
