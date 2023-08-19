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
 'sickle>=0.7,<0.8',
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
    'version': '0.0.1',
    'description': 'A benchmark designed to advance foundation models for Earth monitoring, tailored for remote sensing. It encompasses six classification and six segmentation tasks, curated for precision and model evaluation. The package also features a comprehensive evaluation methodology and showcases results from 20 established baseline models.',
    'long_description': '# GEO-Bench: Toward Foundation Models for Earth Monitoring\n\nGeoBench is a [ServiceNow Research](https://www.servicenow.com/research) project. \n\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Language: Python](https://img.shields.io/badge/language-Python%203.7%2B-green?logo=python&logoColor=green)](https://www.python.org)\n\nGEO-Bench is a General Earth Observation benchmark for evaluating the performances of large pre-trained models on geospatial data. Read the [full paper](https://arxiv.org/abs/2306.03831) for usage details and evaluation of existing pre-trained vision models.\n\n<img src="https://github.com/ServiceNow/geo-bench/raw/main/banner.png" width="500" />\n\n## Installation\n\nYou can install GEO-Bench with [pip](https://pip.pypa.io/):\n\n```console\n$ pip install geo-benchmark\n```\n\n## Downloading the data\n\nSet `$GEO_BENCH_DIR` to your preferred location. If not set, it will be stored in `$HOME/dataset/geobench`.\n\nNext, use the [download script](https://github.com/ServiceNow/geo-bench/blob/main/geobench/download_geobench.py). This will automatically download from [Zenodo](https://zenodo.org/communities/geo-bench/)\n\n```console\ncd geobench\npython download_geobench.py\n```\n\n## Loading Datasets\n\nSee [`example_load_dataset.py`](https://github.com/ServiceNow/geo-bench/blob/main/geobench/example_load_datasets.py) for how to iterate over datasets.\n\n```python\nfrom geobench import io\n\nfor task in io.task_iterator(benchmark_name="classification_v0.9.0"):\n    dataset = task.get_dataset(split="train")\n    sample = dataset[0]\n    for band in sample.bands:\n        print(f"  {band.band_info.name}: {band.data.shape}")\n\n```\n## Visualizing Results\n\nSee the notebook [`baseline_results.ipynb`](https://github.com/ServiceNow/geo-bench/blob/main/geobench/baseline_results.ipynb) for an example of how to visualize the results.\n\n\n',
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
