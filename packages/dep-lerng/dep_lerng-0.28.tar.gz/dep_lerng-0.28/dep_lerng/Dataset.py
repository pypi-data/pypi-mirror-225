
import torch
from torch.utils.data import Dataset

data_dir = r'C:\Users\USER\Desktop\josh\Data\RAW_DATA'    

torch.manual_seed(43)

class WaferDS_Labled(Dataset):
    def __init__(self):
        
        self.labels = torch.load(f'{data_dir}/test_labels.pt')
        self.wafers = torch.load(f'{data_dir}/test_wafers.pt')     

        self.radon = torch.nan_to_num(torch.load(f'{data_dir}/test_radon.pt'))   
        # self.regional = torch.load(f'{data_dir_2}/regional.pt')    
        # self.statistical = torch.load(f'{data_dir_2}/statistical.pt')    
        # self.density = torch.load(f'{data_dir_2}/density.pt')    

    def __len__(self):

        return len(self.labels)

    def __getitem__(self, idx):

        label = self.labels[idx].long()
        image = self.wafers[idx]

        radon = self.radon[idx]
        # regional = self.regional[idx]
        # statistical = self.statistical[idx]
        # density = self.density[idx]

        # return image, radon, (regional, statistical, density), label
        return (image, radon), label
