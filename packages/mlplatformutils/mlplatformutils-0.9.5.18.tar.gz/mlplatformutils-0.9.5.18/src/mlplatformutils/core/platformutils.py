#Defining all Utility Functions
import os
import subprocess
import configparser
from azureml.core.compute import ComputeInstance
from azureml.core.compute_target import ComputeTargetException

def is_package_installed(package_name, package_version=None):
    try:
        output = subprocess.check_output(['pip', 'show', package_name])
        output = output.decode('utf-8')
        if package_version is None:
            return True
        else:
            return f'Version: {package_version}' in output
    except subprocess.CalledProcessError:
        return False


def read_setup_ini(cwd,section_name, key_name):
    try:
        # Read the setup.ini file
        config = configparser.ConfigParser()
        config.read(os.path.join(cwd+"/core/", 'setup.ini'))
        # Get the value of the requested key
        value = config.get(section_name, key_name)
        return value
    except FileNotFoundError:
        print(f"Error: setup.ini file not found in '{cwd}'")
        return None
    except configparser.NoSectionError:
        print(f"Error: section '{section_name}' not found in setup.ini")
        return None
    except configparser.NoOptionError:
        print(f"Error: key '{key_name}' not found in section '{section_name}' in setup.ini")
        return None

def assert_amlcompute(workspace, compute_name):
    try:
        compute_instance = ComputeInstance(workspace=workspace, name=compute_name)
        print(f"Found existing compute instance: {compute_name}")
    except ComputeTargetException:
        print(f"Not Found compute instance: {compute_name}")

def get_environment(env_yaml_file_path):
    import yaml
    with open(env_yaml_file_path) as f:
        env_yaml = yaml.safe_load(f)

    for env, value in env_yaml['Environment'].items():
        if value == 1:
            return env

    raise ValueError('No environment variable has a value of 1')

def set_environment(env_yaml):
    if env_yaml=="DEV_ENV":
        set_environment_params="DEV_PARAMS"
        set_environment_var="DEV_ENV_VARS"
    elif env_yaml=="PROD_ENV":
        set_environment_params="PROD_PARAMS"
        set_environment_var="PROD_ENV_VARS"
    elif env_yaml=="PPE_ENV":
        set_environment_params="PPE_PARAMS"
        set_environment_var="PPE_ENV_VARS"
    return set_environment_params,set_environment_var
    raise ValueError('Incorrect Environment Variable Supplied!')


def install_pip(package_name):
    for pkg in package_name:
        try:
            if not is_package_installed(pkg, None):
                subprocess.check_call(["pip", "install", pkg])
                print(f"Successfully installed {pkg}!")
            else:
                print(f"{pkg} is already installed.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {pkg}.")
    return

def upgrade_pip(package_name):
    for pkg in package_name:
        try:
            subprocess.check_call(["pip", "install","--upgrade", pkg])
            print(f"Successfully upgraded and installed {pkg}!")
        except subprocess.CalledProcessError:
            print(f"Failed to install {pkg}.")
    return
