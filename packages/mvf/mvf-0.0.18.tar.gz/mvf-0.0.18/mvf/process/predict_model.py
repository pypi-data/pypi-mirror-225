# imports
import feather
import pandas
from mvf.process.utils import ProcessTimer, convert_to_pandas_data, import_model_class, init_model, convert_to_r_data


def predict_model(upstream, product, lang, model_name, split_type, n_folds=10, quantile_intervals=None, target_features=[]):
    '''
    Main method to predict from fit model(s). Behaviour depends on project configuration.
    '''
    # start process timer
    timer = ProcessTimer(f'{model_name}_predict')
    # format variable
    upstream = dict(upstream)

    # import model class
    model_module = import_model_class(lang)

    if split_type == 'train_test':
        preds = make_prediction(
            upstream['split_data']['test_X_data'],
            str(upstream[f'{model_name}_fit']['model']),
            lang,
            model_module,
            model_name,
            quantile_intervals
        )
        # save data for next process
        feather.write_dataframe(preds, product['predictions'])
    elif split_type == 'k_fold':
        # allocate memory for predictions
        predictions = []
        # for each fold
        for i in range(1, n_folds+1):
            preds = make_prediction(
                upstream['split_data'][f'fold_{i}_X_data'],
                str(upstream[f'{model_name}_fit'][f'model_{i}']),
                lang,
                model_module,
                model_name,
                quantile_intervals
            )
            # append fold predictions to predictions set
            predictions.append(preds)
        # save data for next process
        feather.write_dataframe(
            pandas.concat(predictions),
            product['predictions']
        )
    # end process timer
    timer.end()
    # save process metadata
    timer.save(product['process_metadata'])
    

def make_prediction(data_path, model_path, lang, model_module, model_name, quantile_intervals):
    '''
    Makes a prediction based on a set of test data and a path to a fit model.
    '''
    # load test data
    X_test = feather.read_dataframe(data_path)

    # initialise and load model
    model = init_model(
        model_module,
        lang,
        model_name
    )
    model.load(model_path)

    if lang == 'R':
        # convert pandas dataframe to R dataframe
        X_test = convert_to_r_data(X_test)
        if quantile_intervals is None:
            # convert quantiles to R data
            r = model_module['r']
            quantile_intervals = r('NULL')

    # predict
    preds = model.predict(X_test, quantile_intervals)

    if lang == 'R':
        # convert to pandas dataframe
        preds = convert_to_pandas_data(preds)
    return preds

