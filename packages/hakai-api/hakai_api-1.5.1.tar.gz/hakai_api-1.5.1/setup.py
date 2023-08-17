# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hakai_api']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2023.3,<2024.0',
 'requests-oauthlib>=1.3.1,<2.0.0',
 'requests>=2.30.0,<3.0.0']

setup_kwargs = {
    'name': 'hakai-api',
    'version': '1.5.1',
    'description': 'Get Hakai database resources using http calls',
    'long_description': '# Hakai Api Python Client\n\nThis project exports a single Python class that can be used to make HTTP requests to the\nHakai API resource server.\nThe exported `Client` class extends the functionality of the\nPython [requests library](https://docs.python-requests.org/en/master/) to supply Hakai\nOAuth2 credentials with url requests.\n\n![PyPI](https://img.shields.io/pypi/v/hakai-api)   [![tests](https://github.com/HakaiInstitute/hakai-api-client-py/actions/workflows/test.yaml/badge.svg)](https://github.com/HakaiInstitute/hakai-api-client-py/actions/workflows/test.yaml)  [![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](https://opensource.org/licenses/MIT)\n\n<details>\n\n<summary>Table of Contents</summary>\n\n[Installation](#installation)\n\n[Quickstart](#quickstart)\n\n[Methods](#methods)\n\n[API endpoints](#api-endpoints)\n\n[Advanced usage](#advanced-usage)\n\n[Contributing](#contributing)\n\n</details>\n\n# Installation\n\nPython 3.8 or higher is required. Install with pip:\n\n```bash\npip install hakai-api\n```\n\n# Quickstart\n\n```python\nfrom hakai_api import Client\n\n# Get the api request client\nclient = Client()  # Follow stdout prompts to get an API token\n\n# Make a data request for chlorophyll data\nurl = \'%s/%s\' % (client.api_root, \'eims/views/output/chlorophyll?limit=50\')\nresponse = client.get(url)\n\nprint(url)  # https://hecate.hakai.org/api/eims/views/output/chlorophyll...\nprint(response.json())\n# [{\'action\': \'\', \'event_pk\': 7064, \'rn\': \'1\', \'date\': \'2012-05-17\', \'work_area\': \'CALVERT\'...\n```\n\n# Methods\n\nThis library exports a single client name `Client`. Instantiating this class produces\na `requests.Session` client from the Python requests library. The Hakai API Python\nClient inherits directly from `requests.Session` thus all methods available on that\nparent class are available. For details see\nthe [requests documentation](http://docs.python-requests.org/).\n\nThe hakai_api `Client` class also contains a property `api_root` which is useful for\nconstructing urls to access data from the API. The\nabove [Quickstart example](#quickstart) demonstrates using this property to construct a\nurl to access project names.\n\n# API endpoints\n\nFor details about the API, including available endpoints where data can be requested\nfrom, see the [Hakai API documentation](https://github.com/HakaiInstitute/hakai-api).\n\n# Advanced usage\n\nYou can specify which API to access when instantiating the Client. By default, the API\nuses `https://hecate.hakai.org/api` as the API root. It may be useful to use this\nlibrary to access a locally running API instance or to access the Goose API for testing\npurposes. If you are always going to be accessing data from a locally running API\ninstance, you are better off using the requests.py library directly since Authorization\nis not required for local requests.\n\n```python\nfrom hakai_api import Client\n\n# Get a client for a locally running API instance\nclient = Client("http://localhost:8666")\nprint(client.api_root)  # http://localhost:8666\n```\n\nYou can also pass in the credentials string retrieved from the hakai API login page\nwhile initiating the Client class.\n\n```python\nfrom hakai_api import Client\n\n# Pass a credentials token as the Client Class is initiated\nclient = Client(credentials="CREDENTIAL_TOKEN")\n```\n\nFinally, you can set credentials for the client class using the `HAKAI_API_CREDENTIALS`\nenvironment variable. This is useful for e.g. setting credentials in a docker container.\nThe value of the environment variable should be the credentials token retrieved from the\nHakai API login page.\n\n# Contributing\n\nSee [CONTRIBUTING](CONTRIBUTING.md)\n\n# License\n\nSee [LICENSE](LICENSE.md)\n',
    'author': 'Taylor Denouden',
    'author_email': 'taylor.denouden@hakai.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HakaiInstitute/hakai-api-client-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
