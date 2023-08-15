from .model_protected import ModelProtected
from typing import List


class Model(ModelProtected):
    """Model base class, end user part
    The instantiation and execution of the models are governed by a Runner class.
    Models are defined by a model_type and a model_class_name that contains the calculations
    """

    # A user defined ModelType needs to be defined for each instantiated model
    model_type = None

    def __init__(self, model_runner: 'Runner'):
        super().__init__(model_runner)

    def init(self):
        """Override this function to register needed input models
        for the calculations. This function is called by the Runner
        """
        raise NotImplementedError(
            f"Please implemented method 'def init(self):' in '{self.name}'")

    def run(self):
        """In each model override this function to do the actual model calculations
        This function is called by the Runner
        """
        raise NotImplementedError(
            f"Please implemented method 'def run(self):' in '{self.name}'")

    def depend_on(self, source_model_type: 'ModelType'):
        """Request input from a <source_model> that <this_model> needs access to
           <source_model> --> <this_model>"""
        try:
            self._register_input_from(source_model_type)
        except Exception as e:
            raise AttributeError(f"{self.name}.depend_on({source_model_type}) failed") from e

    def notify(self, target_model_type: 'ModelType'):
        """<this_model> wants to notify a <target_model>
           <this_model> --> <target_model>
           Tell the <target_model> that <this_model> has data that might be of interest
        """
        try:
            target_model_instance = self._model_runner.get_model_instance(target_model_type)
            this_model_type = self.model_type
            this_model_instance = self
            # let the <target_model> know that <this_model> has data that might be of interest
            target_model_instance.register_notifying_model(this_model_type, this_model_instance)
            # store this notification, allow for notifying the same model multiple times
            self._notified_models[target_model_type] = target_model_instance
        except Exception as e:
            raise AttributeError(f"{self.name}.notify({target_model_type}) failed") from e

    @property
    def input(self) -> 'ModelInterface':
        return self._input

    def add_input(self, name: str, val: any):
        """Add an input parameter to the model        """
        try:
            self._add_param(name, val, self.input)
        except Exception as e:
            raise ValueError(f"{self.name}.add_input() failed for"
                            f" {self.name}.{self.input.name}.{name} = {val}") from e

    @property
    def output(self) -> 'ModelInterface':
        return self._output

    def add_output(self, name: str, val: any):
        """Add an output parameter to the model        """
        try:
            self._add_param(name, val, self.output)
        except Exception as e:
            raise ValueError(f"{self.name}.add_output() failed for"
                            f" {self.name}.{self.output.name}.{name} = {val}") from e

    @property
    def type(self) -> 'ModelType':
        return self.model_type

    @property
    def name(self) -> str:
        """return the class name of this instance"""
        return type(self).__name__

    @property
    def input_models(self) -> List['Model']:
        """Return a list of models that <this_model> is depending on
           that <this_model> did with a call to <this_model>.depend_on() """
        models = []
        for model_name, model in self._input_models.items():
            models.append(model)
        return models

    @property
    def notifying_models(self) -> List['Model']:
        """Return a list of models that has notified <this_model>
           with a call to <other_model>.notify( <this_model> )
        """
        models = []
        for model_name, model in self._notifying_models.items():
            models.append(model)
        return models

    def notified_models(self) -> List['Model']:
        """Return a list of other models that <this_model> has notified
           with a call to <this_model>.notify( <other_model> )
        """
        models = []
        for model_name, model in self._notifying_models.items():
            models.append(model)
        return models

    def __repr__(self):
        return f"Model(name='{self.name}'," \
               f" type='{self.type}'," \
               f" input='{self.input.params}'," \
               f" output='{self.output.params}')"
