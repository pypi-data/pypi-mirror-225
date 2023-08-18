def predict_model_py(product, params):
    '''
    Run Python model checks prior to predict process.
    '''
    import models
    # get model class
    model_class = getattr(models, params['model_name'])
    # init model
    model = model_class()
    # run common checks
    predict_model_common(product, params, model)
    

def predict_model_r(product, params):
    '''
    Run R model checks prior to predict process.
    '''
    import rpy2.robjects as robjects
    import rpy2_r6.r6b as r6b
    # get model class
    r = robjects.r
    r.source('models.R')
    model_class = r6b.R6DynamicClassGenerator(r[params['model_name']])
    # init model
    model = model_class.new()
    # run common checks
    predict_model_common(product, params, model)
    

def predict_model_common(product, params, model):
    '''
    Run checks common to Python and R models.
    '''
    assert 'predictions' in product, 'The \'predictions\' product must be defined.'
    # check the model has a predict method
    assert hasattr(model, 'predict'), f'The model class defined for {params["model_name"]} must have a predict() method.'
    assert callable(getattr(model, 'predict')), f'The model saved at {params["model_name"]} must have a predict() method. The class\' predict attribute is not currently callable.'
    # check the model has a load method
    assert hasattr(model, 'load'), f'The model class defined for {params["model_name"]} must have a load() method.'
    assert callable(getattr(model, 'load')), f'The model saved at {params["model_name"]} must have a load() method. The class\' load attribute is not currently callable.'
