import importlib
from src.mdrunner import Runner
from tests.models import ModelType


class Test_4:

    def test_models(self):
        ''' Register and run models '''

        # configure models to run
        all_models = importlib.import_module('tests.models')
        selected_models = ['S2', 'A2', 'B2', 'F1']
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
            'A.output.x': 12.0,
            'B.output.x': 48.0,
            'F.output.x': 60.0
        }

        assert runner.S.input.p1 == 2.0
        assert runner.S.input.p2 == 3.0
        assert runner.S.input.p3 == 4.0
        assert runner.A.output.x == 12.0
        assert runner.B.output.x == 48.0
        assert runner.F.output.x == 60.0
