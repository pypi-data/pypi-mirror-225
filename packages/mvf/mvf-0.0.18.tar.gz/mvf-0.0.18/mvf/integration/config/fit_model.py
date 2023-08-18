def fit_model_params(product: dict, params: dict) -> None:
    '''
    Check params for fit_model tasks.
    '''
    assert 'model_name' in params, 'The \'model_name\' parameter must be defined.'
    assert 'split_type' in params, 'The \'split_type\' parameter must be defined.'
    if params['split_type'] == 'train_test':
        assert 'model' in product, 'The \'model\' product must be defined.'
    elif params['split_type'] == 'k_fold':
        assert 'n_folds' in params, 'For a K fold split, the n_folds must be defined.'
        n_folds = params['n_folds']
        for i in range(1, n_folds+1):
            assert f'model_{i}' in product, f'The {i}-th model product must be defined.'


def fit_model_r(product: dict, params: dict) -> None:
    '''
    Run R model checks prior to fit process.
    '''
    import rpy2.robjects as robjects
    import rpy2_r6.r6b as r6b

    # check params
    fit_model_params(product, params)
    # check that the correct model class is available
    r = robjects.r
    try:
        r.source('models.R')
        model_class = r6b.R6DynamicClassGenerator(r[params["model_name"]])
        model = model_class.new()
        check_model(model, params['model_name'])
    except rpy2.rinterface_lib.embedded.RRuntimeError:
        raise ModuleNotFoundError(f'If using an R based model for {params["model_name"]}, you must have a models.R file in your project directory.')


def fit_model_py(product: dict, params: dict) -> None:
    '''
    Run Python model checks prior to fit process.
    '''
    # check params
    fit_model_params(product, params)
    # check that the correct model class is available
    try:
        import models
        assert hasattr(models, params['model_name']), f'models.py must contain a class called {params["model_name"]}.'
        model_class = getattr(models, params['model_name'])
        check_model(model_class, params['model_name'])
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f'If using a Python based model for {params["model_name"]}, you must have a models.py file in your project directory. The project directory is {os.getcwd()}')
    

def check_model(model_class, model_name):
    '''
    Check the instantiated model class or generic model class has the necessary methods.
    '''
    # check the model class has a callable 'fit' method
    assert hasattr(model_class, 'fit'), f'The class {model_name} must have a fit() method. The class does not currently have a fit attribute.'
    assert callable(getattr(model_class, 'fit')), f'The class {model_name} must have a fit() method. The class\' fit attribute is not currently callable.'
    # check the model class has a callable 'save' method
    assert hasattr(model_class, 'save'), f'The class {model_name} must have a save() method. The class does not currently have a save attribute.'
    assert callable(getattr(model_class, 'save')), f'The class {model_name} must have a save() method. The class\' save attribute is not currently callable.'
    