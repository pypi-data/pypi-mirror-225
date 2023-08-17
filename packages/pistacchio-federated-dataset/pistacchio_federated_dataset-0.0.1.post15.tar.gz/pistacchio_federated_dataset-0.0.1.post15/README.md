# FederatedDataset

This "library" allows you to create a partitioned dataset from a dataset. This is useful for federated learning.


## Supported partitioning methods

- IID partitioning: a simple partitioning method where we partition the dataset in N parts.
- Non-IID partitioning: Given a dataset with C classes, we sample from a Dirichlet distribution the samples from each of these classes and assigne them to the nodes. 
The non-iidness of the dataset is controlled by a alpha parameter.
- Majority-Minority partitioning: We want to split the dataset among the nodes based on the target class to create unbalanced datasets. Given a dataset with C classes, 
we split the samples of that class into two parts.
The first one comprising 70% of the data of that class is
called the majority class. The second one, comprising the remaining 30% is
called the minority class. To assign majority and minority classes to the clusters
we have two different cases.
If n_labels > n_clusters, we know that each node will have
max(num_labels / num_clusters, 1) different majority labels.
Considering that n_labels > n_clusters, each label will be assigned at most to
one node. Sometimes, we will have some labels that are not assigned to any node.
In this case, we distribute these labels among the nodes with an IID strategy.
The remaining 30% of the data will be assigned using a different strategy. Each
of these minority classes will be assigned to 50% of the nodes that do not have
that class. For instance, let us consider the case with 10 labels and 5 clusters.
In this case, each cluster will have 2 majority classes. We assign 70% of the data
of each majority class to one node. Then we have to assign the remaining 30%
of the data. In this case, each minority class will be assigned to two nodes.
If n_labels < n_clusters, each majority class will be assigned to at most
n_clusters / n_labels nodes. In this case, we have that a majority class can be
assigned to more than one node. In this case, we equally divide the majority
class's data among the nodes. For the minority classes, we have that each minority
class will be assigned to the 50% of the nodes that do not have that class.
For instance. If we have 5 labels and 10 nodes, then we have that each node will
have 2 majority classes. We assign 35% of the data of each majority class to one
of these two nodes. Then we have to assign the remaining 30% of the data. In this
case, each minority class will be assigned to two nodes.

## How to use this library

You can use this library in two differnet ways:
- You can run the code to partition the dataset from CLI
- You can import the library and use it in your code

### CLI

In the examples folder there are some already made examples. You can run them with the following command:

```bash
poetry run python ./generate_dataset.py --config majority_minority_3_8.json
```

The previous command partitions the dataset in 3 clusters and then for each cluster, it creates 8 partitions. The configuration file is a json file that contains the following fields:

```json
{
    "dataset": "mnist",
    "data_split_config": {
        "split_type_clusters": "majority_minority",
        "split_type_nodes": "non_iid",
        "num_classes": 10,
        "num_nodes": 8,
        "num_clusters": 3,
        "alpha": 1,
        "store_path": "../data/MNIST/federated_data"
    }
}
```

If you want to partition only among the nodes:

```json
{
    "dataset": "mnist",
    "data_split_config": {
        "split_type_nodes": "non_iid",
        "num_classes": 10,
        "num_nodes": 8,
        "alpha": 1,
        "store_path": "../data/MNIST/federated_data"
    }
}
```

### From your code

You can import the library and use it in your code. The following code shows how to use the library:

```python
from federated_dataset import FederatedDataset



FederatedDataset.generate_partitioned_dataset(
    split_type_clusters="majority_minority",
    split_type_nodes="non_iid",
    num_nodes=8,
    num_clusters=3,
    num_classes=10,
    alpha=1.0,
    dataset_name="mnist",
    store_path="../data/MNIST/federated_data",
)
```

With the previous code you'll partition the dataset among 3 clusters and then among 8 nodes.

If you just want to partition the dataset among 8 nodes, you can use the following code:

```python
from federated_dataset import FederatedDataset

FederatedDataset.generate_partitioned_dataset(
    split_type_nodes="majority_minority", # "non_iid" or "iid"
    num_nodes=8,
    num_classes=10,
    dataset_name="mnist",
    store_path="../data/MNIST/federated_data",
)
```

In the previous examples we passed the parameter dataset_name. In this case, the dataset will be 
downloaded inside the generate_partitioned_dataset function. If you want to pass a custom dataset you can do it in this way:

```python
from federated_dataset import FederatedDataset

train_ds = torchvision.datasets.MNIST(
        "../data/MNIST",
        train=True,
        download=True,
        transform=torchvision.transforms.Compose(
            [torchvision.transforms.ToTensor()]
        ),
    )
test_ds = torchvision.datasets.MNIST(
        "../data/MNIST",
        train=False,
        download=True,
        transform=torchvision.transforms.Compose(
            [torchvision.transforms.ToTensor()]
        ),
    )

FederatedDataset.generate_partitioned_dataset(
    split_type_nodes="majority_minority", # "non_iid" or "iid"
    num_nodes=8,
    num_classes=10,
    dataset_name="mnist",
    store_path="../data/MNIST/federated_data",
    train_ds=train_ds,
    test_ds=test_ds
)
```


In the examples folder there are some examples that show how to use the library.