# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rul_adapt',
 'rul_adapt.approach',
 'rul_adapt.construct',
 'rul_adapt.construct.adarul',
 'rul_adapt.construct.cnn_dann',
 'rul_adapt.construct.consistency',
 'rul_adapt.construct.latent_align',
 'rul_adapt.construct.lstm_dann',
 'rul_adapt.construct.tbigru',
 'rul_adapt.loss',
 'rul_adapt.model']

package_data = \
{'': ['*'],
 'rul_adapt.construct.adarul': ['config/*', 'config/task_source/*'],
 'rul_adapt.construct.cnn_dann': ['config/*'],
 'rul_adapt.construct.consistency': ['config/*', 'config/dataset/*'],
 'rul_adapt.construct.latent_align': ['config/*',
                                      'config/dataset/*',
                                      'config/split_steps/*',
                                      'config/subtask/*'],
 'rul_adapt.construct.lstm_dann': ['config/*', 'config/task/*'],
 'rul_adapt.construct.tbigru': ['config/*', 'config/task/*']}

install_requires = \
['dtaidistance>=2.3.10,<3.0.0',
 'hydra-core>=1.3.1,<2.0.0',
 'pytorch-lightning>=1.8.0.post1,<2.0.0',
 'pywavelets>=1.4.1,<2.0.0',
 'rul-datasets>=0.10.5,<0.11.0',
 'tqdm>=4.62.2,<5.0.0']

setup_kwargs = {
    'name': 'rul-adapt',
    'version': '0.2.0',
    'description': 'A collection of unsupervised domain adaption approaches for RUL estimation.',
    'long_description': '# RUL Adapt\n\n[![Master](https://github.com/tilman151/rul-adapt/actions/workflows/on_push.yaml/badge.svg)](https://github.com/tilman151/rul-adapt/actions/workflows/on_push.yaml)\n[![Release](https://github.com/tilman151/rul-adapt/actions/workflows/on_release.yaml/badge.svg)](https://github.com/tilman151/rul-adapt/actions/workflows/on_release.yaml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nThis library contains a collection of unsupervised domain adaption algorithms for RUL estimation.\nThey are provided as [LightningModules](https://pytorch-lightning.readthedocs.io/en/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule) to be used in [PyTorch Lightning](https://pytorch-lightning.readthedocs.io/en/latest/).\n\nCurrently, five approaches are implemented, including their original hyperparameters:\n\n* **LSTM-DANN** by Da Costa et al. (2020)\n* **ADARUL** by Ragab et al. (2020)\n* **LatentAlign** by Zhang et al. (2021)\n* **TBiGRU** by Cao et al. (2021)\n* **Consistency-DANN** by Siahpour et al. (2022)\n\nThree approaches are implemented without their original hyperparameters:\n\n* **ConditionalDANN** by Cheng et al. (2021)\n* **ConditionalMMD** by Cheng et al. (2021)\n* **PseudoLabels** as used by Wang et al. (2022)\n\nThis includes the following general approaches adapted for RUL estimation:\n\n* **Domain Adaption Neural Networks (DANN)** by Ganin et al. (2016)\n* **Multi-Kernel Maximum Mean Discrepancy (MMD)** by Long et al. (2015)\n\nEach approach has an example notebook which can be found in the [examples](https://github.com/tilman151/rul-adapt/tree/master/examples) folder.\n\n## Installation\n\nThis library is pip-installable. Simply type:\n\n```bash\npip install rul-adapt\n```\n\n## Contribution\n\nContributions are always welcome. Whether you want to fix a bug, add a feature or a new approach, just open an issue and a PR.',
    'author': 'Krokotsch, Tilman',
    'author_email': 'tilman.krokotsch@tu-berlin.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://krokotsch.eu/rul-adapt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
