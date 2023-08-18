from jinja2 import Environment, PackageLoader
import os
import jupytext


class FileGenerator:
    '''
    Generator for project files.

    Each method loads and renders a Jinja template and writes
    the template to a file.
    '''

    def __init__(self):
        '''
        Configure template file location for Jinja environment.
        '''
        self.env = Environment(
            loader=PackageLoader(
                'mvf',
                os.path.join('template', 'templates')
            )
        )

    def gen_preprocess(self, path, lang='Python'):
        '''
        Generate a data preprocessing template.
        '''
        template = self.env.get_template('preprocess.py')
        rendered = template.render(
            python=True if lang == 'Python' else False
        )
        # Convert to ipynb format
        nb = jupytext.reads(rendered, fmt="py:percent")
        out = jupytext.writes(nb, 'ipynb')
        with open(path, 'w') as f:
            f.write(out)

    def gen_models_py(self, models, path='models.py'):
        '''
        Generate a template Python models file.
        '''
        if models == []:
            pass
        else:
            template = self.env.get_template('models_py.py')
            rendered = template.render(
                models=models
            )
            with open(path, 'w') as f:
                f.write(rendered)

    def gen_models_r(self, models, path='models.R'):
        '''
        Generate a template R models file.
        '''
        if models == []:
            pass
        else:
            template = self.env.get_template('models_r.py')
            rendered = template.render(
                models=models
            )
            with open(path, 'w') as f:
                f.write(rendered)
