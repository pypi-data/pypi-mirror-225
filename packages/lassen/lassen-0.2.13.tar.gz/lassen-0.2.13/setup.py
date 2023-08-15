# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lassen',
 'lassen.alembic',
 'lassen.assets',
 'lassen.core',
 'lassen.datasets',
 'lassen.db',
 'lassen.stubs',
 'lassen.stubs.generators',
 'lassen.stubs.templates',
 'lassen.tests',
 'lassen.tests.datasets',
 'lassen.tests.fixtures',
 'lassen.tests.fixtures.stubs',
 'lassen.tests.fixtures.test_harness.test_harness',
 'lassen.tests.fixtures.test_harness.test_harness.migrations',
 'lassen.tests.stubs',
 'lassen.tests.stubs.generators']

package_data = \
{'': ['*'], 'lassen.tests.fixtures': ['test_harness/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'alembic-autogenerate-enums>=0.1.1,<0.2.0',
 'alembic>=1.11.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'fastapi>=0.99.0,<0.100.0',
 'inflection>=0.5.1,<0.6.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0']

extras_require = \
{'database': ['SQLAlchemy>=2.0.15,<3.0.0', 'psycopg2>=2.9.6,<3.0.0'],
 'datasets': ['datasets>=2.13.0,<3.0.0',
              'numpy>=1.24.3,<2.0.0',
              'pandas>=2.0.2,<3.0.0']}

entry_points = \
{'console_scripts': ['generate-lassen = lassen.stubs.generate:cli',
                     'migrate = lassen.alembic.cli:main']}

setup_kwargs = {
    'name': 'lassen',
    'version': '0.2.13',
    'description': 'Common webapp scaffolding.',
    'long_description': '# lassen\n\n**40.4881° N, 121.5049° W**\n\nCore utilities for MonkeySee web applications.\n\nNot guaranteed to be backwards compatible, use at your own risk.\n\n## Structure\n\n**Stores:** Each datamodel is expected to have its own store. Base classes that provide standard logic are provided by `lassen.store`\n- StoreBase: Base class for all stores\n- StoreFilterMixin: Mixin for filtering stores that specify an additional schema to use to filter\n\n**Schemas:** Each datamodel should define a Model class (SQLAlchemy base object) and a series of Schema objects (Pydantic) that allow the Store to serialize the models. These schemas are also often used for direct CRUD referencing in the API layer.\n\nWe use a base `Stub` file to generate these schemas from a centralized definition. When defining generators you should use a path that can be fully managed by lassen, since we will remove and regenerate these files on each run.\n\n```python\nSTORE_GENERATOR = StoreGenerator("models/auto")\nSCHEMA_GENERATOR = SchemaGenerator("schemas/auto")\n```\n\n```bash\npoetry run generate-lassen\n```\n\n**Datasets:** Optional huggingface `datasets` processing utilities. Only installed under the `lassen[datasets]` extra. These provide support for:\n\n- batch_to_examples: Iterate and manipulate each example separately, versus over nested key-based lists.\n- examples_to_batch: Takes the output of a typehinted element-wise batch and converts into the format needed for dataset insertion. If datasets can\'t automatically interpret the type of the fields, also provide automatic casting based on the typehinted dataclass.\n\n```python\nfrom lassen.datasets import batch_to_examples, examples_to_batch\nimport pandas as pd\n\n@dataclass\nclass BatchInsertion:\n    texts: list[str]\n\ndef batch_process(examples):\n    new_examples : list[BatchInsertion] = []\n    for example in batch_to_examples(examples):\n        new_examples.append(\n            BatchInsertion(\n                example["raw_text"].split()\n            )\n        )\n\n    # datasets won\'t be able to typehint a dataset that starts with an empty example, so we use our explicit schema to cast the data\n    return examples_to_batch(new_examples, BatchInsertion, explicit_schema=True)\n\ndf = pd.DataFrame(\n    [\n        {"raw_text": ""},\n        {"raw_text": "This is a test"},\n        {"raw_text": "This is another test"},\n    ]\n)\n\ndataset = Dataset.from_pandas(df)\n\ndataset = dataset.map(\n    batch_process,\n    batched=True,\n    batch_size=1,\n    num_proc=1,\n    remove_columns=dataset.column_names,\n)\n```\n\n**Migrations:** Lassen includes a templated alembic.init and env.py file. Client applications just need to have a `migrations` folder within their project root. After this you can swap `poetry run alembic` with `poetry run migrate`.\n\n```sh\npoetry run migrate upgrade head\n```\n\n**Settings:** Application settings should subclass our core settings. This provides a standard way to load settings from environment variables and includes common database keys.\n\n```python\nfrom lassen.core.config import CoreSettings, register_settings\n\n@register_settings\nclass ClientSettings(CoreSettings):\n    pass\n```\n\n**Schemas:** For helper schemas when returning results via API, see [lassen.schema](./lassen/schema.py).\n\n## Development\n\n```sh\npoetry install --extras "datasets"\n\ncreateuser lassen\ncreatedb -O lassen lassen_db\ncreatedb -O lassen lassen_test_db\n```\n\nUnit Tests:\n\n```sh\npoetry run pytest\n```\n',
    'author': 'Pierce Freeman',
    'author_email': 'pierce@freeman.vc',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
