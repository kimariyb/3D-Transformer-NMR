import os
import torch

from torch_geometric.data import InMemoryDataset


class CarbonDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super(CarbonDataset, self).__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])
        
    @property
    def processed_dir(self):
        return os.path.join(self.root, 'carbon/processed')
        
    @property
    def processed_file_names(self):
        return 'processed.pt'
    

