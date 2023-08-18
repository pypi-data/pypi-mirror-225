def fit_model_py(product: dict, params: dict) -> None:
    '''
    Run checks after fit process for Python models.
    '''
    import models
    # get model class
    model_class = getattr(models, params['model_name'])
    # different tests by split type
    if params['split_type'] == 'train_test':
        # load model
        model = model_class()
        model.load(product['model'])
        # check the model has a predict method
        check_loaded_model(
            model,
            product["model"]
        )
    elif params['split_type'] == 'k_fold':
        for i in range(1, params['n_folds'] + 1):
            # load model
            model = model_class()
            model.load(product[f'model_{i}'])
            # check the model has a predict method
            check_loaded_model(
                model,
                product[f'model_{i}']
            )
    else:
        raise NotImplementedError(
            f"The {params['split_type']} implementation is not tested. This is unacceptable.")


def fit_model_r(product: dict, params: dict) -> None:
    '''
    Run checks after fit process for R models.
    '''
    import rpy2.robjects as robjects
    import rpy2_r6.r6b as r6b
    # get model class
    r = robjects.r
    r.source('models.R')
    model_class = r6b.R6DynamicClassGenerator(r[params['model_name']])

    # different tests by split type
    if params['split_type'] == 'train_test':
        # load model
        model = model_class.new()
        model.load(str(product['model']))
        # check the model has a predict method
        check_loaded_model(
            model,
            product["model"]
        )
    elif params['split_type'] == 'k_fold':
        for i in range(1, params['n_folds'] + 1):
            # load model
            model = model_class.new()
            model.load(str(product[f'model_{i}']))
            # check the model has a predict method
            check_loaded_model(
                model,
                product[f'model_{i}']
            )
    else:
        raise NotImplementedError(
            f"The {params['split_type']} implementation is not tested. This is unacceptable.")


def check_loaded_model(model, path):
    '''
    Check a loaded model has a predict() method.
    '''
    assert hasattr(
        model, 'predict'), f'The model saved at {path} must have a predict() method.'
    assert callable(getattr(
        model, 'predict')), f'The model saved at {path} must have a predict() method. The class\' predict attribute is not currently callable.'
