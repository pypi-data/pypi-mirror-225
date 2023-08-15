class ModelSelector:
    @staticmethod
    def select(rules: 'dict[dict]', global_params: dict, local_params: dict, as_dict: bool = False):
        """select models based on the selection rule defined for each model version

        :param rules :
            A dict containing model_types, model_versions and selection_rules
            the rules decides what model to select
            { model_type [any] : { model_version [str] : rule [str] }

            model_type    : The type of model
            model_version : The version of the model (model class name)
            rule          : python code that shall return a bool to decide if
                            the model version shall be selected or not

        :param global_params :
            A dict containing the global symbol table, to be used for evaluating the rules.

        :param local_params :
            A dict containing the local symbol table, to be used for evaluating the rules.

        :param as_dict :
            A bool to decide to return a list (default) or a dict (True)

        return:
            A list with selected model versions [models version] or
            A dict with model_type and selected model_version (model class name)
            { model_type : model_version }

        >>> rules = {
        ... 'A': { 'A1': 'x == 1', 'A2': '1 < x <= 3', 'A3': 'x > 3'},
        ... 'B': { 'B1': '(x+y) < 4', 'B2': 'y > 5'}
        ... }
        >>> x = 2
        >>> y = 1
        >>> selection = ModelSelector.select(rules, globals(), locals())
        >>> selection
        ['A2', 'B1']
        >>> selection = ModelSelector.select(rules, globals(), locals(), True)
        >>> selection
        {'A': 'A2', 'B': 'B1'}
        """
        selected_models = {}
        for model_type, model_selection_rules in rules.items():
            for model_class_name, rule in list(model_selection_rules.items()):
                try:
                    if eval(rule, global_params, local_params):
                        selected_models[model_type] = model_class_name
                        break
                except Exception as e:
                    raise ValueError(f"failed to parse rule ({rule})"
                                     f" for model({model_class_name})"
                                     f" with error:"
                                     f" {str(e)}") from e

        if as_dict:
            return selected_models
        else:
            return list(selected_models.values())
