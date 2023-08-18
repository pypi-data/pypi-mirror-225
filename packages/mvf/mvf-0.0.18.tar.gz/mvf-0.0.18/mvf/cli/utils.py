import click
import os
import distutils.dir_util
import subprocess
import yaml
from mvf.integration import mvf_config


def load_config(path):
    '''
    Loads the mvf_conf.yaml from the working directory 
    and validates the config against the schema.
    '''
    # open the mvf config file
    try:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        raise Exception('No `mvf_conf.yaml` found in the working directory.')
    else:
        # validate the config against the schema
        click.echo('Validating config...')
        mvf_config.check_config(config)
        return config


def download_example(example_name, output_dir):
    '''
    Downloads an example MVF project.
    '''
    branch = 'main'
    url = 'https://gitlab.com/TomKimCTA/model-validation-framework'
    example_path = f'test/test_resources/test_{example_name}'
    # check target directory does not already exist
    if os.path.isdir(output_dir):
        raise Exception(f'{output_dir} is already a directory.')
    # create sparse repository
    subprocess.run(
        [
            'git',
            'clone',
            '-n',
            '--depth',
            '1',
            '-b',
            branch,
            '--filter=blob:none',
            url,
            output_dir
        ]
    )
    os.chdir(output_dir)
    # set which subfolder to checkout
    subprocess.run(
        [
            'git',
            'sparse-checkout',
            'set',
            example_path
        ]
    )
    # checkout example
    subprocess.run(
        [
            'git',
            'checkout'
        ]
    )
    # reorganise directories
    distutils.dir_util.copy_tree(
        os.path.join(
            'test',
            'test_resources',
            f'test_{example_name}'
        ),
        os.getcwd()
    )
    # clean up directory
    distutils.dir_util.remove_tree('test')
    distutils.dir_util.remove_tree('.git')
    files_to_delete = ['README.md', 'pipeline.yaml']
    for f in files_to_delete:
        if os.path.exists(f):
            os.remove(f)
