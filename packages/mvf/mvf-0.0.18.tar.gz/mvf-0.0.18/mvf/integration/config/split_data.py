import numbers

def split_data(product: dict, params: dict) -> None:
    '''
    Run checks prior to split_data process.
    '''
    # check split_type
    assert 'split_type' in params, 'The \'split_type\' parameters must be provided.'
    supported_split_types = ['train_test', 'k_fold']
    assert params['split_type'] in supported_split_types, f"{params['split_type']} is not supported. Supported split types are {supported_split_types}."
    # given split, type check accompanying parameters
    if params['split_type'] == 'train_test':
        # check injection params
        assert 'test_size' in params, 'If the split_type is \'train_test\', the test_size parameter must be provided.'
        assert isinstance(params['test_size'], numbers.Number), f"test_size must be a number. Currently {type(params['test_size'])}."
        assert 0 <= params['test_size'] <= 1, f"test_size must be between 0 and 1. Currently {params['test_size']}."
        # check product params
        assert 'train_X_data' in product, 'The \'train_X_data\' product must be defined.'
        assert 'test_X_data' in product, 'The \'test_X_data\' product must be defined.'
        assert 'train_y_data' in product, 'The \'train_y_data\' product must be defined.'
        assert 'test_y_data' in product, 'The \'test_y_data\' product must be defined.'
    # else must be 'k_fold'
    else:
        # check injection params
        assert 'n_folds' in params, 'If the split_type is \'k_fold\', the n_folds parameter must be provided.'
        assert isinstance(params['n_folds'], int), f"n_folds must be a number. Currently {type(params['n_folds'])}."
        assert params['n_folds'] >= 2, f"n_folds must be at least 2. Currently {params['n_folds']}."
        # check product params
        for i in range(1, params['n_folds'] + 1):
            assert f'fold_{i}_X_data' in product, f'The \'fold_{i}_X_data\' product must be defined.'
            assert f'fold_{i}_y_data' in product, f'The \'fold_{i}_y_data\' product must be defined.'