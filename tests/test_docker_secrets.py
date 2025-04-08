import json
import pytest
from unittest.mock import patch, mock_open
from docker_secrets import get_docket_secrets, load_all_secrets, load_selective_secrets
import os

def test_get_docker_secrets_valid():
    secret_name = "my_secret"
    secret_value = "secret_value"
    secrets = {secret_name: secret_value}
    secrets_json = json.dumps(secrets)

    with patch("builtins.open", mock_open(read_data=secrets_json)):
        with patch("os.listdir", return_value=["secrets.json"]):
            result = get_docket_secrets(secret_name)
            assert result == secret_value

def test_get_docker_secrets_missing_secret():
    secret_name = "missing_secret"
    secrets = {"my_secret": "secret_value"}
    secrets_json = json.dumps(secrets)

    with patch("builtins.open", mock_open(read_data=secrets_json)):
        with patch("os.listdir", return_value=["secrets.json"]):
            with pytest.raises(KeyError):
                get_docket_secrets(secret_name)

def test_get_docker_secrets_invalid_json():
    invalid_json = "{invalid_json}"

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        with patch("os.listdir", return_value=["secrets.json"]):
            with pytest.raises(ValueError):
                get_docket_secrets("my_secret")

def test_get_docker_secrets_io_error():
    with patch("os.listdir", side_effect=IOError):
        with pytest.raises(IOError):
            get_docket_secrets("my_secret")

def test_get_docker_secrets_local_env():
    secret_name = "my_secret"
    secret_value = "secret_value"
    secrets = {secret_name: secret_value}
    secrets_json = json.dumps(secrets)

    with patch.dict("os.environ", {"LOCAL_SECRETS": secrets_json}):
        result = get_docket_secrets(secret_name)
        assert result == secret_value

def test_load_all_secrets():
    secrets = {"my_secret": "secret_value", "another_secret": "another_value"}
    secrets_json = json.dumps(secrets)

    with patch("builtins.open", mock_open(read_data=secrets_json)):
        with patch("os.listdir", return_value=["secrets.json"]):
            load_all_secrets()
            assert os.environ["my_secret"] == "secret_value"
            assert os.environ["another_secret"] == "another_value"

def test_load_selective_secrets():
    secrets = {"my_secret": "secret_value", "another_secret": "another_value"}
    secrets_json = json.dumps(secrets)

    with patch("builtins.open", mock_open(read_data=secrets_json)):
        with patch("os.listdir", return_value=["secrets.json"]):
            load_selective_secrets(["my_secret"])
            assert os.environ["my_secret"] == "secret_value"
            assert "another_secret" not in os.environ
