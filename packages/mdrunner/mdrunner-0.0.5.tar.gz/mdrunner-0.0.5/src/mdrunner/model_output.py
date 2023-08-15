from .model_interface import ModelInterface


class ModelOutput(ModelInterface):
    """Class for holding model parameters"""

    def __init__(self):
        super().__init__(name='output')
