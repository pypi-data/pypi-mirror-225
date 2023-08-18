import os
from matplotlib import pyplot as plt
import feather
import pandas
from IPython.display import display, Markdown
import pickle
import sklearn.metrics


def load_validation_data(upstream, split_type, n_folds=10):
    '''
    Load validation data from upstream 'split_data' process.
    '''
    if split_type == 'train_test':
        validation_data = feather.read_dataframe(
            upstream['split_data']['test_y_data']
        ).reset_index(drop=True)

    elif split_type == 'k_fold':
        validation_data = []
        for i in range(1, n_folds+1):
            validation_data.append(
                feather.read_dataframe(
                    upstream['split_data'][f'fold_{i}_y_data'])
            )
        validation_data = pandas.concat(validation_data).reset_index(drop=True)
    return validation_data


def load_predictions(upstream, models):
    '''
    Load predictions from upstream 'predict_model' processes.
    '''
    predictions = {}
    for model_name in models:
        predictions[model_name] = feather.read_dataframe(
            upstream[f'{model_name}_predict']['predictions']
        ).reset_index(drop=True)
    return predictions


def error_metrics(target_features, predictions, validation_data):
    '''
    Calculate error metrics for each of the target features and for each model.
    '''
    # display a report for each target feature
    for target in target_features:
        # error
        error_df = pandas.DataFrame()
        for model, preds in predictions.items():
            # get predictions and ground truth
            mean_preds = preds[[target]].add_suffix('_pred', axis=1)
            ground_truth = validation_data[[
                target]].add_suffix('_truth', axis=1)
            # drop null validation values
            merged = pandas.concat([ground_truth, mean_preds], axis=1).dropna(
                subset=f'{target}_truth')
            # calculate metrics
            error_df.loc[model, 'MSE'] = sklearn.metrics.mean_squared_error(
                merged[f'{target}_truth'],
                merged[f'{target}_pred']
            )
            error_df.loc[model, 'RMSE'] = sklearn.metrics.mean_squared_error(
                merged[f'{target}_truth'],
                merged[f'{target}_pred'],
                squared=False
            )
            error_df.loc[model, 'MAE'] = sklearn.metrics.mean_absolute_error(
                merged[f'{target}_truth'],
                merged[f'{target}_pred']
            )
            error_df.loc[model, 'MAPE'] = sklearn.metrics.mean_absolute_percentage_error(
                merged[f'{target}_truth'],
                merged[f'{target}_pred']
            )
            error_df.loc[model, 'R-squared'] = sklearn.metrics.r2_score(
                merged[f'{target}_truth'],
                merged[f'{target}_pred']
            )
        print(f'Error metrics for `{target}` predictions:')
        display(error_df)


def qi_coverage(validation_data, target_features, predictions, quantile_intervals=[]):
    '''
    Calculate the coverage of for each quantile interval, for each target feature. 
    '''
    if quantile_intervals == []:
        print('No quantile intervals specified. Nothing to calculate.')
        return
    # display a report for each target feature
    for target in target_features:
        qi_coverage = pandas.DataFrame()
        # row index
        idx = 0
        for model, preds in predictions.items():
            for qi in quantile_intervals:
                lb = f'{target}_Q{min(qi) * 100:g}'
                ub = f'{target}_Q{max(qi) * 100:g}'
                if lb in preds.columns and ub in preds.columns:
                    qi_coverage.loc[idx, 'model'] = model
                    qi_coverage.loc[idx, 'interval'] = str(sorted(qi))
                    qi_coverage.loc[idx, 'level'] = max(qi) - min(qi)
                    # boolean mask for non-null validation values
                    m = validation_data[target].notna()
                    truth_above_lb = preds.loc[m,
                                               lb] <= validation_data.loc[m, target]
                    truth_below_ub = preds.loc[m,
                                               ub] >= validation_data.loc[m, target]
                    # boolean array for qi covering ground truth
                    in_interval = truth_above_lb & truth_below_ub
                    qi_coverage.loc[idx, 'coverage'] = in_interval.sum(
                    ) / in_interval.shape[0]
                    idx += 1
        print(f'Coverage metrics for `{target}` predictions:')
        display(qi_coverage.set_index(['model', 'interval']))


def qi_sharpness(target_features, predictions, quantile_intervals):
    '''
    Calculate the sharpness of each quantile interval for each target feature.
    '''
    if quantile_intervals == []:
        print('No quantile intervals specified. Nothing to calculate.')
        return
    # display a report for each target feature
    for target in target_features:
        qi_sharpness = pandas.DataFrame()
        for model, preds in predictions.items():
            for qi in quantile_intervals:
                lb = f'{target}_Q{min(qi) * 100:g}'
                ub = f'{target}_Q{max(qi) * 100:g}'
                if lb in preds.columns and ub in preds.columns:
                    qi_sharpness.loc[model, str(sorted(qi))] = (
                        preds[ub] - preds[lb]).mean()
        print(f'Sharpness metrics for `{target}` predictions:')
        display(qi_sharpness)


def computational_performance(upstream, models, split_type, n_folds=10):
    '''
    Calculates computational performance metrics for each model.
    '''
    # computational performance
    comp_perf = pandas.DataFrame()
    for model in models:
        # fit time
        with open(upstream[f'{model}_fit']['process_metadata'], 'rb') as f:
            fit_metadata = pickle.load(f)
        comp_perf.loc[model, 'fit time'] = fit_metadata[f'{model}_fit']
        # predict time
        with open(upstream[f'{model}_predict']['process_metadata'], 'rb') as f:
            predict_metadata = pickle.load(f)
        comp_perf.loc[model,
                      'predict time'] = predict_metadata[f'{model}_predict']
        # model size
        if split_type == 'train_test':
            # only one model
            comp_perf.loc[model, 'size'] = os.path.getsize(
                os.path.join(
                    'output',
                    'models',
                    f'{model}_fit'
                )
            )
        elif split_type == 'k_fold':
            # sum the model sizes
            total_size = 0
            for i in range(1, n_folds+1):
                total_size += os.path.getsize(
                    os.path.join(
                        'output',
                        'models',
                        f'{model}_fit_{i}'
                    )
                )
            comp_perf.loc[model, 'size'] = total_size
    display(comp_perf)


class Plot:
    '''
    Main plotting class. Holds matplotlib configs.
    '''
    colour_map = {
        0: 'tab:blue',
        1: 'tab:orange',
        2: 'tab:cyan',
        3: 'tab:purple',
        4: 'tab:grey'
    }
    line_map = {
        0: 'dotted',
        1: 'dashdot',
        2: 'dashed'
    }

    def __init__(self, models, target_features, validation_data, upstream, split_type):
        '''
        Sets basic class attributes.
        '''
        # set attributes
        self.models = models
        self.target_features = target_features
        self.validation_data = validation_data
        self.upstream = upstream
        self.split = split_type

    def plot(self, predictions, grouping_variable=None, quantile_intervals=None, temporal_variable=None):
        '''
        Main plotting method. Calls subsidiary plotting methods based on config.
        '''
        if grouping_variable and temporal_variable and self.split == 'train_test':
            self.group_var = grouping_variable
            self.temp_var = temporal_variable
            self.hierarchical_time_series_plot(predictions, quantile_intervals)
        else:
            print('Plotting for this project configuration has not been implemented yet.')

    def hierarchical_time_series_plot(self, predictions, quantile_intervals=None):
        '''
        Plots model predictions for hierarchical time series problems.
        '''
        if len(self.models) > 5:
            print(
                'Hierarchical time series plots are only supported for 5 models or fewer.')
            exit

        # extract upstream data
        X_train = feather.read_dataframe(
            self.upstream['split_data']['train_X_data']
        )
        X_test = feather.read_dataframe(
            self.upstream['split_data']['test_X_data']
        )
        y_train = feather.read_dataframe(
            self.upstream['split_data']['train_y_data']
        )
        y_test = feather.read_dataframe(
            self.upstream['split_data']['test_y_data']
        )
        train_data = pandas.concat([X_train, y_train], axis=1)
        test_data = pandas.concat([X_test, y_test], axis=1)

        if quantile_intervals and len(quantile_intervals) > 2:
            print('Only the first two quantile intervals will be included in the plots.')

        # create plots for each of the target features
        for target in self.target_features:
            display(Markdown(f'# Plots for {target} target feature'))

            # subset relevant ground truth data
            df = test_data[
                [self.group_var, self.temp_var, target]
            ].merge(
                train_data[
                    [self.group_var, self.temp_var, target]
                ],
                how='inner',
                on=[self.group_var, self.temp_var],
                suffixes=['_test', '_train']
            )
            # merge with predictions
            preds = [p.add_prefix(f'{m}_') for m, p in predictions.items()]
            df = pandas.concat([df] + preds, axis=1)

            # get min/max values to set common axis for all plots
            xmin = df[self.temp_var].min()
            xmax = df[self.temp_var].max()
            ymin = df[[f'{model}_{target}' for model in self.models]].min().min()
            ymax = df[[f'{model}_{target}' for model in self.models]].max().max()

            # create a plot for each instance of the grouping variable
            for var in df[self.group_var].unique():
                # subset data
                var_df = df.loc[df[self.group_var] == var]

                # add to figure for each model
                for c, model in enumerate(self.models):
                    # mean prediction line
                    plt.plot(
                        var_df[self.temp_var], var_df[f'{model}_{target}'], color=self.colour_map[c], label=f'{model}')
                    # quantiles
                    for l, qi in enumerate(quantile_intervals):
                        lb = min(qi)
                        ub = max(qi)
                        try:
                            plt.plot(
                                var_df[self.temp_var], var_df[f'{model}_{target}_Q{lb * 100:g}'], color=self.colour_map[c], linestyle=self.line_map[l])
                            plt.plot(
                                var_df[self.temp_var], var_df[f'{model}_{target}_Q{ub * 100:g}'], color=self.colour_map[c], linestyle=self.line_map[l])
                        except KeyError:
                            pass
                # ground truth points
                plt.scatter(var_df[self.temp_var],
                            var_df[f'{target}_test'], c='red')
                plt.scatter(var_df[self.temp_var],
                            var_df[f'{target}_train'], c='green')
                plt.xlim(xmin, xmax)
                plt.ylim(ymin, ymax)
                plt.xlabel(self.temp_var)
                plt.ylabel(target)
                plt.title(
                    f'{self.group_var}: {int(var)}, N train: {var_df[f"{target}_train"].notna().sum()}, N_test: {var_df[f"{target}_test"].notna().sum()}')
                plt.legend()
                plt.show()
