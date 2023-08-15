from src.mdrunner.model_selector import ModelSelector


class Test_7:

    def test_model_selector(self):
        rules = {
            'A': {'A1': 'x == 1', 'A2': '2 <= x <= 4', 'A3': 'x >= 5'},
            'B': {'B1': '(x+y) < 4', 'B2': 'y > 5'}
        }
        x = 2
        y = 1
        selected_models = ModelSelector.select(rules, globals(), locals())
        assert selected_models == ['A2', 'B1']
