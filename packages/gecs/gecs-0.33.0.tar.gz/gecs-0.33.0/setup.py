# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gecs', 'gecs.utils']

package_data = \
{'': ['*']}

install_requires = \
['lightgbm==3.3.5',
 'matplotlib==3.7.1',
 'numpy==1.23.5',
 'pandas==1.5.2',
 'poetry==1.3.2',
 'pytest==7.2.1',
 'scikit-learn==1.2.2',
 'scipy==1.10.1',
 'tqdm==4.65.0',
 'typer==0.9.0']

setup_kwargs = {
    'name': 'gecs',
    'version': '0.33.0',
    'description': 'LightGBM Classifier with integrated bayesian hyperparameter optimization',
    'long_description': '![a gecko looking at the camera with bayesian math in white on a pink and green background](documentation/assets/header.png)\n\n\n# (100)gecs\n\nBayesian hyperparameter tuning for LGBMClassifier with a scikit-learn API\n\n\n## Table of Contents\n\n- [Project Overview](#project-overview)\n- [Introduction](#introduction)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Example](#example)\n- [Contributing](#contributing)\n- [License](#license)\n\n\n## Project Overview\n\n`gecs` is a tool to help automate the process of hyperparameter tuning for LightGBM classifiers, which can potentially save significant time and computational resources in model building and optimization processes. The `GEC` stands for **G**ood **E**nough **C**lassifier, which allows you to focus on other tasks such as feature engineering. If you deploy 100 of them, you get 100GECs.\n\n\n## Introduction\n\nThe primary class in this package is `GEC`, which is derived from `LGBMClassifier`. Like its parent, GEC can be used to build and train gradient boosting models, but with the added feature of **automated bayesian hyperparameter optimization**. It can be imported from `gecs.gec` and then used in place of `LGBMClassifier`, with the same API.\n\nBy default, `GEC` optimizes `boosting_type`, `learning_rate`, `reg_alpha`, `reg_lambda`, `min_child_samples`, `min_child_weight`, `colsample_bytree`, `subsample_freq`, `subsample` and optionally `num_leaves` and `n_estimators`. Which hyperparameters to tune is fully customizable.\n\n\n## Installation\n\n    pip install gecs\n\n\n## Usage\n\n\nThe `GEC` class provides the same API to the user as the `LGBMClassifier` class of `lightgbm`, and additionally:\n\n-   the two additional parameters to the fit method:\n    - `n_iter`: Defines the number of hyperparameter combinations that the model should try. More iterations could lead to better model performance, but at the expense of computational resources\n\n    - `fixed_hyperparameters`: Allows the user to specify hyperparameters that the GEC should not optimize. By default, these are `n_estimators` and `num_leaves`. Any of the LGBMClassifier init arguments can be fixed, and so can  `subsample_freq` and `subsample`, but only jointly. This is done by passing the value `bagging`.\n\n-   the methods `serialize` and `deserialize`, which stores the `GEC` state for the hyperparameter optimization process, **but not the fitted** `LGBMClassifier` **parameters**, to a json file. To store the boosted tree model itself, you have to provide your own serialization or use `pickle`\n\n-   the methods `freeze` and `unfreeze` that turn the `GEC` functionally into a `LGBMClassifier` and back\n\n\n## Example\n\nThe default use of `GEC` would look like this:\n\n    from sklearn.datasets import load_iris\n    from gecs.gec import GEC\n\n    X, y = load_iris(return_X_y=True)\n\n\n    # fit and infer GEC\n    gec = GEC()\n    gec.fit(X, y)\n    yhat = gec.predict(X)\n\n\n    # manage GEC state\n    path = "./gec.json"\n    gec.serialize(path) # stores gec data and settings, but not underlying LGBMClassifier attributes\n    gec2 = GEC.deserialize(path, X, y) # X and y are necessary to fit the underlying LGBMClassifier\n    gec.freeze() # freeze GEC so that it behaves like a LGBMClassifier\n    gec.unfreeze() # unfreeze to enable GEC hyperparameter optimisation\n\n\n    # benchmark against LGBMClassifier\n    from lightgbm import LGBMClassifier\n    from sklearn.model_selection import cross_val_score\n    import numpy as np\n\n    clf = LGBMClassifier()\n    lgbm_score = np.mean(cross_val_score(clf, X, y))\n\n    gec.freeze()\n    gec_score = np.mean(cross_val_score(gec, X, y))\n\n    print(f"{gec_score = }, {lgbm_score = }")\n    assert gec_score > lgbm_score, "GEC doesn\'t outperform LGBMClassifier"\n\n    #check what hyperparameter combinations were tried\n    gec.tried_hyperparameters()\n\n\n\n## Contributing\n\nIf you want to contribute, please reach out and I\'ll design a process around it.\n\n## License\n\nMIT\n\n## Contact Information\n\nYou can find my contact information on my website: [https://leonluithlen.eu](https://leonluithlen.eu)',
    'author': 'Leon Luithlen',
    'author_email': 'leontimnaluithlen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/0xideas/sequifier',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
