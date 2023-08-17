import yaml
from fuzzywuzzy import fuzz, process
import os
import pkg_resources
from yaml import safe_load

def fuzzy_api_blueprint_matching(testsuite_path, swagger_path=None):
    if swagger_path is None:
        swagger_api_path = os.path.join(os.path.dirname(__file__), '..', '..', 'swagger', 'swagger_api_file.yaml')
    else:
        swagger_api_path = swagger_path
    with open(swagger_api_path, 'r') as file:
        api_yaml_blueprint_dict = yaml.safe_load(file)

    apis_dict = api_yaml_blueprint_dict['paths']
    apis = list(apis_dict.keys())

    with open(testsuite_path, 'r') as file:
        test_suite_dict = yaml.safe_load(file)
    test_cases_dict = test_suite_dict['test_cases']

    test_data = prepare_test_data(test_cases_dict)

    request_method_mapper = {'get': ['get', 'verify', 'check'],
                             'post': ['create', 'add', 'register', 'modify', 'update', 'delete', 'remove'],
                             'put': ['modify', 'update'],
                             'patch': ['modify', 'update'],
                             'delete': ['delete', 'remove']}

    apis_extract = {}
    for test_case, test_steps in test_cases_dict.items():
        apis_extract[test_case] = []
        for test_step_dict in test_steps:
            test_step_name, test_step_api = list(test_step_dict.items())[0]
            result = process.extractOne(test_step_api, apis)
            request_method_keyword = test_step_name.split()[0].lower()
            test_step_expected_methods = list(apis_dict[result[0]].keys())
            request_method = ''

            if len(test_step_expected_methods) == 1:
                apis_extract[test_case].append({
                    result[0]: apis_dict[result[0]],
                })
            else:
                for method in test_step_expected_methods:
                    if request_method_keyword in request_method_mapper[method]:
                        request_method = method
                        break
                if request_method == '':
                    request_method = test_step_expected_methods[0]
                apis_extract[test_case].append({
                    result[0]: {request_method: apis_dict[result[0]][request_method]},
                })

    return test_suite_dict['test_suite'], apis_extract, test_data

def prepare_test_data(test_cases_dict):
    test_data = {}
    for test_case, test_steps in test_cases_dict.items():
        for test_step_dict in test_steps:
            test_step_name, test_step_api = list(test_step_dict.items())[0]
            save_value = test_step_dict.get('save')
            verify_value = test_step_dict.get('verify')

            test_data[test_step_api] = {'save': save_value, 'verify': verify_value}

    return test_data



if __name__ == "__main__":
    test_suite_name, fuzzy_matching_output, test_data = fuzzy_api_blueprint_matching()
    print(fuzzy_matching_output)
    print(test_data)