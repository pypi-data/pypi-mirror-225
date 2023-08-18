# imports
from mvf.process.utils import import_model_class, init_model

# + tags=["parameters"]
upstream = None
product = None
model_name = ''
split_type = 'train_test'
n_folds = 10
lang = ''
# -

# import model module
model_module = import_model_class(lang)

# run validation
if split_type == 'train_test':
    # load model
    model = init_model(
        model_module, 
        lang,
        model_name,
    )
    model.load(str(next(iter(upstream.values()))['model']))
    # run model specific validation
    model.validate()
elif split_type == 'k_fold':
    for i in range(1, n_folds+1):
        # load model
        model = init_model(
            model_module, 
            lang,
            model_name,
        )
        model.load(str(next(iter(upstream.values()))[f'model_{i}']))
        # run model specific validation
        model.validate()