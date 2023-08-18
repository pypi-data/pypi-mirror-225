import mvf.integration.config as on_render
import mvf.integration.process as on_finish
import mvf.process as process
import os
from pathlib import Path
from ploomber import DAG
from ploomber.products import File
from ploomber.tasks import PythonCallable, NotebookRunner


class DagBuilder:
    def __init__(self, config, output_dir='output') -> None:
        '''
        Assigns key parameters as attributes. Initialises the Ploomber DAG.
        '''
        self.config = config
        self.output_dir = output_dir
        # path to source code
        self.path_to_process = process.__path__[0]
        self.dag = DAG(
            # set dag name as basename of working dir
            name=os.path.basename(os.getcwd())
        )


    def build(self):
        '''
        Main method for the class.

        Builds ploomber DAG from config file.
        '''
        # build up generic tasks
        preprocess_data = self.__build_preprocess_data()
        split_data = self.__build_split_data()
        validate = self.__build_validate()
        # model tasks
        for model in self.config['models']:
            # get model params
            name = model['name']
            lang = model['lang']
            if 'validation_step' in model:
                val_step = model['validation_step']
            else:
                val_step = False
            return_quantiles = model.get('return_quantiles', False)
            # build up model tasks
            fit_model = self.__build_fit_model(name, lang)
            predict_model = self.__build_predict_model(name, lang, return_quantiles=return_quantiles)
            if val_step:
                validate_model = self.__build_validate_model(name, lang)
                # set upstream
                fit_model >> validate_model
            # set upstream
            split_data >> fit_model
            split_data >> predict_model
            fit_model >> predict_model
            fit_model >> validate
            predict_model >> validate
        # set upstream
        preprocess_data >> split_data
        split_data >> validate


    def __build_preprocess_data(self):
        '''
        Creates the preprocess_data DAG task.
        '''
        # define task
        preprocess_data = NotebookRunner(
            params={
                'input_features': self.config['data']['input_features'],
                'target_features': self.config['data']['target_features']
            },
            source=Path(
                os.path.abspath(
                    self.config['data']['source']
                )
            ),
            product={
                'nb': File(
                    os.path.join(
                        self.output_dir,
                        'notebooks',
                        self.config['data']['source']
                    ),
                ),
                'X_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'preprocess_X_data.feather'
                    ),
                ),
                'y_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'preprocess_y_data.feather'
                    ),
                ),
            },
            dag=self.dag,
            name='preprocess_data',
        )
        # hooks
        preprocess_data.on_render = on_render.preprocess_data.preprocess_data
        preprocess_data.on_finish = on_finish.preprocess_data.preprocess_data
        return preprocess_data


    def __build_split_data(self):
        '''
        Creates the split_data DAG task.
        '''
        # params
        params = {
            'split_type': self.config['data']['split']
        }
        if 'grouping_variable' in self.config['data']:
            params['grouping_variable'] = self.config['data']['grouping_variable']
            if 'temporal_split' in self.config['data']:
                params['temporal_split'] = self.config['data']['temporal_split']
        # define params based on split_type
        if self.config['data']['split'] == 'train_test':
            params['test_size'] = self.config['data']['test_size']
            product = {
                'train_X_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'train_X_data.feather'
                    ),
                ),
                'test_X_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'test_X_data.feather'
                    ),
                ),
                'train_y_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'train_y_data.feather'
                    ),
                ),
                'test_y_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        'test_y_data.feather'
                    ),
                ),
            }
        else:
            n_folds = self.config['data']['n_folds']
            params['n_folds'] = n_folds
            product = {
                f'fold_{i}_X_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        f'fold_{i}_X_data.feather'
                    ),
                )
                for i in range(1, n_folds + 1)
            }
            product_y = {
                f'fold_{i}_y_data': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        f'fold_{i}_y_data.feather'
                    ),
                )
                for i in range(1, n_folds + 1)
            }
            product.update(product_y)
        # define task
        split_data = PythonCallable(
            source=process.split_data.split_data,
            product=product,
            dag=self.dag,
            name='split_data',
            params=params,
        )
        # hooks
        split_data.on_render = on_render.split_data.split_data
        split_data.on_finish = on_finish.split_data.split_data
        return split_data
    

    def __build_fit_model(self, name, lang):
        '''
        Creates the fit DAG task for a model.
        '''
        task_name = name + '_fit'
        # params
        params = {
            'model_name': name,
            'split_type': self.config['data']['split'],
            'lang': lang,
        }
        if self.config['data']['split'] == 'k_fold':
            params['split_type'] = self.config['data']['split']
            params['n_folds'] = self.config['data']['n_folds']
            product = {
                f'model_{i}': File(
                    os.path.join(
                        self.output_dir,
                        'models',
                        task_name + f'_{i}'
                    ),
                )
                for i in range(1, self.config['data']['n_folds'] + 1)
            }
        else:
            product = {
                'model': File(
                    os.path.join(
                        self.output_dir,
                        'models',
                        task_name
                    ),
                ),
            }
        product['process_metadata'] = File(
            os.path.join(
                self.output_dir,
                '.metadata',
                f'{task_name}.metadata'
            )
        )
        # define task
        fit_model = PythonCallable(
            source=process.fit_model.fit_model,
            product=product,
            dag=self.dag,
            name=task_name,
            params=params,
        )
        # hooks
        if lang == 'Python':
            fit_model.on_render = on_render.fit_model.fit_model_py
            fit_model.on_finish = on_finish.fit_model.fit_model_py
        else:
            fit_model.on_render = on_render.fit_model.fit_model_r
            fit_model.on_finish = on_finish.fit_model.fit_model_r
        return fit_model


    def __build_predict_model(self, name, lang, return_quantiles=False):
        '''
        Creates the predict DAG task for a model.
        '''
        task_name = name + '_predict'
        # source
        source = process.predict_model.predict_model
        # params
        params = {
            'split_type': self.config['data']['split'],
            'model_name': name,
            'lang': lang,
            'target_features': self.config['data']['target_features']
        }
        if self.config['data']['split'] == 'k_fold':
            params['n_folds'] = self.config['data']['n_folds']
        if 'output' in self.config:
            if 'quantile_intervals' in self.config['output'] and return_quantiles:
                params['quantile_intervals'] = self.config['output']['quantile_intervals']
        # define task
        predict_model = PythonCallable(
            source=source,
            product={
                'predictions': File(
                    os.path.join(
                        self.output_dir,
                        'data',
                        f'{task_name}.feather'
                    ),
                ),
                'process_metadata': File(
                    os.path.join(
                        self.output_dir,
                        '.metadata',
                        f'{task_name}.metadata'
                    )
                )
            },
            dag=self.dag,
            name=task_name,
            params=params
        )
        # hooks
        if lang == 'Python':
            predict_model.on_render = on_render.predict_model.predict_model_py
        else:
            predict_model.on_render = on_render.predict_model.predict_model_r
        predict_model.on_finish = on_finish.predict_model.predict_model
        return predict_model
    

    def __build_validate_model(self, name, lang):
        '''
        Creates the validate DAG task for a model.
        '''
        task_name = name + '_validate'
        # params
        params = {
            'model_name': name,
            'split_type': self.config['data']['split'],
            'lang': lang
        }
        if self.config['data']['split'] == 'k_fold':
            params['n_folds'] = self.config['data']['n_folds']
        # define task
        validate_model = NotebookRunner(
            source=Path(
                os.path.join(
                    self.path_to_process,
                    'validate_model.py'
                )
            ),
            product={
                'nb': File(
                    os.path.join(
                        self.output_dir,
                        'notebooks',
                        task_name + '.html'
                    ),
                ),
            },
            dag=self.dag,
            name=task_name,
            params=params,
        )
        # hooks
        if lang == 'Python':
            validate_model.on_render = on_render.validate_model.validate_model_py
        else:
            validate_model.on_render = on_render.validate_model.validate_model_r
        return validate_model


    def __build_validate(self):
        '''
        Creates the common validate DAG task.
        '''
        source_path = Path(
            os.path.join(
                self.path_to_process,
                'validate.py'
            )
        )
        # params
        params = {
            'split_type': self.config['data']['split'],
            'models': [model['name'] for model in self.config['models']],
            'target_features': self.config['data']['target_features']
        }
        if self.config['data']['split'] == 'k_fold':
            params['n_folds'] = self.config['data']['n_folds']
        if 'output' in self.config:
            if 'quantile_intervals' in self.config['output']:
                params['quantile_intervals'] = self.config['output']['quantile_intervals']
        if 'temporal_split' in self.config['data']:
            params['temporal_variable'] = self.config['data']['temporal_split']['temporal_variable']
        if 'grouping_variable' in self.config['data']:
            params['grouping_variable'] = self.config['data']['grouping_variable']
        # define task
        validate = NotebookRunner(
            source=source_path,
            product={
                'nb': File(
                    os.path.join(
                        self.output_dir,
                        'notebooks',
                        'validate.ipynb'
                    ),
                ),
                'nb_html': File(
                    os.path.join(
                        self.output_dir,
                        'notebooks',
                        'validate.html'
                    ),
                ),
            },
            nb_product_key=[
                'nb',
                'nb_html'
            ],
            dag=self.dag,
            name='validate',
            params=params,
        )
        # hooks
        validate.on_render = on_render.validate.validate
        return validate
    