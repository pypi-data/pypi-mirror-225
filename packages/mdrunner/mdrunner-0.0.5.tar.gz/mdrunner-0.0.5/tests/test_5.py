import importlib
from src.mdrunner import Runner
from tests.models import ModelType
import numpy as np


class Test_5:

    def test_models(self):
        ''' Register and run models '''

        # configure models to run
        all_models = importlib.import_module('tests.models')
        selected_models = ['S2', 'A1', 'B1']
        runner = Runner(all_models, selected_models)

        # feed models with external inputs
        p1 = np.array([1.0, 2.0, 3.0])
        p2 = np.array([4.0, 5.0, 6.0])
        p3 = np.array([7.0, 8.0, 9.0])
        values = {'p1': p1, 'p2': p2, 'p3': p3}

        runner.add_input_to_model(values, ModelType.S)

        # run models
        runner.run_models()

        # check results
        assert np.array_equal(runner.S.input.p1, np.array([1.0, 2.0, 3.0]))
        assert np.array_equal(runner.S.input.p2, np.array([4.0, 5.0, 6.0]))
        assert np.array_equal(runner.S.input.p3, np.array([7.0, 8.0, 9.0]))

        # A.output.x = S.input.p1 * S.input.p2
        assert np.array_equal(runner.A.output.x, np.array([4, 10, 18]))
        # B.output.x = A.output.x * S.input.p3
        assert np.array_equal(runner.B.output.x, np.array([28.0, 80, 162.0]))
