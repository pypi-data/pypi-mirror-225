import pandas
import feather


def predict_model(product, task, params):
    '''
    Check predictions are in expected format.
    '''
    # load target data
    if params['split_type'] == 'train_test':
        with open(task.upstream['split_data'].product['test_y_data'], 'rb') as f:
            target_data = feather.read_dataframe(f)
    elif params['split_type'] == 'k_fold':
        target_data = []
        for i in range(1, params['n_folds']+1):
            with open(task.upstream['split_data'].product[f'fold_{i}_y_data'], 'rb') as f:
                target_data.append(
                    feather.read_dataframe(f)
                )
        target_data = pandas.concat(target_data)
    target_shape = target_data.shape

    # load predictions
    predictions = feather.read_dataframe(product['predictions'])

    if 'quantile_intervals' in params:
        # check the quantiles are given in the columns
        quantiles = set()
        for interval in params['quantile_intervals']:
            quantiles.update(interval)
        for quantile in quantiles:
            for target in params['target_features']:
                str_quantile = f'{target}_Q{quantile * 100:g}'
                assert str_quantile in predictions.columns, f'{str_quantile} missing from predictions. Columns are {predictions.columns}.'

    # check the target features are returned by the predictions and that the predictions are of the right shape
    try:
        target_labels = params['target_features']
        assert target_shape == predictions[target_labels].shape, f'The predictions should have the same shape as the test data. Currently {predictions.shape} and {target_shape}.'
    except KeyError:
        raise Exception(f'{target_labels} are not in the columns. Columns are {predictions.columns}.')
