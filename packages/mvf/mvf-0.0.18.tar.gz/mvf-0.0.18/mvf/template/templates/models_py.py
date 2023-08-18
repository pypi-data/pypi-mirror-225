# Python models file

# MVF imports
import pandas
# User imports
{% for model in models %}

class {{model}}:
    '''
    Class implementing {{model}}.
    '''

    def fit(self, X, y):
        '''
        Fit model to data.
        '''
        raise NotImplementedError

    def predict(self, X, quantiles=None):
        '''
        Predict target values (y) from new data.
        '''
        raise NotImplementedError

    def save(self, path):
        '''
        Save model.
        '''
        raise NotImplementedError

    def load(self, path):
        '''
        Load a model.
        '''
        raise NotImplementedError
{% endfor %}
