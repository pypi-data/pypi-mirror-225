import importlib
from src.mdrunner import Runner
from tests.models import ModelType


class Test_2:

    def test_models(self):
        ''' Register and run models '''

        # configure models to run
        all_models = importlib.import_module('tests.models')
        selected_models = ['S2', 'A1', 'B1']
        runner = Runner(all_models, selected_models)

        # feed models with external inputs
        values = {'p1': 2.0, 'p2': 3.0, 'p3': 4.0}
        runner.add_input_to_model(values, ModelType.S)

        # run models
        runner.run_models()

        # check results
        assert runner.input == {
            'S.input.p1': 2.0,
            'S.input.p2': 3.0,
            'S.input.p3': 4.0
        }

        assert runner.output == {
            'A.output.x': 6.0,
            'B.output.x': 24.0,
        }

        assert runner.A.output.x == 6.0
        assert runner.B.output.x == 24.0
        assert runner.S.input.p1 == 2.0
        assert runner.S.input.p2 == 3.0
        assert runner.S.input.p3 == 4.0
