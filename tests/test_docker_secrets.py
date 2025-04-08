import json
import pytest
from unittest.mock import patch, mock_open
from docker_secrets import get_docker_secrets, load_all_secrets, load_selective_secrets, _get_secrets_file
import os

@pytest.fixture(autouse=True)
def cleanup_env_vars():
    """Fixture to clean up environment variables after each test."""
    # Store initial environment
    initial_env = os.environ.copy()
    
    # Run the test
    yield
    
    # Clean up any variables added during the test
    current_env = os.environ.copy()
    for key in current_env:
        if key not in initial_env:
            del os.environ[key]
    
    # Restore any variables that were changed
    for key, value in initial_env.items():
        os.environ[key] = value

def test_get_secrets_file():
    secrets = {"my_secret": "secret_value"}
    secrets_json = json.dumps(secrets)

    with patch("builtins.open", mock_open(read_data=secrets_json)):
        with patch("os.path.isdir", return_value=False):
            result = _get_secrets_file("/path/to/secrets.json")
            assert result == secrets

def test_get_secrets_file_directory():
    secrets = {"my_secret": "secret_value"}
    secrets_json = json.dumps(secrets)

    with patch("builtins.open", mock_open(read_data=secrets_json)):
        with patch("os.path.isdir", return_value=True):
            with patch("os.listdir", return_value=["secrets.json"]):
                result = _get_secrets_file("/path/to/secrets")
                assert result == secrets

def test_get_secrets_file_empty_directory():
    with patch("os.path.isdir", return_value=True):
        with patch("os.listdir", return_value=[]):
            with pytest.raises(IOError):
                _get_secrets_file("/path/to/empty/dir")

def test_get_secrets_file_invalid_json():
    invalid_json = "{invalid_json}"

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        with patch("os.path.isdir", return_value=False):
            with pytest.raises(ValueError):
                _get_secrets_file("/path/to/invalid.json")

def test_get_docker_secrets_valid():
    secret_name = "my_secret"
    secret_value = "secret_value"
    secrets = {secret_name: secret_value}

    with patch("docker_secrets._get_secrets_file", return_value=secrets):
        result = get_docker_secrets(secret_name)
        assert result == secret_value

def test_get_docker_secrets_missing_secret():
    secret_name = "missing_secret"
    secrets = {"my_secret": "secret_value"}

    with patch("docker_secrets._get_secrets_file", return_value=secrets):
        with pytest.raises(KeyError):
            get_docker_secrets(secret_name)

def test_get_docker_secrets_io_error():
    with patch("docker_secrets._get_secrets_file", side_effect=IOError("Test IO error")):
        with pytest.raises(IOError):
            get_docker_secrets("my_secret")

def test_load_all_secrets():
    secrets = {"my_secret": "secret_value", "another_secret": "another_value"}

    with patch("docker_secrets._get_secrets_file", return_value=secrets):
        load_all_secrets()
        assert os.environ["my_secret"] == "secret_value"
        assert os.environ["another_secret"] == "another_value"

def test_load_selective_secrets():
    secrets = {"my_secret": "secret_value", "another_secret": "another_value"}

    with patch("docker_secrets._get_secrets_file", return_value=secrets):
        load_selective_secrets(["my_secret"])
        assert os.environ["my_secret"] == "secret_value"
        assert "another_secret" not in os.environ

def test_load_selective_secrets_missing():
    secrets = {"my_secret": "secret_value"}

    with patch("docker_secrets._get_secrets_file", return_value=secrets):
        with pytest.raises(KeyError):
            load_selective_secrets(["missing_secret"])
