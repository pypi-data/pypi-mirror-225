from .model_interface import ModelInterface


class ModelInput(ModelInterface):
    """Class for holding model parameters"""

    def __init__(self):
        super().__init__(name='input')
