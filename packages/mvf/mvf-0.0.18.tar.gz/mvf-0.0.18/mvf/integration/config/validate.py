def validate(product):
    '''
    Run checks prior to common validate process.
    '''
    assert 'nb' in product, 'The \'nb\' product must be defined.'
    