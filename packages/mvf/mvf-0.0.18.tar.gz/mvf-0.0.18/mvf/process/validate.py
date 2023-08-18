# # Comparative Model Validation

# imports
from mvf.process import validation

# + tags=["parameters"]
upstream = None
product = None
models = []
split_type = ''
n_folds = 10
quantile_intervals = []
target_features = []
grouping_variable = None
temporal_variable = None
# -

# format variable
upstream = dict(upstream)

# ## Load predictions and validation data

# load validation data data from upstream
validation_data = validation.load_validation_data(
    upstream,
    split_type,
    n_folds
)

# load predictions from upstream
predictions = validation.load_predictions(
    upstream,
    models
)

# ## Error Metrics
# The error metrics reported are
# * MSE - Mean squared error
# * RMSE - Root mean squared error
# * MAE - Mean absolute error
# * MAPE - Mean absolute percentage error
# * R-squared - Coefficient of determination

validation.error_metrics(
    target_features,
    predictions,
    validation_data
)

# ## Quantile interval coverage
# For each of the intervals defined in `quantile_intervals`, what proportion of predicted values fall within the interval?

validation.qi_coverage(
    validation_data,
    target_features,
    predictions,
    quantile_intervals
)

# ## Model Sharpness
# How uncertain is the model? `sharpness` of a quantile interval is defined as the average width of the interval across all predictions.

validation.qi_sharpness(
    target_features, 
    predictions, 
    quantile_intervals
)

# ## Computational performance
# Record
# * the total size in bytes of the fit model(s).
# * the total time taken to fit the model(s).
# * the total time taken for the model(s) to predict.

validation.computational_performance(
    upstream,
    models,
    split_type,
    n_folds
)

# ## Plots

validation.Plot(
    models, 
    target_features, 
    validation_data, 
    upstream, 
    split_type
).plot(
    predictions,
    grouping_variable,
    quantile_intervals,
    temporal_variable
)