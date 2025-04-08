# Docker Secrets

A simple Python module for managing Docker secrets in containerized applications.

## Features

- Retrieve individual Docker secrets
- Load all secrets into environment variables
- Selectively load specific secrets into environment variables
- Compatible with both JSON files and Docker secrets directories

## Usage

### Basic Usage

```python
from docker_secrets import get_docker_secrets

# Get a single secret
api_key = get_docker_secrets("api_key")
print(f"API Key: {api_key}")

# Load all secrets into environment variables
from docker_secrets import load_all_secrets
load_all_secrets()

# Load only specific secrets
from docker_secrets import load_selective_secrets
load_selective_secrets(["api_key", "database_password"])
```

### Custom Secrets Path

By default, the module looks for secrets in `/run/secrets` (Docker's default location), but you can specify a custom path:

```python
# Specify a custom directory
api_key = get_docker_secrets("api_key", secrets_path="/path/to/secrets")

# Or a specific JSON file
load_all_secrets(secrets_path="/path/to/secrets.json")
```

## Testing

Run the tests using:

```
python -m unittest test_docker_secrets.py
```

## License

This project is available under the MIT License.