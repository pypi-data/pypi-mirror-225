# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['causal_tracer', 'causal_tracer.causal_tracing', 'causal_tracer.lib']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.1,<4.0.0',
 'tqdm>=4.66.1,<5.0.0',
 'transformers>=4.28.1,<5.0.0']

setup_kwargs = {
    'name': 'causal-tracer',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Causal Tracer\n\nCausal trace plots for transformer language models\n\n## About\n\nThis library is based heavily on causal tracing code from [ROME](https://rome.baulab.info/), and package and improves on their excellent work.\n',
    'author': 'David Chanin',
    'author_email': 'chanindav@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
