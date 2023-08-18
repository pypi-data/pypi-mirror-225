def preprocess_data(product: dict) -> None:
    '''
    Run checks prior to preprocess_data process.
    '''
    # check product params
    assert 'X_data' in product, 'The \'X_data\' product must be defined.'
    assert 'y_data' in product, 'The \'y_data\' product must be defined.'