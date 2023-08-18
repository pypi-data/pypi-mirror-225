# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faker_security']

package_data = \
{'': ['*']}

install_requires = \
['faker>=8.2.1']

setup_kwargs = {
    'name': 'faker-security',
    'version': '0.4.0',
    'description': 'Faker provider for security related data',
    'long_description': "# Faker-Security\n\n[![Pypi](https://badge.fury.io/py/faker-security.svg)](https://pypi.org/project/faker-security/)\n[![CircleCI](https://circleci.com/gh/snyk/faker-security/tree/main.svg?style=svg)](https://circleci.com/gh/snyk/faker-security/tree/main)\n\nProvider for [Faker](https://github.com/joke2k/faker)\nto generate random/fake data related to security.\n\n## Requirements\n\n- Faker\n- Python 3.8+\n\n## Installation and Usage\n\nIf you want to use `faker-security` within your project, add it to your dependency file of choice.\n\nThis is typically your project's `requirements.txt` file. If you are using a higher-level package manager like `poetry` or `pipenv`, follow their instructions for adding new packages.\n\nOnce installed, you need to setup `Faker` to make use of the `SecurityProvider`. An example of how that could be done is shown below:\n\n```python\nfrom faker import Faker\nfrom faker_security.providers import SecurityProvider\n\nfake = Faker()\nfake.add_provider(SecurityProvider)\n\n# generate a CVSSv3 vector\nfake.cvss3()\n```\n\n## Provider Features\n\n- `cvss3`: generates a CVSS v3 vector\n- `cvss2`: generates a CVSS v2 vector\n- `ccss`: generates a CCSS vector\n- `version`: generates a [semver version number](https://semver.org/)\n- `npm_semver_range`: generates a [npm compatible semver version range](https://docs.npmjs.com/about-semantic-versioning)\n- `cwe`: generates a CWE identifier\n- `cve`: generates a CVE identifier\n\n## Developing\n\n- Install `poetry` and run `poetry install`\n- Install `pre-commit` and run `pre-commit install --install-hooks`\n\n## Testing\n\n`poetry run pytest` to run tests.\n",
    'author': 'Snyk Security R&D',
    'author_email': 'security-engineering@snyk.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/snyk/faker-security',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
