import yaml
import os


class ConfigBuilder:
    '''
    Generator for MVF configuration file.
    If a file already exists, user changes will not be overwritten.
    '''
    # template configuration
    config = {
        'data': {
            'source': 'path_to_your_source_code',
            'lang': 'Python',
            'split': 'train_test',
            'test_size': 0.3,
            'input_features': [],
            'target_features': []
        },
        'models': [
            {
                'name': 'your_model_name',
                'lang': 'Python',
            },
        ],
    }

    def __init__(self, pth):
        '''
        Initialise the builder with template config.
        Updates with any existing config.
        '''
        # construct path to config file
        self.config_path = os.path.join(
            pth,
            'mvf_conf.yaml',
        )
        # load any existing config
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                existing_config = yaml.safe_load(f)
            self.config.update(existing_config)

    def write(self):
        '''
        Write config to file.
        '''
        with open(self.config_path, 'w') as f:
            yaml.safe_dump(self.config, f, default_flow_style=False, sort_keys=False)
