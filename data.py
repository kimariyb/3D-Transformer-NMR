from torch.utils.data import Subset
from torch_geometric.data import DataLoader
from pytorch_lightning import LightningDataModule

from loader.carbon import CarbonDataset
from loader.hydrogen import HydrogenDataset


class DataModule(LightningDataModule):
    def __init__(self, hparams):
        super(DataModule, self).__init__()
        self.hparams.update(hparams.__dict__) if hasattr(
            hparams, "__dict__"
        ) else self.hparams.update(hparams)
        self._saved_dataloaders = dict()
        self.dataset = None

    def prepare_dataset(self):
        if self.hparams["dataset"] == "carbon":
            self.dataset = CarbonDataset(self.hparams)
        elif self.hparams["dataset"] == "hydrogen":
            self.dataset = HydrogenDataset(self.hparams)
            
        self.idx_train, self.idx_val, self.idx_test = None, None, None

        print(
            f"train {len(self.idx_train)}, val {len(self.idx_val)}, test {len(self.idx_test)}"
        )
        self.train_dataset = Subset(self.dataset, self.idx_train)
        self.val_dataset = Subset(self.dataset, self.idx_val)
        self.test_dataset = Subset(self.dataset, self.idx_test)

    def train_dataloader(self):
        return self._get_dataloader(self.train_dataset, "train")

    def val_dataloader(self):
        return self._get_dataloader(self.val_dataset, "val")

    def test_dataloader(self):
        return self._get_dataloader(self.test_dataset, "test")

    def _get_dataloader(self, dataset, stage, store_dataloader=True):
        store_dataloader = store_dataloader and not self.hparams["reload"]
        if stage in self._saved_dataloaders and store_dataloader:
            return self._saved_dataloaders[stage]

        if stage == "train":
            batch_size = self.hparams["batch_size"]
            shuffle = True
        elif stage in ["val", "test"]:
            batch_size = self.hparams["inference_batch_size"]
            shuffle = False

        dl = DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=self.hparams["num_workers"],
            pin_memory=True,
            drop_last=False,
        )

        if store_dataloader:
            self._saved_dataloaders[stage] = dl
        return dl


