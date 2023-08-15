# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'openapi_fal_rest': 'openapi-fal-rest/openapi_fal_rest',
 'openapi_fal_rest.api': 'openapi-fal-rest/openapi_fal_rest/api',
 'openapi_fal_rest.api.billing': 'openapi-fal-rest/openapi_fal_rest/api/billing',
 'openapi_fal_rest.api.files': 'openapi-fal-rest/openapi_fal_rest/api/files',
 'openapi_fal_rest.api.keys': 'openapi-fal-rest/openapi_fal_rest/api/keys',
 'openapi_fal_rest.api.logs': 'openapi-fal-rest/openapi_fal_rest/api/logs',
 'openapi_fal_rest.api.usage': 'openapi-fal-rest/openapi_fal_rest/api/usage',
 'openapi_fal_rest.models': 'openapi-fal-rest/openapi_fal_rest/models'}

packages = \
['fal_serverless',
 'fal_serverless.auth',
 'fal_serverless.console',
 'fal_serverless.exceptions',
 'fal_serverless.logging',
 'fal_serverless.toolkit',
 'fal_serverless.toolkit.file',
 'fal_serverless.toolkit.file.providers',
 'fal_serverless.toolkit.image',
 'openapi_fal_rest',
 'openapi_fal_rest.api',
 'openapi_fal_rest.api.billing',
 'openapi_fal_rest.api.files',
 'openapi_fal_rest.api.keys',
 'openapi_fal_rest.api.logs',
 'openapi_fal_rest.api.usage',
 'openapi_fal_rest.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.3.0',
 'auth0-python>=4.1.0,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'datadog-api-client==2.12.0',
 'dill==0.3.7',
 'grpc-interceptor>=0.15.0,<0.16.0',
 'grpcio>=1.50.0,<2.0.0',
 'httpx>=0.15.4,<0.25.0',
 'isolate-proto>=0.0.37,<0.0.38',
 'isolate[build]>=0.12.2,<1.0',
 'opentelemetry-api>=1.15.0,<2.0.0',
 'opentelemetry-sdk>=1.15.0,<2.0.0',
 'packaging>=21.3',
 'pathspec>=0.11.1,<0.12.0',
 'portalocker>=2.7.0,<3.0.0',
 'pydantic<2.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=13.3.2,<14.0.0',
 'structlog>=22.3.0,<23.0.0',
 'types-python-dateutil>=2.8.0,<3.0.0',
 'typing-extensions==4.5']

extras_require = \
{':python_version < "3.10"': ['importlib-metadata>=4.4']}

entry_points = \
{'console_scripts': ['fal-serverless = fal_serverless.cli:cli']}

setup_kwargs = {
    'name': 'fal-serverless',
    'version': '0.6.41',
    'description': 'fal Serverless is an easy-to-use Serverless Python Framework',
    'long_description': '# fal-serverless\n\nLibrary to run, serve or schedule your Python functions in the cloud with any machine type you may need.\n\nCheck out to the [docs](https://docs.fal.ai/fal-serverless/quickstart) for more details.\n\n## Generate OpenAPI client for the REST API\n\nThe recommended way is to use bop. First set the `FAL_REST` variable to the right value and then run:\n\n```sh\nbop openapi\n```\n\nInitial client was generated using\n\n```sh\ncd projects/fal_serverless\n# Notice that you can point to any environment\nopenapi-python-client generate --url https://rest.shark.fal.ai/openapi.json --meta none --config openapi_rest.config.yaml\n```\n\nAnd can be manually updated with\n\n```sh\ncd projects/fal_serverless\n# Notice that you can point to any environment\nopenapi-python-client update --url https://rest.shark.fal.ai/openapi.json --meta none --config openapi_rest.config.yaml\n```\n',
    'author': 'Features & Labels',
    'author_email': 'hello@fal.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
