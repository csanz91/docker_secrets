import os
import json
from typing import List, Dict

root = os.path.abspath(os.sep)

def get_docket_secrets(name: str, secretsPath: str = os.path.abspath(os.path.join(os.sep, "run", "secrets"))) -> str:
    """This function fetches a docker secret

    :param name: the name of the docker secret
    :param secretsPath: the directory where the secrets are stored
    :returns: docker secret
    :raises ValueError: if the secrets cannot be parsed
    :raises IOError: if [secretsPath] cannot be opened
    :raises KeyError: if [name] nof found in the secrets

    To load the secrets from the local machine, set the environment variable LOCAL_SECRETS to a json object
    with open('../secrets', 'r') as file:
        os.environ["LOCAL_SECRETS"] = file.read()
    """

    if os.getenv('LOCAL_SECRETS'):
        secrets = json.loads(os.getenv('LOCAL_SECRETS'))
        return secrets[name]

    secretsFile = os.listdir(secretsPath)[0]
    secretsFilePath = os.path.join(secretsPath, secretsFile)

    with open(secretsFilePath) as f:
        secrets = json.load(f)
    return secrets[name]

def load_all_secrets(secretsPath: str = os.path.abspath(os.path.join(os.sep, "run", "secrets"))) -> None:
    """This function loads all docker secrets into environment variables

    :param secretsPath: the directory where the secrets are stored
    :raises ValueError: if the secrets cannot be parsed
    :raises IOError: if [secretsPath] cannot be opened
    """

    if os.getenv('LOCAL_SECRETS'):
        secrets = json.loads(os.getenv('LOCAL_SECRETS'))
    else:
        secretsFile = os.listdir(secretsPath)[0]
        secretsFilePath = os.path.join(secretsPath, secretsFile)

        with open(secretsFilePath) as f:
            secrets = json.load(f)

    for key, value in secrets.items():
        os.environ[key] = value

def load_selective_secrets(names: List[str], secretsPath: str = os.path.abspath(os.path.join(os.sep, "run", "secrets"))) -> None:
    """This function loads selective docker secrets into environment variables

    :param names: the names of the docker secrets to load
    :param secretsPath: the directory where the secrets are stored
    :raises ValueError: if the secrets cannot be parsed
    :raises IOError: if [secretsPath] cannot be opened
    :raises KeyError: if any of the [names] not found in the secrets
    """

    if os.getenv('LOCAL_SECRETS'):
        secrets = json.loads(os.getenv('LOCAL_SECRETS'))
    else:
        secretsFile = os.listdir(secretsPath)[0]
        secretsFilePath = os.path.join(secretsPath, secretsFile)

        with open(secretsFilePath) as f:
            secrets = json.load(f)

    for name in names:
        if name in secrets:
            os.environ[name] = secrets[name]
        else:
            raise KeyError(f"Secret {name} not found")

getDocketSecrets = get_docket_secrets
