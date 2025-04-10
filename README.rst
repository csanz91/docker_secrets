Docker Secrets
==============

This package provides utilities for managing Docker secrets in your applications.

Installation
------------

To install the package, use pip:

.. code-block:: bash

    pip install pip@git+https://github.com/csanz91/docker_secrets

Usage
-----

To use the package, import it in your Python code:

.. code-block:: python

    from docker_secrets import get_docket_secrets, load_all_secrets, load_selective_secrets

    secret_value = get_docket_secrets('my_secret')

    # Load all secrets into environment variables
    load_all_secrets()

    # Load selective secrets into environment variables
    load_selective_secrets(['my_secret', 'another_secret'])

Contributing
------------

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

License
-------

This project is licensed under the MIT License. See the LICENSE file for details.
