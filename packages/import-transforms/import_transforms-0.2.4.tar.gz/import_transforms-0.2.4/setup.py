# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['import_transforms']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'import-transforms',
    'version': '0.2.4',
    'description': '',
    'long_description': '`import-transforms` is a Python library for intercepting and transforming source code at import time. The main use case is [unit-syntax](https://github.com/ahupp/unit-syntax), which modifies the Python syntax to support units of measure.\n\n# Usage\n\nTransforms are a function that takes the raw module source as input and returns the transformed source as a `str` or `ast.AST`. So for example, this transform would print the name of the module when it is imported:\n\n```python\ndef print_name(source, path):\n    return f\'print(f"{__name__}")\\n\' + source\n```\n\nTransforms are registed with a glob-style module pattern:\n\n- "foo" matches just that single module.\n- "foo.\\*" matches all sub-modules of "foo" (but not "foo" itself).\n- "\\*" will match all modules.\n\nTypically you\'ll want to register the transform in your pacakge\'s `__init__.py`, with a pattern that applies to just the sub-modules of your package, e.g:\n\n```python\nregister_package_source_transform(__name__, my_transform)\n```\n\n# Example\n\n# TODO\n\n- check/support bytecode cached files\n- how do I define a type parameter that matches a function?\n- bare module import fails check_module?\n',
    'author': 'Adam Hupp',
    'author_email': 'adam@hupp.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
