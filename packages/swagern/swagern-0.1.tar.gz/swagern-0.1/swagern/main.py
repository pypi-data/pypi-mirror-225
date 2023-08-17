import sys
import os
import click
import yaml
from pkg_resources import resource_filename

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_dir)

from swagern.tavern_utils.template_engine import map_swagger_to_tavern, load_mapper_variables
from swagern.tavern_utils.fuzzy_matching import fuzzy_api_blueprint_matching

def print_custom_help(ctx, param, value):
    if value and not ctx.resilient_parsing:
        click.echo('Swagern CLI tool to generate tests.\n\n'
                   'Usage:\n'
                   '    generate --input INPUT [--output OUTPUT] [--mapper MAPPER] [--api-spec API_SPEC]\n'
                   '    Use the "generate" command to create tests from a given YAML input file.\n')
        ctx.exit()

@click.group()
@click.option('--help', '-h', is_flag=True, callback=print_custom_help, expose_value=False, is_eager=True, help='Show custom help message and exit.')
def cli():
    """Swagern CLI tool."""
    pass


@click.command(name='generate')
@click.option('--input', required=True, help='Path to input test cases YAML.')
@click.option('--output', default=None, help='Path to the output directory.')
@click.option('--mapper', default= '/mappers/mapper.yaml', help='Path to the mapper YAML.')
@click.option('--api-spec', default='/swagger/swagger_api_file.yaml', help='Path to the API specification/documentation.') # needs to be hardcoded
def generate_command(input, output, mapper, api_spec):
    testsuite_path = input
    test_suite_name, fuzzy_matching_output, test_data = fuzzy_api_blueprint_matching(testsuite_path, api_spec)
    tavern_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates',
                                                'tavern_template_default.yaml')

    if not output:
        output = os.path.join(os.getcwd(), 'tests')
        if not os.path.exists(output):
            os.makedirs(output)

    if mapper:
        mapper_variables = load_mapper_variables(mapper)
    else:
        mapper_variables = {}

    map_swagger_to_tavern(testsuite_path, tavern_template, output, mapper)


cli.add_command(generate_command)
if __name__ == "__main__":
    cli()
