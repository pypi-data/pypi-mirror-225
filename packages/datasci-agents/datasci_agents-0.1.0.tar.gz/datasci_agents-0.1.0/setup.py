# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datasci_agents']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0',
 'ipykernel>=6.25.1,<7.0.0',
 'ipython>=8.14.0,<9.0.0',
 'jupyter-client>=8.3.0,<9.0.0',
 'litellm>=0.1.398,<0.2.0',
 'nbformat>=5.9.2,<6.0.0',
 'pandas>=2.0.3,<3.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'pyyaml>=6.0.1,<7.0.0',
 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['mymodule = datasci_agents.__main__:main']}

setup_kwargs = {
    'name': 'datasci-agents',
    'version': '0.1.0',
    'description': 'Datasci Agents',
    'long_description': '\n<p align="center">\n  <img src="media/image.jpg" height="200" alt="Datasci Agents fig"/>\n</p>\n\nData science agents are LLM-powered helpers designed to help with routine tasks around EDA, feature engineering and modelling.\n\nAlthough they are able to deliver full datasci projects on their own (and even compete on Kaggle fully autonomously), they are primarily designed as assistants relying on careful human steering.\n\n# Installation\nTODO\n\n# Kaggle integration\nComing soon!',
    'author': 'Ivan Bestvina',
    'author_email': 'ivan.bestvina@qluent.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
