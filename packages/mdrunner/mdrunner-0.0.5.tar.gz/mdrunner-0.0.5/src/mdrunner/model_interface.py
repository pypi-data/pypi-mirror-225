from typing import Dict


class ModelInterface():
    """Class for holding model parameters"""

    def __init__(self, name: str):
        self.name = name
        self._params = {}

    @property
    def params(self) -> Dict[str, any]:
        """Returns a dict with all model input parameters as.
        { 'model_type.param_name' : value }  of type (str:any)"""
        return self._params
