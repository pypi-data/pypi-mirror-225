from .model import Model
from typing import Dict


class RunnerProtected:
    """This class instantiates and run all models defined in the _models_to_run that is situated in a _model_package"""

    def __init__(self, model_package: 'python_package', models_to_run: Dict['ModelType', str]):
        """instantiated all models"""
        '''_model_package
            the imported python package of DimensioningModels to execute.
            The models imported using importlib e.g. using
            _model_package = importlib.import_module('models')'''
        self._model_package = model_package

        '''_models_to_run
            dictionary of ModelType and the corresponding class name where the calculations are defined
            { ModelType: 'model_class_name' }'''
        self._models_to_run = models_to_run
        self._check_models_to_run()

        '''_created_models
            { ModelType: model_instance }'''
        self._created_models = {}

        '''_model_run_order
            The order the models shall be executed, considering model dependencies
            A list of lists with one list per dependency level. Execution will start at the top. 
            [
                [model_a_instance],
                [model_d_instance, model_b_instance],
                [model_c_instance]
            ]'''
        self._model_run_order = [[]]

        # prepare for models to be executed
        self._create_models()
        self._init_models()
        self._set_model_run_order()

    def _check_models_to_run(self):
        """make sure no duplicates exist"""
        numof_models = len(self._models_to_run)
        numof_unique_models = len(set(self._models_to_run))
        if numof_models != numof_unique_models:
            raise ValueError(
                f"duplicate models found in {self._models_to_run}")

    def _create_models(self):
        """instantiate and register models"""
        for model_class_name in self._models_to_run:
            model_instance = self._create_model(model_class_name)
            self._register_model(model_instance)

    def _create_model(self, model_class_name: str) -> Model:
        """instantiate the model by its model class name
        and passing a callback pointer to this object model_class_name(self)
        e.g. like Model_X(model_runner)"""
        try:
            class_definition = getattr(self._model_package, model_class_name)
            model_instance = class_definition(self)
        except Exception as e:
            raise KeyError(
                f"failed to instantiate model: {model_class_name}'"
                f" not found in model library {self._model_package}") from e
        return model_instance

    def get_model_instance(self, model_type: 'ModelType') -> Model:
        """return the model instance associated with the user defined ModelType"""
        try:
            return self._created_models[model_type]
        except KeyError as e:
            raise KeyError(
                f'model instance for model type "{model_type}" does not exist') from e

    def _register_model(self, model_instance: Model):
        """register the instantiated model"""
        # add instantiated model to model dict
        model_type = model_instance.model_type
        if not model_type:
            raise ValueError(
                f"Missing model_type in model '{model_instance.name}' class definition")

        if model_type in self._created_models:
            current_model_name = model_instance.name
            previous_model_name = self._created_models[model_instance.model_type].name
            raise ValueError(
                f"two model instances ({previous_model_name} and {current_model_name}) "
                f"have the same model_type ({model_type})")
        else:
            self._created_models[model_type] = model_instance
            # add model to self for simplified access
            try:
                setattr(self, model_type.name, model_instance)
            except Exception as e:
                raise ValueError(
                    f"failed to register model '{model_instance.name}'"
                    f" of type '{model_type}'"
                    f" with error: {str(e)}") from e
        return

    def _init_models(self):
        """register the dependencies between all models
        each model instance knows what models they need input
        from before they can do any calculations"""
        for model_name, model in self._created_models.items():
            model._init()

    def _set_model_run_order(self):
        """Find the correct execution order between all models
        If a model B is depending on model A then model A has to be calculated before model B
        example of a dependency tree
            A --> B --> C
              --> D
        each model dependency depth is represented by one position in the list, e.g.
            _model_run_order = [
                [model_a_instance],
                [model_b_instance, model_d_instance],
                [model_c_instance]
            ]
        """
        for model_name, model_instance in self._created_models.items():
            depth = model_instance.get_model_dependency_depth()
            self._extend_model_run_order(depth)
            self._model_run_order[depth].append(model_instance)

    def _extend_model_run_order(self, depth: int):
        """Extends the _model_run_order list with needed dependency depth
        if the length is not enough"""
        needed_len = depth + 1
        list_len = len(self._model_run_order)
        if needed_len > list_len:
            for _ in range(needed_len - list_len):
                self._model_run_order.append([])

    @property
    def numof_created_models(self) -> int:
        """return the number of instantiated models"""
        return len(self._created_models)
