# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuzzy_multi_dict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fuzzy-multi-dict',
    'version': '0.0.6',
    'description': '`fuzzy-multi-dict` is a module that provides a hight-flexible structure for storing and accessing information by a string key.',
    'long_description': '# fuzzy-multi-dict\n\n[![Coverage Status](https://img.shields.io/badge/%20Python%20Versions-%3E%3D3.9-informational)](https://pypi.org/project/fuzzy_multi_dict/)\n[![Coverage Status](https://coveralls.io/repos/github/SemioTricks/fuzzy-multi-dict/badge.svg?branch=feature/initial)](https://coveralls.io/github/SemioTricks/fuzzy-multi-dict?branch=feature/initial)\n\n[![Coverage Status](https://img.shields.io/badge/Version-0.0.6-informational)](https://pypi.org/project/fuzzy_multi_dict/)\n[![Coverage Status](https://img.shields.io/badge/Docs-passed-green)](https://github.com/SemioTricks/fuzzy-multi-dict/tree/main/docs)\n\n**fuzzy-multi-dict** is a module that provides a hight-flexible structure for storing \nand accessing information by a string key.\n\n**Fuzzy**: access by key is carried out even if there are mistakes \n(missing/extra/incorrect character) in the string representation of the key.\n\n**Multi**: flexible functionality for updating data on an existing key.\n\n\n# Installation\n\n> pip install fuzzy_multi_dict\n\n# Quickstart\n\nModule can be used as a fast enough (due to the tree structure of data storage)\nspell-checker.\n\n```python\nimport re\nfrom fuzzy_multi_dict import FuzzyMultiDict\n\nwith open(\'big_text.txt\', \'r\') as f:\n    words = list(set(re.findall(r\'[a-z]+\', f.read().lower())))\n    \nvocab = FuzzyMultiDict(max_corrections=3)\nfor word in words:\n    vocab[word] = word\n    \nvocab[\'responsibilities\']\n# \'responsibilities\'\n\nvocab[\'espansibillities\']\n# \'responsibilities\'\n\nvocab.get(\'espansibillities\')\n# [{\'value\': \'responsibilities\',\n#   \'key\': \'responsibilities\',\n#   \'mistakes\': [{\'mistake_type\': \'missing symbol "r"\', \'position\': 0},\n#    {\'mistake_type\': \'wrong symbol "a": replaced on "o"\', \'position\': 3},\n#    {\'mistake_type\': \'extra symbol "l"\', \'position\': 10}]}]\n```\n\nIt can also be used as a flexible structure to store and access semi-structured data.\n\n```python\nfrom fuzzy_multi_dict import FuzzyMultiDict\n\ndef update_value(x, y):\n    \n    if x is None: return y\n    \n    if not isinstance(x, dict) or not isinstance(y, dict):\n        raise TypeError(f\'Invalid value type; expect dict; got {type(x)} and {type(y)}\')\n        \n    for k, v in y.items():\n        if x.get(k) is None: x[k] = v\n        elif isinstance(x[k], list):\n            if v not in x[k]: x[k].append(v)\n        elif x[k] != v: x[k] = [x[k], v]\n            \n    return x\n\nphone_book = FuzzyMultiDict(\n    max_corrections=3, \n    update_value_func=update_value\n)\n\nphone_book[\'Mom\'] = {\'phone\': \'123-4567\', \'organization\': \'family\'}\nphone_book[\'Adam\'] = {\'phone\': \'890-1234\', \'organization\': \'work\'}\nphone_book[\'Lisa\'] = {\'phone\': \'567-8901\', \'organization\': \'family\'}\nphone_book[\'Adam\'] = {\'address\': \'baker street 221b\'}\nphone_book[\'Adam\'] = {\'phone\': \'234-5678\', \'organization\': \'work\'}\n\nphone_book[\'Adam\']\n# {\'phone\': [\'890-1234\', \'234-5678\'],\n#  \'organization\': \'work\',\n#  \'address\': \'baker street 221b\'}\n```\n\nIt can also be used for indexing data and fuzzy-search.\n\n```python\nfrom fuzzy_multi_dict import FuzzyMultiDict\n\nd = FuzzyMultiDict()\n\nd["apple"] = "apple"\nd["apple red delicious"] = "apple red delicious"\nd["apple fuji"] = "apple fuji"\nd["apple granny smith"] = "apple granny smith"\nd["apple honeycrisp"] = "apple honeycrisp"\nd["apple golden delicious"] = "apple golden delicious"\nd["apple pink lady"] = "apple pink lady"\n\nd.get("apple") \n# [{\'value\': \'apple\', \'key\': \'apple\', \'correction\': [], \'leaves\': []}]\n\nd.search("apple") \n# [\'apple\', \'apple red delicious\', \'apple fuji\', \'apple granny smith\',\n#  \'apple golden delicious\', \'apple honeycrisp\', \'apple pink lady\']\n\nd.search("apl") \n# [\'apple\', \'apple red delicious\', \'apple fuji\', \'apple granny smith\', \n#  \'apple golden delicious\', \'apple honeycrisp\', \'apple pink lady\']\n\n```\n',
    'author': 'Tetiana Lytvynenko',
    'author_email': 'lytvynenkotv@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
