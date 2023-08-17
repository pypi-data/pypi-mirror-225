# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macrometa_target_collection']

package_data = \
{'': ['*']}

install_requires = \
['adjust-precision-for-schema==0.3.4',
 'c8connector>=0.0.31',
 'pipelinewise-singer-python==1.2.0',
 'prometheus-client==0.16.0',
 'pyc8==1.0.1']

entry_points = \
{'console_scripts': ['macrometa-target-collection = '
                     'macrometa_target_collection.main:main']}

setup_kwargs = {
    'name': 'macrometa-target-collection',
    'version': '1.0.1',
    'description': 'Singer.io target for writing to Macrometa GDN collections',
    'long_description': '# macrometa-target-collection\n\nA [Singer](https://singer.io) target that writes data to ([GDN Collections](https://macrometa.com/docs/c8ql/)).\n\n## How to use it\n\n`macrometa_target_collection` works together with any other [Singer Tap] to move data from sources like [Braintree], [Freshdesk] and [Hubspot] to JSONL formatted files.\n',
    'author': 'Macrometa',
    'author_email': 'info@macrometa.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
