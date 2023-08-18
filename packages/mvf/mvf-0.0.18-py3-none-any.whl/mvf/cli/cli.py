import click
import os
import sys
from ploomber.exceptions import DAGBuildError
from mvf.cli import utils
from mvf.dag.builder import DagBuilder
from mvf.template.config import ConfigBuilder
from mvf.template.file_gen import FileGenerator
from rpy2.rinterface_lib.callbacks import logger as rpy2_logger
import logging
rpy2_logger.setLevel(logging.ERROR)


@click.group(
    help='''
    MVF

    See the documentation: 

        https://tomkimcta.gitlab.io/model-validation-framework
    '''
)
def mvf():
    '''
    CLI entry point.
    '''
    # add working directory to PYTHONPATH to allow import of local modules
    sys.path.append(os.getcwd())


@click.command(
    help='''
        Initialise an MVF project. Default use will initialise the MVF
        project in the current working directory.
    '''
)
@click.option(
    '--directory',
    '-d',
    default='.',
    help='The directory in which to initialise the MVF project.'
)
def init(directory):
    '''
    Generates or updates an MVF configuration file.
    '''
    # check if default use
    if directory == '.':
        pth = os.getcwd()
        click.echo('Initialising MVF project in the current working directory')
    # path specified by user
    else:
        if os.path.isabs(directory):
            pth = directory
        # if relative path provided, construct absolute
        else:
            pth = os.path.join(
                os.getcwd(),
                directory
            )
        # check if the path provided by the user is already a file
        if os.path.isfile(pth):
            raise click.ClickException(
                'A file already exists at the location provided!')
        click.echo(f'Initialising MVF project in {pth}')
    # get confirmation from user
    click.confirm(f'Do you want to continue?', abort=True)
    # make project dir if not already exists
    if not os.path.exists(pth):
        os.makedirs(pth)
    # generate or update configuration file
    cfg_builder = ConfigBuilder(pth)
    cfg_builder.write()
    # print next steps
    click.echo('Next steps:\n')
    if directory != '.':
        click.secho(f'    cd {pth}', fg='green')
    click.echo('    Edit the mvf_conf.yaml file.\n')


@click.command(
    help='''
        Generate template files based on project configuration.
    '''
)
def scaffold():
    '''
    Generates template project files based on configuration.
    '''
    click.echo(f'This action will overwrite any existing source files.')
    click.confirm(f'Do you want to continue?', abort=True)
    # load project config
    config = utils.load_config(
        os.path.join(
            os.getcwd(),
            'mvf_conf.yaml'
        )
    )
    # parse specified models
    py_mods = [mod['name']
               for mod in config['models'] if mod['lang'] == 'Python']
    r_mods = [mod['name'] for mod in config['models'] if mod['lang'] == 'R']
    # generate files
    generator = FileGenerator()
    generator.gen_preprocess(config['data']['source'], config['data']['lang'])
    generator.gen_models_py(py_mods)
    generator.gen_models_r(r_mods)


@click.command(
    help='''
        Run an MVF project or process. Default use
        will trigger an incremental execution of the project.
    '''
)
@click.option(
    '--force',
    '-f',
    is_flag=True,
    default=False,
    help="Force execution of whole workflow."
)
@click.option(
    '--output',
    '-o',
    default='output',
    help='Specify the output directory.'
)
@click.option(
    '--process',
    '-p',
    default=None,
    help='Force execution of a specific process by name.'
)
def run(force, output, process):
    '''
    Runs an MVF project or process.
    '''
    # load project config
    config = utils.load_config(
        os.path.join(
            os.getcwd(),
            'mvf_conf.yaml'
        )
    )
    # build dag from config
    click.echo('Building MVF project workflow...')
    dag_builder = DagBuilder(config, output_dir=output)
    dag_builder.build()
    try:
        if process is None:
            # access the built dag and execute it
            click.echo('Running MVF project...')
            dag_builder.dag.build(force=force)
        else:
            # access a process and execute it
            dag_process = dag_builder.dag.get(process)
            dag_builder.dag.render(force=force)
            if dag_process is None:
                click.echo(f'No process named {process}')
                click.echo(f'The existing processes are {[k for k in dag_builder.dag.keys()]}')
            else:
                click.echo(f'Running {process} process...')
                dag_process.build(force=True)
    except DAGBuildError as e:
        click.echo(e)
    finally:
        # plot the dag
        click.echo('Plotting workflow...')
        dag_builder.dag.plot('project_workflow.html')


@click.command(
    help='''
        Plot an MVF workflow. If saving outputs to a
        custom directory, this directory should be passed as an
        option to get up-to-date process statuses.
    '''
)
@click.option(
    '--output',
    '-o',
    default='output',
    help='Specify the output directory.'
)
def plot(output):
    '''
    Plots an MVF workflow.
    '''
    # load project config
    config = utils.load_config(
        os.path.join(
            os.getcwd(),
            'mvf_conf.yaml'
        )
    )
    # build dag from config
    dag_builder = DagBuilder(config, output_dir=output)
    dag_builder.build()
    click.echo('Plotting workflow...')
    # access the built dag and plot it
    dag_builder.dag.plot('project_workflow.html')


@click.command(
    help='''
        Try out an example project.
    '''
)
@click.option(
    '--list',
    '-l',
    is_flag=True,
    default=False,
    help='List the available projects.'
)
@click.option(
    '--name',
    '-n',
    default=None,
    help='Name of project to download.'
)
@click.option(
    '--output',
    '-o',
    default=None,
    help='Target directory.'
)
def examples(list, name, output):
    '''
    Downloads an example project.
    '''
    # use this list to manage which examples to expose
    examples_list = [
        'feature_scaling',
        'py_preprocess_train_test',
        'r_preprocess_kfold'
    ]
    if list:
        # list the examples in the console
        click.echo('The available examples are\n')
        for example_name in examples_list:
            click.echo(f'    {example_name}')
        click.echo('\nDownload them using `mvf examples -n name_of_project`')
    elif name is None:
        # print help text
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
    else:
        # try download the example called name
        if name in examples_list:
            click.echo(f'Downloading {name} project...')
            # download the example
            output_dir = output if output is not None else name
            utils.download_example(name, output_dir)
            # print next steps
            click.echo('Next steps:\n')
            click.secho(f'    cd {output_dir}\n    mvf run\n', fg='green')
        else:
            click.echo(
                f'There is no project named {name}. Check the available projects with\n\n    mvf examples -l\n')


# add commands to group
mvf.add_command(init)
mvf.add_command(scaffold)
mvf.add_command(run)
mvf.add_command(plot)
mvf.add_command(examples)
