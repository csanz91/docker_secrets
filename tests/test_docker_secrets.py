import json
import pytest
from unittest.mock import patch, mock_open
from docker_secrets import getDocketSecrets

def test_get_docker_secrets_valid():
    secret_name = "my_secret"
    secret_value = "secret_value"
    secrets = {secret_name: secret_value}
    secrets_json = json.dumps(secrets)

    with patch("builtins.open", mock_open(read_data=secrets_json)):
        with patch("os.listdir", return_value=["secrets.json"]):
            result = getDocketSecrets(secret_name)
            assert result == secret_value

def test_get_docker_secrets_missing_secret():
    secret_name = "missing_secret"
    secrets = {"my_secret": "secret_value"}
    secrets_json = json.dumps(secrets)

    with patch("builtins.open", mock_open(read_data=secrets_json)):
        with patch("os.listdir", return_value=["secrets.json"]):
            with pytest.raises(KeyError):
                getDocketSecrets(secret_name)

def test_get_docker_secrets_invalid_json():
    invalid_json = "{invalid_json}"

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        with patch("os.listdir", return_value=["secrets.json"]):
            with pytest.raises(ValueError):
                getDocketSecrets("my_secret")

def test_get_docker_secrets_io_error():
    with patch("os.listdir", side_effect=IOError):
        with pytest.raises(IOError):
            getDocketSecrets("my_secret")
