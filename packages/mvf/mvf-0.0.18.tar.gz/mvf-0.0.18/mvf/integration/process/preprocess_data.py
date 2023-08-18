import feather

def preprocess_data(product: dict, params):
    '''
    Run checks on dataset after preprocess_data process.
    '''
    # load datasets
    X = feather.read_dataframe(product['X_data'])
    y = feather.read_dataframe(product['y_data'])
    # check the expected features exist
    for input in params['input_features']:
        assert input in X.columns, f'{input} is specified as an input feature. A column named {input} must be in the \'X\' data frame.'
    for target in params['target_features']:
        assert target in y.columns, f'{target} is specified as an target feature. A column named {target} must be in the \'y\' data frame.'
    # check dimensionality of data
    assert len(X.shape) == 2, f'Expected the X data to have 2 dimensions, has {len(X.shape)}'
    assert len(y.shape) == 2, f'Expected the y data to have 2 dimensions, has {len(y.shape)}'  
