# Swagern

Swagern is a command-line tool that automates the process of generating API test cases from a given Swagger or other API specification files. It leverages the power of fuzzy logic to match user-defined test case descriptions with the corresponding API endpoints defined in the specification file. The output is a set of Tavern YAML files that can be directly used to run API tests.

## Features

- **Fuzzy Matching**: Swagern automatically maps user-defined test cases to API endpoints using fuzzy logic, allowing for more flexible test case definitions.
- **Customizable Output**: Specify output directories or use the default location.
- **Integration with Various API Specifications**: While initially built for Swagger files, Swagern aims to support various API specifications.
- **Environment Variable Mapping**: Use a mapper file to define and load environment variables into your tests.

## Installation

Install Swagern using pip:

```bash
pip install swagern
```
## Options

### `--input`
Path to input test cases in YAML format. This is a required parameter.

### `--output`
Path to the output directory where the Tavern test files will be generated. This is an optional parameter, and the default location is the `tests` directory in the current working directory.

### `--mapper`
Path to the mapper YAML file, used for defining and loading environment variables into your tests. 

### `--api-spec`
Path to the Swagger or other API specifications file. This is an optional parameter. If not provided, Swagern will look for a default file path.

## Usage

Use the `generate` command to create Tavern YAML files based on your input file and specifications:

```bash
swagern generate --input path/to/test_cases.yaml --output path/to/output-dir --mapper path/to/mapper-file --api-spec path/to/swagger.json
```
