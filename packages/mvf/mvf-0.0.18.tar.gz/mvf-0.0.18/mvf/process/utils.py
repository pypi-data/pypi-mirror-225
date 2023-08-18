import timeit
import pickle


class ProcessTimer:
    '''
    Timer for DAG processes.
    '''
    def __init__(self, process_name):
        '''
        Start the timer.
        '''
        self.process_name = process_name
        self.start = timeit.default_timer()

    def end(self):
        '''
        End the timer.
        '''
        self.end = timeit.default_timer()

    def save(self, path):
        '''
        Save process metadata.
        '''
        self.process_time = {
            self.process_name: self.end - self.start
        }
        with open(path, 'wb') as f:
            pickle.dump(self.process_time, f, protocol=pickle.HIGHEST_PROTOCOL)


def import_model_class(lang):
    '''
    Import model module depending on language parameter.
    '''
    if lang == 'Python':
        import models
        return models
    elif lang == 'R':
        import rpy2.robjects as robjects
        import rpy2_r6.r6b as r6b

        r = robjects.r
        r['source']('models.R')

        return {
            'r6b': r6b,
            'r': r
        }


def init_model(model_module, lang, model_name):
    '''
    Instantiate a model.
    '''
    if lang == 'Python':
        model_class = getattr(model_module, model_name)
        model = model_class()
    elif lang == 'R':
        r6b = model_module['r6b']
        r = model_module['r']
        model_class = r6b.R6DynamicClassGenerator(r[model_name])
        model = model_class.new()
    return model


def convert_to_r_data(data):
    '''
    Convert pandas.DataFrame to R data for use by rpy2.
    '''
    from rpy2.robjects import pandas2ri
    import rpy2.robjects as robjects
    with (robjects.default_converter + pandas2ri.converter).context():
        r_data = robjects.conversion.get_conversion().py2rpy(
            data
        )
    return r_data


def convert_to_pandas_data(data):
    '''
    Convert R data from rpy2 to pandas.DataFrame.
    '''
    from rpy2.robjects import pandas2ri
    import rpy2.robjects as robjects
    with (robjects.default_converter + pandas2ri.converter).context():
        pandas_data = robjects.conversion.get_conversion().rpy2py(data)
    return pandas_data