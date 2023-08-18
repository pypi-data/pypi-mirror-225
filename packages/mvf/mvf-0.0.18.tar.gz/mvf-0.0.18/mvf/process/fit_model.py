# imports
import feather
import pandas
from mvf.process.utils import ProcessTimer, import_model_class, init_model, convert_to_r_data


def fit_model(product, upstream, lang, model_name, split_type, n_folds=10):
    '''
    Main method to fit model(s). Behaviour depends on project configuration.
    '''
    # start process timer
    timer = ProcessTimer(f'{model_name}_fit')

    # import model class
    model_module = import_model_class(lang)

    if split_type == 'train_test':
        # load training data
        X_train = feather.read_dataframe(upstream['split_data']['train_X_data'])
        y_train = feather.read_dataframe(upstream['split_data']['train_y_data'])

        # fit and save model
        fit(
            X_train,
            y_train,
            str(product['model']),
            model_module,
            lang,
            model_name
        )
    elif split_type == 'k_fold':
        # allocate memory
        X_data = []
        y_data = []
        for i in range(1, n_folds+1):
            # load data from upstream process
            X_data.append(
                feather.read_dataframe(
                    upstream['split_data'][f'fold_{i}_X_data']
                )
            )
            y_data.append(
                feather.read_dataframe(
                    upstream['split_data'][f'fold_{i}_y_data']
                )
            )
        
        # fit k models
        for i in range(1, n_folds+1):
            # get train set as all folds except i-th
            X_train = pandas.concat([x for j, x in enumerate(X_data) if j != i-1])
            y_train = pandas.concat([y for j, y in enumerate(y_data) if j != i-1])
            # fit and save model
            fit(
                X_train,
                y_train,
                str(product[f'model_{i}']),
                model_module,
                lang,
                model_name
            )
    # end process timer
    timer.end()
    # save process metadata
    timer.save(product['process_metadata'])


def fit(X_train, y_train, model_path, model_module, lang, model_name):
    '''
    Generic fit method.
    '''
    # if fitting an R model, must convert input data to R data.frame
    if lang == 'R':
        # convert pandas dataframe to R dataframe
        X_train = convert_to_r_data(X_train)
        y_train = convert_to_r_data(y_train)
    # initialise model
    model = init_model(
        model_module,
        lang,
        model_name
    )
    model.fit(X_train, y_train)
    model.save(model_path)