# imports
import pandas
import feather
from sklearn.model_selection import KFold, GroupShuffleSplit, train_test_split
import numpy


def split_data(upstream, product, split_type, test_size=0.5, n_folds=10, grouping_variable=None, temporal_split=None):
    '''
    Main method to split dataset.
    '''
    # load data from upstream process
    X = feather.read_dataframe(upstream['preprocess_data']['X_data'])
    y = feather.read_dataframe(upstream['preprocess_data']['y_data'])

    if grouping_variable is None:
        groups = None
    else:
        groups = X[grouping_variable]

    # parse split_type parameter
    if split_type == 'train_test':
        if groups is not None:
            # split data
            gss = GroupShuffleSplit(
                n_splits=1,
                test_size=test_size,
            )
            for train_idx, test_idx in gss.split(X, y, groups):
                X_train = X.iloc[train_idx]
                y_train = y.iloc[train_idx]
                X_test = X.iloc[test_idx]
                y_test = y.iloc[test_idx]
                if temporal_split:
                    temp_var = temporal_split['temporal_variable']
                    # split target feature time series into train and test
                    y_test, y_train_sup = y_temporal_split(
                        X_test,
                        y_test,
                        temp_var,
                        grouping_variable,
                        temporal_split['test_size']
                    )
                    # add supplementary training data back into training set
                    X_train = pandas.concat([X_train, X_test])
                    y_train = pandas.concat([y_train, y_train_sup])
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=test_size
            )
        # print metadata
        print(f'X_train shape: {X_train.shape}')
        print(f'X_test shape: {X_test.shape}')
        print(f'y_train shape: {y_train.shape}')
        print(f'y_test shape: {y_test.shape}')
        # save data for next process
        feather.write_dataframe(X_train, product['train_X_data'])
        feather.write_dataframe(X_test, product['test_X_data'])
        feather.write_dataframe(y_train, product['train_y_data'])
        feather.write_dataframe(y_test, product['test_y_data'])
    elif split_type == 'k_fold':
        kfolds = KFold(n_splits=n_folds)
        for i, (train_idx, test_idx) in enumerate(kfolds.split(X, groups=groups)):
            # split data
            fold_X_data = X.iloc[test_idx]
            fold_y_data = y.iloc[test_idx]
            # print metadata
            print(f'Fold {i+1} X shape: {fold_X_data.shape}')
            print(f'Fold {i+1} y shape: {fold_y_data.shape}')
            # save data for next process
            feather.write_dataframe(fold_X_data, product[f'fold_{i+1}_X_data'])
            feather.write_dataframe(fold_y_data, product[f'fold_{i+1}_y_data'])


def y_temporal_split(X_test, y_test, temp_var, grouping_variable, test_size):
    '''
    Temporal split of hierarchical time series.
    '''
    # allocate memory for supplementary training data
    y_train_sup = y_test.copy()

    target_not_null = y_test.notna().any(axis=1)
    df = X_test[target_not_null].groupby(
        grouping_variable
    )[temp_var].agg(
        ['min', 'max']
    )
    # determine the test size
    if isinstance(test_size, float):
        df['test_prop'] = numpy.full(
            df.shape[0], 
            test_size
        )
    else:
        df['test_prop'] = numpy.random.uniform(
            min(test_size),
            max(test_size),
            df.shape[0]
        )
    df['split_timestep'] = numpy.ceil(
        ((df['max'] - df['min']) * (1 - df.test_prop)) + df['min']
    )

    # mask to set test values to null
    m = X_test.groupby(
        grouping_variable
    ).apply(
        lambda g: g[temp_var] < df.loc[g[grouping_variable].unique()[
            0], 'split_timestep']
    ).reset_index(drop=True)
    # split time series
    y_test[m.values] = numpy.nan
    y_train_sup[~m.values] = numpy.nan

    return y_test, y_train_sup