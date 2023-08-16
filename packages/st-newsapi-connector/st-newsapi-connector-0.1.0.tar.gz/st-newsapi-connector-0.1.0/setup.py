# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['st_newsapi_connector']

package_data = \
{'': ['*']}

install_requires = \
['pandas==1.5.1', 'pycountry==22.3.5', 'requests==2.31.0', 'streamlit==1.25.0']

setup_kwargs = {
    'name': 'st-newsapi-connector',
    'version': '0.1.0',
    'description': 'A Python package to query data from NewsAPI in Streamlit apps',
    'long_description': None,
    'author': 'D. Carpintero',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
