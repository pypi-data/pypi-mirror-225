import datasets
from datasets import load_dataset
from fedata.split.shard_splits import Shard_Splits
from fedata.exceptions.generateexceptions import Invalid_SplitType

def load_mnist(settings: dict) -> list[datasets.arrow_dataset.Dataset,
                                       list[list[list[datasets.arrow_dataset.Dataset]]]]:
    """Loads the MNIST dataset, splits it into the number of shards, pre-process selected
    shards (subsets) and returns in a following format:
    list[   
        "Orchestrator Data"[
            Dataset
            ],   
        "Agents Data"[
            "Agent N"[
                "Train Data"[
                Dataset
                ],
                "Test Data"[
                Dataset
                ]
            ]]]
    Where all 'Datasets' are an instances of hugging face container datasets.arrow_dataset.Dataset
    ---------
    Args:
        settings (dict) : A dictionary containing all the dataset settings.
    Returns:
        list[datasets.arrow_dataset.Dataset,
                                       list[list[list[datasets.arrow_dataset.Dataset]]]]"""
    
    # Using the 'test' data as a orchestrator validaiton set.
    orchestrator_data = load_dataset('mnist', split='test')
    # Using the 'train' data as a dataset reserved for agents
    dataset = load_dataset('mnist', split='train')

    # Settings rng seed
    if settings.get('rng_seed'):
        shard_splits = Shard_Splits(settings['rng_seed'])
    else:
        shard_splits = Shard_Splits(seed=42)

    # Type: Homogeneous Size and Distribution (Sharding) -> Same size, similar distribution 
    if settings['split_type'] == 'homogeneous':
        return [orchestrator_data, shard_splits.homogeneous(dataset=dataset, settings=settings)]
    
    # Type: Heterogeneous Size, Homogeneous Distribution -> Differeny size (draws from exponential distribution), similar distribution
    elif settings['split_type'] == 'heterogeneous_size':
        return [orchestrator_data, shard_splits.heterogeneous_size(dataset=dataset, settings=settings)]
    
    # Type: Dominant clients are sampled first according to the pre-defined in-sample distribution. Then rest of the clients draws from 
    # left-over data instances
    elif settings['split_type'] == "dominant_sampling":
        return [orchestrator_data, shard_splits.dominant_sampling(dataset=dataset, settings=settings)]

    # Type: Dataset replication -> One dataset copied n times.
    elif settings['split_type'] == 'replication':
        return [orchestrator_data, shard_splits.replication(dataset=dataset, settings=settings)]
    
    # Type: Blocks - One dataset copied inside one block (cluster)
    elif settings['split_type'] == 'split_in_blocks':
        return [orchestrator_data, shard_splits.replicate_same_dataset(dataset=dataset, settings=settings)]
    
    else:
        raise Invalid_SplitType
            