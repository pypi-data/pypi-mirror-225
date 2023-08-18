# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geobench',
 'geobench.benchmark',
 'geobench.benchmark.dataset_converters',
 'geobench.io',
 'geobench.torch_toolbox']

package_data = \
{'': ['*'], 'geobench.benchmark.dataset_converters': ['geolifeclef_scripts/*']}

install_requires = \
['h5py>=3.8.0,<4.0.0',
 'ipykernel>=6.15.2,<7.0.0',
 'ipyleaflet>=0.17.1,<0.18.0',
 'ipyplot>=1.1.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pre-commit>=3.0.4,<4.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'seaborn>=0.12.0,<0.13.0',
 'segmentation-models-pytorch==0.3.3',
 'torch>=1.12.0',
 'torchmetrics==0.11.1',
 'torchvision==0.13.0',
 'wandb>=0.13.10,<0.14.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['geobench-expgen = '
                     'geobench.experiment.experiment_generator:start',
                     'geobench-sweep-trainer = '
                     'geobench.torch_toolbox.sweep_trainer:start',
                     'geobench-toolkit = toolkit.dispatch_toolkit:start',
                     'geobench-trainer = geobench.torch_toolbox.trainer:start']}

setup_kwargs = {
    'name': 'geo-benchmark',
    'version': '0.0.0',
    'description': 'A benchmark designed to advance foundation models for Earth monitoring, tailored for remote sensing. It encompasses six classification and six segmentation tasks, curated for precision and model evaluation. The package also features a comprehensive evaluation methodology and showcases results from 20 established baseline models.',
    'long_description': '# GEO-Bench: Toward Foundation Models for Earth Monitoring\n\nGeoBench is a [ServiceNow Research](https://www.servicenow.com/research) project.\n \n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Language: Python](https://img.shields.io/badge/language-Python%203.7%2B-green?logo=python&logoColor=green)](https://www.python.org)\n\n<img src="https://github.com/ServiceNow/geo-bench/raw/main/banner.png" />\n\n> Recent progress in self-supervision has shown that pre-training large neural networks on vast amounts of unsupervised data can lead to substantial increases in generalization to downstream tasks. Such models, recently coined foundation models, have been transformational to the field of natural language processing. Variants have also been proposed for image data, but their applicability to remote sensing tasks is limited. To stimulate the development of foundation models for Earth monitoring, we propose a benchmark comprised of six classification and six segmentation tasks, which were carefully curated and adapted to be both relevant to the field and well-suited for model evaluation. We accompany this benchmark with a robust methodology for evaluating models and reporting aggregated results to enable a reliable assessment of progress. Finally, we report results for 20 baselines to gain information about the performance of existing models. We believe that this benchmark will be a driver of progress across a variety of Earth monitoring tasks.\n\n\n## Downloading the data\n\nThe data can be downloaded from [Zenodo](https://zenodo.org/communities/geo-bench/).\n\n## Getting Started\n\nComing soon.\n\n',
    'author': 'Alexandre Lacoste',
    'author_email': 'alexandre.lacoste@servicenow.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4',
}


setup(**setup_kwargs)
