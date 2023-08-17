import click
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from swagern.tavern_utils.fuzzy_matching import fuzzy_api_blueprint_matching

DEFAULT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'template', 'tavern_template_default.yaml')
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'tests')
DEFAULT_MAPPER_FILE = os.path.join(os.path.dirname(__file__), 'mappers', 'mapper.yaml')

def load_mapper_variables(mapper_file_path):
    with open(mapper_file_path, 'r') as file:
        mapper_data = yaml.safe_load(file)
    return mapper_data['variables']

def map_swagger_to_tavern(testsuite_path, tavern_template, output_directory, mapper_file):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    template_path = os.path.join(current_dir, tavern_template)

    with open(mapper_file, 'r') as stream:
        try:
            variables = yaml.safe_load(stream)['variables']
        except yaml.YAMLError:
            variables = {}

    env = Environment(
        loader=FileSystemLoader(os.path.dirname(template_path)),
        autoescape=select_autoescape(['yaml'])
    )
    template = env.get_template(os.path.basename(template_path))
    test_suite_name, fuzzy_matching_output, test_data = fuzzy_api_blueprint_matching(testsuite_path)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    tavern_tests = {}
    for test_case, apis_list in fuzzy_matching_output.items():
        if test_case not in tavern_tests:
            tavern_tests[test_case] = []
        for api_details in apis_list:
            for endpoint, details in api_details.items():
                for method, method_details in details.items():
                    stage_name = method_details['operationId']
                    request_url = endpoint
                    request_method = method.upper()
                    required_request_params = {}
                    optional_request_params = {}
                    response_status_code = '200' if 'responses' in method_details and '200' in method_details['responses'] else None

                    if 'parameters' in method_details:
                        for param in method_details['parameters']:
                            param_name = param['name']
                            required = param['required']
                            templated_value = f'[{param_name}]' if param_name not in variables else (
                                f"{{{variables[param_name].strip('{}')}}}" if ':' not in variables[param_name] else
                                f"{{{variables[param_name].strip('{}').split(':')[0]}}}"
                            )

                            if required:
                                required_request_params[param_name] = templated_value
                            else:
                                optional_request_params[param_name] = templated_value

                    stage = {
                        'name': stage_name,
                        'request': {
                            'url': request_url,
                            'method': request_method,
                            'params': required_request_params,
                            'optional_params': optional_request_params
                        },
                        'response': {
                            'status_code': response_status_code
                        }
                    }

                    if endpoint in test_data:
                        if 'save' in test_data[endpoint]:
                            stage['response']['save'] = {'json': test_data[endpoint]['save']}
                        if 'verify' in test_data[endpoint]:
                            stage['response']['json'] = test_data[endpoint]['verify']

                    tavern_tests[test_case].append(stage)

    file_path = os.path.join(output_directory, f"test_{test_suite_name}.tavern.yaml")
    try:
        with open(file_path, 'w') as file:
            for test_name, stages in tavern_tests.items():
                tavern_test = template.render(test_name=test_name, stages=stages, variables=variables)
                file.write(tavern_test)
                file.write('\n')
        print(f"File successfully created at: {file_path}")
    except Exception as e:
        print(f"Failed to create file. Error: {e}")

@click.command()
@click.option('--tavern-template', default=DEFAULT_TEMPLATE_PATH, help='Path to the tavern template.')
@click.option('--output-directory', default=DEFAULT_OUTPUT_DIR, help='Path to the output directory.')
@click.option('--mapper-file', default=DEFAULT_MAPPER_FILE, help='Path to the mapper file.')
def generate_command(testsuite_path, tavern_template, output_directory, mapper_file):
    test_suite_name, fuzzy_matching_output, test_data = fuzzy_api_blueprint_matching(testsuite_path)
    map_swagger_to_tavern(test_data, tavern_template, output_directory, mapper_file)

if __name__ == "__main__":
    generate_command()
