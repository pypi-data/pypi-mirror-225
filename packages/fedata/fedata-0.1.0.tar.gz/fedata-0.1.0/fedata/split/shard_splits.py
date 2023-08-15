import datasets
from fedata.transform.shard_transformation import Shard_Transformation
from fedata.utils.showcase import save_random
import copy
import numpy as np

def rescale_vector_tosum(vector, 
                         desired_sum):
    norm_const = desired_sum / vector.sum()
    vector = vector * norm_const
    vector = vector.astype(int)
    l = desired_sum - vector.sum()
    np.argpartition(vector, l)
    for _ in range(l):
        vector[np.argmin(vector)] += 1
    return vector


def transform_shard(shard,
                    transformation_settings,
                    save_transformation: bool = False,
                    shard_name: int = None):
    if save_transformation:
        original_imgs = copy.deepcopy(shard['image'])
    shard = Shard_Transformation.transform(shard, preferences=transformation_settings) # CALL SHARD_TRANSFORMATION CLASS
    if save_transformation:
        save_random(original_imgs, 
                    shard['image'], 
                    transformation_settings["transformation_type"],
                    name = f"of_node_{shard_name}")
    return shard


class Shard_Splits:
    """a common class for creating various splits among the clients"""
    def __init__(self,
                 seed: int) -> None:
        self.seed = seed


    def homogeneous(self,
                    dataset: datasets.arrow_dataset.Dataset,
                    settings: dict):
        # DATASET SHUFFLING
        if settings['shuffle'] == True:
            dataset = dataset.shuffle(seed = self.seed)
        # SHARD PARTITIONING
        nodes_data = []
        for shard in range(settings['shards']): # Each shard corresponds to one agent.
            agent_data = dataset.shard(num_shards=settings['shards'], index=shard)
            # Shard transformation
            if shard in settings['transformations'].keys():
                agent_data = transform_shard(shard=agent_data,
                                        transformation_settings=settings['transformations'][shard],
                                        save_transformation=settings["save_transformations"],
                                        shard_name=shard)
            # In-shard split between test and train data.
            agent_data = agent_data.train_test_split(test_size=settings["local_test_size"])
            nodes_data.append([agent_data['train'], agent_data['test']])
        # RETURNING NODES DATA
        return nodes_data
    
    
    def heterogeneous_size(self,
                           dataset: datasets.arrow_dataset.Dataset,
                           settings: dict):
        #DATASET SHUFFLING
        if settings['shuffle'] == True:
            dataset = dataset.shuffle(seed = self.seed)
        
        # INDEX PARTITIONING
        nodes_data = []
        clients = settings['agents']
        beta = len(dataset) / clients # Average shard size
        rng = np.random.default_rng(self.seed)
        # Drawing from exponential distribution size of the local sample
        shards_sizes = rng.exponential(scale=beta, size=clients)
        shards_sizes = rescale_vector_tosum(vector = shards_sizes, desired_sum = len(dataset))
        print(shards_sizes)

        # SHARD PARTITIONING
        moving_idx = 0
        for shard in range(clients):
            ag_idx = moving_idx + shards_sizes[shard]
            agent_data = dataset.select(range(moving_idx, ag_idx))
            # Shard transformation
            if shard in settings['transformations'].keys():
                agent_data = transform_shard(shard=agent_data,
                                        transformation_settings=settings['transformations'][shard],
                                        save_transformation=settings["save_transformations"],
                                        shard_name=shard)
            moving_idx = ag_idx
            agent_data = agent_data.train_test_split(test_size=settings["local_test_size"])
            nodes_data.append([agent_data['train'], agent_data['test']])
        # RETURNING NODES DATA
        return nodes_data


    def dominant_sampling(self,
                          dataset: datasets.arrow_dataset.Dataset,
                          settings: dict):
        nodes_data = []
        no_agents = settings['agents']
        imbalanced_agents = settings['imbalanced_clients']
        agents = [agent for agent in range(no_agents)]
        pandas_df = dataset.to_pandas().drop('image', axis=1)
        labels = sorted(pandas_df.label.unique())
        if settings.get('custom_sample_size'):
            sample_size = settings['custom_sample_size']
        else:
            sample_size = int(len(dataset) / no_agents)
    
        # I) Sampling dominant clients
        for agent in agents:
            if agent in imbalanced_agents:
                # 1. Sampling indexes
                sampling_weights = {key: (1 - imbalanced_agents[agent][1]) / (len(labels) - 1) for key in labels}
                sampling_weights[imbalanced_agents[agent][0]] = imbalanced_agents[agent][1]
                
                # Additional step, checking the availability of every label TODO
                # required_samples = (np.array(list(sampling_weights.values())) * sample_size).astype('int')
                # counts = pandas_df['label'].value_counts()[pandas_df['label'].value_counts() > required_samples]
                
                # 2. Applying weights
                pandas_df["weights"] = pandas_df['label'].apply(lambda x: sampling_weights[x])
                sample = pandas_df.sample(n = sample_size, weights='weights', random_state=42)
                
                counts = sample['label'].value_counts().sort_index()
                # 3. Selecting indexes and performing test - train split.
                sampled_data = dataset.filter(lambda filter, idx: idx in list(sample.index), with_indices=True)
                
                # Shard transformation
                if agent in settings['transformations'].keys():
                    sampled_data = transform_shard(shard=sampled_data,
                                            transformation_settings=settings['transformations'][agent],
                                            save_transformation=settings["save_transformations"],
                                            shard_name=agent)
                agent_data = sampled_data.train_test_split(test_size=settings["local_test_size"])
                nodes_data.append([agent_data['train'], agent_data['test']])
                
                # 4. Removing samples indexes
                pandas_df.drop(sample.index, inplace=True)
            else:
                nodes_data.append([]) # Inserting placeholder to preserve in-list order.


        # II) Sampling non-dominant clients
        for agent in agents:
            if agent not in imbalanced_agents:
                # 1. Sampling indexes
                sample = pandas_df.sample(n = sample_size, random_state=42)
                counts = sample['label'].value_counts().sort_index()
                # 2. Selecting indexes and performing test - train split.
                sampled_data = dataset.filter(lambda filter, idx: idx in list(sample.index), with_indices=True)
                # Shard transformation
                if agent in settings['transformations'].keys():
                    sampled_data = transform_shard(shard=sampled_data,
                                            transformation_settings=settings['transformations'][agent],
                                            save_transformation=settings["save_transformations"],
                                            shard_name=agent)
                agent_data = sampled_data.train_test_split(test_size=settings["local_test_size"])
                nodes_data[agent] = ([agent_data['train'], agent_data['test']])
                # 3. Removing samples indexes
                pandas_df.drop(sample.index, inplace=True)
        return nodes_data


    def replication(self,
                    dataset: datasets.arrow_dataset.Dataset,
                    settings: dict):
        nodes_data = []
        block_data = dataset.shard(num_shards=1, index=0)
        for shard in range(settings['agents']):
            agent_data = copy.deepcopy(block_data)
            if shard in settings['transformations'].keys():
                agent_data = transform_shard(shard=agent_data,
                                        transformation_settings=settings['transformations'][shard],
                                        save_transformation=settings["save_transformations"],
                                        shard_name=shard)
            agent_data = agent_data.train_test_split(test_size=settings["local_test_size"])
            nodes_data.append([agent_data['train'], agent_data['test']])
        
        return nodes_data
    

    # @staticmethod
    # def split_in_blocks(dataset: datasets.arrow_dataset.Dataset,
    #                     settings: dict):
    #     nodes_data = []
    #     for shard in range(settings['shards']):
    #         agent_data = dataset.shard(num_shards=settings['shards'], index=shard)
    #         agent_data = agent_data.train_test_split(test_size=settings["local_test_size"])
    #         for _ in range((int(settings['agents'] / settings['shards']))):
    #             nodes_data.append([copy.deepcopy(agent_data['train']), copy.deepcopy(agent_data['test'])])
    #     return nodes_data