# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['FederatedDataset',
 'FederatedDataset.PartitionTypes',
 'FederatedDataset.Utils']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.3.0,<24.0.0',
 'google-api-python-client>=2.86.0,<3.0.0',
 'numpy>=1.24.2,<2.0.0',
 'opacus==1.3',
 'pandas>=1.5.3,<2.0.0',
 'pytest>=7.2.2,<8.0.0',
 'scikit-learn>=1.2.2,<2.0.0',
 'torch==2.0.0',
 'torchvision>=0.15.1,<0.16.0',
 'tqdm>=4.65.0,<5.0.0',
 'wandb>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'pistacchio-federated-dataset',
    'version': '0.0.1.post15',
    'description': 'A simple library to partition your dataset to perform federated learning',
    'long_description': '# FederatedDataset\n\nThis "library" allows you to create a partitioned dataset from a dataset. This is useful for federated learning.\n\n\n## Supported partitioning methods\n\n- IID partitioning: a simple partitioning method where we partition the dataset in N parts.\n- Non-IID partitioning: Given a dataset with C classes, we sample from a Dirichlet distribution the samples from each of these classes and assigne them to the nodes. \nThe non-iidness of the dataset is controlled by a alpha parameter.\n- Majority-Minority partitioning: We want to split the dataset among the nodes based on the target class to create unbalanced datasets. Given a dataset with C classes, \nwe split the samples of that class into two parts.\nThe first one comprising 70% of the data of that class is\ncalled the majority class. The second one, comprising the remaining 30% is\ncalled the minority class. To assign majority and minority classes to the clusters\nwe have two different cases.\nIf n_labels > n_clusters, we know that each node will have\nmax(num_labels / num_clusters, 1) different majority labels.\nConsidering that n_labels > n_clusters, each label will be assigned at most to\none node. Sometimes, we will have some labels that are not assigned to any node.\nIn this case, we distribute these labels among the nodes with an IID strategy.\nThe remaining 30% of the data will be assigned using a different strategy. Each\nof these minority classes will be assigned to 50% of the nodes that do not have\nthat class. For instance, let us consider the case with 10 labels and 5 clusters.\nIn this case, each cluster will have 2 majority classes. We assign 70% of the data\nof each majority class to one node. Then we have to assign the remaining 30%\nof the data. In this case, each minority class will be assigned to two nodes.\nIf n_labels < n_clusters, each majority class will be assigned to at most\nn_clusters / n_labels nodes. In this case, we have that a majority class can be\nassigned to more than one node. In this case, we equally divide the majority\nclass\'s data among the nodes. For the minority classes, we have that each minority\nclass will be assigned to the 50% of the nodes that do not have that class.\nFor instance. If we have 5 labels and 10 nodes, then we have that each node will\nhave 2 majority classes. We assign 35% of the data of each majority class to one\nof these two nodes. Then we have to assign the remaining 30% of the data. In this\ncase, each minority class will be assigned to two nodes.\n\n## How to use this library\n\nYou can use this library in two differnet ways:\n- You can run the code to partition the dataset from CLI\n- You can import the library and use it in your code\n\n### CLI\n\nIn the examples folder there are some already made examples. You can run them with the following command:\n\n```bash\npoetry run python ./generate_dataset.py --config majority_minority_3_8.json\n```\n\nThe previous command partitions the dataset in 3 clusters and then for each cluster, it creates 8 partitions. The configuration file is a json file that contains the following fields:\n\n```json\n{\n    "dataset": "mnist",\n    "data_split_config": {\n        "split_type_clusters": "majority_minority",\n        "split_type_nodes": "non_iid",\n        "num_classes": 10,\n        "num_nodes": 8,\n        "num_clusters": 3,\n        "alpha": 1,\n        "store_path": "../data/MNIST/federated_data"\n    }\n}\n```\n\nIf you want to partition only among the nodes:\n\n```json\n{\n    "dataset": "mnist",\n    "data_split_config": {\n        "split_type_nodes": "non_iid",\n        "num_classes": 10,\n        "num_nodes": 8,\n        "alpha": 1,\n        "store_path": "../data/MNIST/federated_data"\n    }\n}\n```\n\n### From your code\n\nYou can import the library and use it in your code. The following code shows how to use the library:\n\n```python\nfrom federated_dataset import FederatedDataset\n\n\n\nFederatedDataset.generate_partitioned_dataset(\n    split_type_clusters="majority_minority",\n    split_type_nodes="non_iid",\n    num_nodes=8,\n    num_clusters=3,\n    num_classes=10,\n    alpha=1.0,\n    dataset_name="mnist",\n    store_path="../data/MNIST/federated_data",\n)\n```\n\nWith the previous code you\'ll partition the dataset among 3 clusters and then among 8 nodes.\n\nIf you just want to partition the dataset among 8 nodes, you can use the following code:\n\n```python\nfrom federated_dataset import FederatedDataset\n\nFederatedDataset.generate_partitioned_dataset(\n    split_type_nodes="majority_minority", # "non_iid" or "iid"\n    num_nodes=8,\n    num_classes=10,\n    dataset_name="mnist",\n    store_path="../data/MNIST/federated_data",\n)\n```\n\nIn the previous examples we passed the parameter dataset_name. In this case, the dataset will be \ndownloaded inside the generate_partitioned_dataset function. If you want to pass a custom dataset you can do it in this way:\n\n```python\nfrom federated_dataset import FederatedDataset\n\ntrain_ds = torchvision.datasets.MNIST(\n        "../data/MNIST",\n        train=True,\n        download=True,\n        transform=torchvision.transforms.Compose(\n            [torchvision.transforms.ToTensor()]\n        ),\n    )\ntest_ds = torchvision.datasets.MNIST(\n        "../data/MNIST",\n        train=False,\n        download=True,\n        transform=torchvision.transforms.Compose(\n            [torchvision.transforms.ToTensor()]\n        ),\n    )\n\nFederatedDataset.generate_partitioned_dataset(\n    split_type_nodes="majority_minority", # "non_iid" or "iid"\n    num_nodes=8,\n    num_classes=10,\n    dataset_name="mnist",\n    store_path="../data/MNIST/federated_data",\n    train_ds=train_ds,\n    test_ds=test_ds\n)\n```\n\n\nIn the examples folder there are some examples that show how to use the library.',
    'author': 'Luca Corbucci',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
