# R models file

# MVF imports
library(R6)
# User imports
{% for model in models %}

{{model}} <- R6Class(
    # Class implementing {{model}}.
    '{{model}}',
    public = list(
        model = NULL,
        fit = function(X, y){
            # Fit model to data.
            .NotYetImplemented()
        },
        predict = function(X, quantile_intervals){
            # Predict target values (y) from new data.
            .NotYetImplemented()
        },
        save = function(path){
            # Save model.
            .NotYetImplemented()
        },
        load = function(path){
            # Load a model.
            .NotYetImplemented()
        }
    )
)
{% endfor %}