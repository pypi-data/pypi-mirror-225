from schema import Schema, Or, Optional, And


def check_config(config):
    '''
    Checks the given config against a schema.
    '''
    # schema for mvf_conf.yaml
    mvf_conf = Schema(
        {
            'data': {
                'source': And(
                    str,
                    lambda s: s.endswith('.ipynb'),
                    error='Invalid `source` file extension. Must be ipynb.'
                ),
                'lang': Or('Python', 'R'),
                'split': Or('train_test', 'k_fold'),
                'input_features': [str],
                'target_features': [str],
                Optional('grouping_variable'): str,
                Optional('test_size'): lambda x: 0 <= x <= 1,
                Optional('n_folds'): And(int, lambda x: x > 0),
                Optional('temporal_split'): {
                    'temporal_variable': str,
                    'test_size': Or(
                        lambda x: 0 <= x <= 1,
                        [lambda x: 0 <= x <= 1],
                    )
                }
            },
            Optional('output'): {
                Optional('quantile_intervals'): [
                    [lambda x: 0 <= x <= 1],
                ],
            },
            'models': [
                {
                    'name': str,
                    'lang': Or('Python', 'R'),
                    Optional('validation_step'): bool,
                    Optional('return_quantiles'): bool,
                }
            ],
        }
    )
    # validate given schema
    mvf_conf.validate(config)
    # additional validation
    if 'n_folds' in config['data'] and 'test_size' in config['data']:
        raise Exception(
            'Only one of `test_size` and `n_folds` may be specified.')
    if config['data']['split'] == 'train_test' and 'n_folds' in config['data']:
        raise Exception(
            '`n_folds` is not a valid parameter for a \'train_test\' split.')
    if config['data']['split'] == 'k_fold' and 'test_size' in config['data']:
        raise Exception(
            '`test_size` is not a valid parameter for a \'k_fold\' split.')
    if 'temporal_split' in config['data'] and 'grouping_variable' not in config['data']:
        raise Exception(
            'If the `temporal_split` parameters are provided, a grouping variable must also be provided.')
    if 'output' in config:
        if 'quantile_intervals' in config['output']:
            for pair in config['output']['quantile_intervals']:
                assert len(
                    pair) == 2, 'Two quantiles must be provided for each interval.'
            for model in config['models']:
                try:
                    assert isinstance(
                        model['return_quantiles'], bool), '`return_quantiles` must be Boolean type.'
                except KeyError:
                    raise Exception(
                        'If `quantile_intervals` are passed in `output`, the `return_quantiles` parameter must be passed for each model.')
