from collections import Counter

import numpy as np
import torch

from FederatedDataset.PartitionTypes.iid_partition import IIDPartition


class NonIIDPartitionPublicPrivate:
    def do_partitioning(
        dataset: torch.utils.data.Dataset,
        num_partitions: int,
        total_num_classes: int,
        alpha=1000000,
    ) -> dict:
        if not alpha:
            raise ValueError("Alpha must be a positive number")
        labels = dataset.targets
        idx = torch.tensor(list(range(len(labels))))

        index_per_label = {}
        for index, label in zip(idx, labels):
            if label.item() not in index_per_label:
                index_per_label[label.item()] = []
            index_per_label[label.item()].append(index.item())

        # in list labels we have the labels of this dataset
        list_labels = {item.item() for item in labels}

        to_be_sampled = []
        # create the distribution for each class
        for label in list_labels:
            # For each label we want a distribution over the num_partitions
            distribution = np.random.dirichlet(num_partitions * [alpha], size=1)
            # we have to sample from the group of samples that have label equal
            # to label and not from the entire labels list.
            selected_labels = labels[labels == label]
            tmp_to_be_sampled = np.random.choice(
                num_partitions, len(selected_labels), p=distribution[0]
            )
            # Inside to_be_sampled we save a counter for each label
            # The counter is the number of samples that we want to sample for each
            # partition
            to_be_sampled.append(Counter(tmp_to_be_sampled))
        # create the partitions
        partitions_index = {
            f"node_{cluster_name}": [] for cluster_name in range(0, num_partitions)
        }
        public_private_indexes = {}
       
        for class_index, distribution_samples in zip(list_labels, to_be_sampled):
            for cluster_name, samples in distribution_samples.items():
                partitions_index[f"node_{cluster_name}"] += index_per_label[
                    class_index
                ][:samples]

                index_per_label[class_index] = index_per_label[class_index][samples:]
    

        for node_name, indexes in partitions_index.items():
            public_and_private = IIDPartition.do_iid_partitioning_with_indexes(indexes=torch.tensor(indexes), num_partitions=2)
            public_private_indexes[f"{node_name}_private"] = public_and_private[0]
            public_private_indexes[f"{node_name}_public"] = public_and_private[1]

        total = 0
        for cluster, samples in public_private_indexes.items():
            total += len(samples)

        assert total == len(labels)

        partitions_labels = {
            cluster: [item.item() for item in labels[samples]]
            for cluster, samples in public_private_indexes.items()
        }

        return public_private_indexes, partitions_labels
