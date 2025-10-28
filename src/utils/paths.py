from pathlib import Path
import yaml

def get_base_dir(format='Path'):
    base_dir = Path(__file__).resolve().parents[2]

    if base_dir.name != 'SigmaRank':
        raise RuntimeError('Please run from SigmaRank root directory!')
    elif format == 'Path':
        return base_dir
    elif format == 'str':
        return str( base_dir )

def get_data_dir(format='Path'):
    data_dir = get_base_dir() / 'data'

    if format == 'Path':
        return data_dir
    elif format == 'str':
        return str( data_dir )

def get_config_dir(format='Path'):
    config_dir = get_base_dir() / 'config'

    if format == 'Path':
        return config_dir
    elif format == 'str':
        return str( config_dir )

def get_scripts_dir(format='Path'):
    scripts_dir = get_base_dir() / 'scripts'

    if format == 'Path':
        return scripts_dir
    elif format == 'str':
        return str( scripts_dir )

def get_tests_dir(format='Path'):
    tests_dir = get_base_dir() / 'tests'

    if format == 'Path':
        return tests_dir
    elif format == 'str':
        return str( tests_dir )

def get_yaml_path(format='Path'):
    yaml_path = get_config_dir() / 'base.yaml'

    if format == 'Path':
        return yaml_path
    elif format == 'str':
        return str( yaml_path )
    
def get_yaml():
    YAML_PATH_STR = get_yaml_path(format="str")

    with open(YAML_PATH_STR) as f:
        return yaml.safe_load(f)