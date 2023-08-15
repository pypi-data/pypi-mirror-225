from typing import Dict
from .model_interface import ModelInterface
from .model_input import ModelInput
from .model_output import ModelOutput


class ModelProtected:
    """Model base class, internal part
    The instantiation and execution of the models are governed by a Runner class.
    Models are defined by a model_type and a model_class_name that contains the calculations
    """

    def __init__(self, model_runner: 'Runner'):

        '''The parent class that instantiated this model'''
        self._model_runner = model_runner

        '''All input models connected to this model
           including <this_model>.depend_on() and
           <other_model>.notify() calls to <this_model>
        '''
        self._input_models = {}

        '''Other models that <this_model> has notified by a call to to 
            <this_model>.notify(<other_model>)
        '''
        self._notified_models = {}

        '''models that has notified <this_model> by a call to to
            <other_model>.notify(<this_model>)
        '''
        self._notifying_models = {}

        '''Input interface parameters
           external parameters added to this model from <runner>.add_input()'''
        self._input = ModelInput()

        '''Output interface parameters'''
        self._output = ModelOutput()

    def _init(self):
        ''' Register the dependencies between models '''
        # Let the user model register the models they <depend_on>
        # and the models they want to <notify>
        self.init()

    def _register_input_from(self, source_model_type: 'ModelType'):
        """Request input from a <source_model> that <this_model> needs data from
           <source_model> --> <this_model>
        """
        try:
            # <source_model>
            source_model = self._model_runner.get_model_instance(source_model_type)
            # add model to dict
            self._input_models[source_model_type] = source_model
            # add model as class attribute for easy access
            setattr(self, source_model_type.name, source_model)
        except Exception as e:
            raise ValueError(f"{self.name}._register_input_from({source_model_type}) failed") from e

    def _run(self):
        """This function is called prior to the run model to make sure
        preprocessing is handled before run can exectute
        This function is called by the Runner
        """
        # now we can call this models run method
        self.run()

    def register_notifying_model(self, model_type: 'ModelType', model_instance: 'Model'):
        '''
        A model has notified <this_model> by a call to
            <other_model>.notify( <this_model> )

        Register this request
        '''
        self._notifying_models[model_type] = model_instance
        self._register_input_from(model_type)

    def get_model_dependency_depth(self, loops: int = 0) -> int:
        """
        Find the level of input models this model is depending on
        Example: Find the max level for the following models
            modelA --> modelB --> modelC
                   --> modelD
        gives
            modelA = 0
            modelB = 1
            modelC = 2
            modelD = 1

        This is used for knowing the execution order of each model
        so each model has the needed input before execution

        The max number of loops without circular dependency if every models is referring to all previous models
        The first model does not refer to any model
        n = models
        i = models that can depends on other models = n - 1
        max dependencies = i(i+1)/2 = (n-1)(n-1+1)/2 = (n-1)n/2
        example A -> B,  A,B -> C, A,B,C -> D
        total num of dependencies = 1+2+3+ ... + (n-1) = (n-1)n/2
        """
        depth = [0]
        n = self._model_runner.numof_created_models
        i = n - 1
        max_loop = (n - 1) * n / 2
        for model_name, model_instance in self._input_models.items():
            loops += 1
            if loops > max_loop:
                raise ValueError(
                    f"Model '{self.name}' (ModelType.{self.model_type.name}):"
                    f" circular dependency found between models"
                    f" ({max_loop} loops, {n} models)")
            child_depth = model_instance.get_model_dependency_depth(loops) + 1
            depth.append(child_depth)
        return max(depth)

    def _add_param(self, name: str, val: any, mif: ModelInterface):
        """Add an interface parameter to the model"""

        if not isinstance(name, str):
            raise AttributeError(f"The parameter name ({name}) must be a string"
                                 f" for '{self.name}.{mif.name}.{name}'")

        if not name.isidentifier():
            raise AttributeError(f"The parameter name ({name}) is not a valid identifier"
                                 f" for '{self.name}.{mif.name}.{name}'")

        """ add as parameter, allow overwriting any existing value"""
        mif.params[name] = val

        """add as object attribute, allow overwriting any existing value"""
        try:
            setattr(mif, name, val)
        except Exception as e:
            raise KeyError(f"Failed to add parameter as attribute"
                           f" for '{self.name}.{mif.name}.{name} = {val}'") from e

    def get_model_interface_params_full_path(self, mif: ModelInterface) -> Dict[str, any]:
        """Returns a dict with model interface parameters as.
        { '<model_type>.<mif.name>.<param_name>' : <param.value> }  of type (str:any)"""
        params = {}
        for param_name, param_val in mif.params.items():
            params[f"{self.type.name}.{mif.name}.{param_name}"] = param_val
        return params
