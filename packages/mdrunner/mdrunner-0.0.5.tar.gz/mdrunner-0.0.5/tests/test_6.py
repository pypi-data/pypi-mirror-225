import importlib
from src.mdrunner import Runner, Model
from tests.models import ModelType
from typing import List


class Test_6:

    def test_models(self):
        ''' Register and run models '''

        # configure models to run
        all_models = importlib.import_module('tests.models')
        selected_models = ['F1', 'B3', 'C3', 'A2', 'S3']
        runner = Runner(all_models, selected_models)

        # feed models with external inputs
        values = {'p1': 2.0, 'p2': 3.0, 'p3': 4.0}

        runner.add_input_to_model(values, ModelType.S)

        # run models
        runner.run_models()

        # check run order
        assert [model.type.name for model in runner.model_run_order] == ['S', 'A', 'B', 'C', 'F']
        assert [model.name for model in runner.model_run_order] == ['S3', 'A2', 'B3', 'C3', 'F1']

        # check params
        assert runner.input == {
            'S.input.p1': 2.0,
            'S.input.p2': 3.0,
            'S.input.p3': 4.0
        }

        assert runner.output == {
            'A.output.x': 12.0,
            'B.output.x': 19.0,
            'C.output.x': 35.0,
            'S.output.x': 7.0,
            'F.output.x': 73.0
        }

        # check input
        assert runner.S.output.x == 7.0

        self.check_model(
            model=runner.S,
            expected_input_param_names=['p1', 'p2', 'p3'],
            expected_output_param_names=['x'],
            expected_notifying_model_types=[])

        # check A
        assert runner.A.output.x == 12.0
        self.check_model(
            model=runner.A,
            expected_input_param_names=[],
            expected_output_param_names=['x'],
            expected_notifying_model_types=[])

        # check B
        assert runner.B.output.x == 19.0
        self.check_model(
            model=runner.B,
            expected_input_param_names=[],
            expected_output_param_names=['x'],
            expected_notifying_model_types=[])

        # check C
        assert runner.C.output.x == 35.0

        self.check_model(
            model=runner.C,
            expected_input_param_names=[],
            expected_output_param_names=['x'],
            expected_notifying_model_types=[])

        # check output
        assert runner.F.output.x == 73.0
        self.check_model(
            model=runner.F,
            expected_input_param_names=[],
            expected_output_param_names=['x'],
            expected_notifying_model_types=[ModelType.B, ModelType.C, ModelType.A, ModelType.S])

    def check_model(
            self, model: Model,
            expected_input_param_names: List[str],
            expected_output_param_names: List[str],
            expected_notifying_model_types: List[ModelType],
    ):
        names = [param_name for param_name, param in model.input.params.items()]
        assert names == expected_input_param_names

        names = [param_name for param_name, param in model.output.params.items()]
        assert names == expected_output_param_names

        types = [model.type for model in model.notifying_models]
        assert types == expected_notifying_model_types
