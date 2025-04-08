import os
import json

root = os.path.abspath(os.sep)


def _get_secrets_file(
    secrets_path: str = os.path.abspath(os.path.join(os.sep, "run", "secrets")),
) -> dict[str, str]:
    """This function reads and returns the secrets from a file or directory
    
    :param secrets_path: path to either a json file with secrets or a directory containing secret files
    :returns: dictionary of secrets
    :raises IOError: if secrets_path cannot be accessed
    :raises ValueError: if the secrets JSON cannot be parsed
    """
    try:
        if os.path.isdir(secrets_path):
            list_of_files = os.listdir(secrets_path)
            if not list_of_files:
                raise IOError(f"No secret files found in directory: {secrets_path}")
            secrets_file = list_of_files[0]
            secrets_file_path = os.path.join(secrets_path, secrets_file)
        else:
            secrets_file_path = secrets_path
            
        with open(secrets_file_path) as f:
            secrets = json.load(f)
            
        return secrets
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse secrets JSON: {str(e)}")
    except IOError as e:
        raise IOError(f"Failed to read secrets file: {str(e)}")


def get_docker_secrets(
    name: str,
    secrets_path: str | None = None,
) -> str:
    """This function fetches a docker secret

    :param name: the name of the docker secret
    :param secrets_path: the directory where the secrets are stored (defaults to /run/secrets)
    :returns: docker secret value
    :raises ValueError: if the secrets cannot be parsed
    :raises IOError: if [secrets_path] cannot be opened
    :raises KeyError: if [name] not found in the secrets
    """

    secrets = _get_secrets_file(secrets_path)
    if name not in secrets:
        raise KeyError(f"Secret '{name}' not found in secrets file")
    return secrets[name]


def load_all_secrets(
    secrets_path: str = os.path.abspath(os.path.join(os.sep, "run", "secrets")),
) -> None:
    """This function loads all docker secrets into environment variables

    :param secrets_path: the directory where the secrets are stored
    :raises ValueError: if the secrets cannot be parsed
    :raises IOError: if [secrets_path] cannot be opened
    """

    secrets = _get_secrets_file(secrets_path)
    for key, value in secrets.items():
        os.environ[key] = str(value)


def load_selective_secrets(
    names: list[str],
    secrets_path: str = os.path.abspath(os.path.join(os.sep, "run", "secrets")),
) -> None:
    """This function loads selective docker secrets into environment variables

    :param names: the names of the docker secrets to load
    :param secrets_path: the directory where the secrets are stored
    :raises ValueError: if the secrets cannot be parsed
    :raises IOError: if [secrets_path] cannot be opened
    :raises KeyError: if any of the [names] not found in the secrets
    """

    secrets = _get_secrets_file(secrets_path)
    missing_secrets = [name for name in names if name not in secrets]
    if missing_secrets:
        raise KeyError(f"Secrets not found: {', '.join(missing_secrets)}")
        
    for name in names:
        os.environ[name] = str(secrets[name])


# Aliases for backward compatibility
getDockerSecrets = get_docker_secrets
