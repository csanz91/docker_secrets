import os
import json

root = os.path.abspath(os.sep)

def get_docket_secrets(name, secretsPath=os.path.abspath(os.path.join(os.sep, "run", "secrets"))):
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

getDocketSecrets = get_docket_secrets
