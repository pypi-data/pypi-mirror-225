"""
for feeding data to network in batches
"""

from typing import Any
import numpy as np


from amrnet.tensor import Tensor


class DataIterator:
    
    def __call__(self, inputs: Tensor, targets: Tensor):
        raise NotImplementedError
    
    
    
    
class BatchIterator(DataIterator):
    
    def __init__(self, batch_size: int = 32, shuffle: bool = True) -> None:
        self.batch_size = batch_size
        
        self.shuffle = shuffle
    
    def __call__(self, inputs: Tensor, targets: Tensor):
        
        starts = np.arange(0,len(inputs), self.batch_size)
        
        if self.shuffle:
            
            np.random.shuffle(starts)
            
        for start in starts:
            
            end = start + self.batch_size
            
            batch_inputs = inputs[start:end]
            
            batch_targets = targets[start:end]
            
            yield batch_inputs, batch_targets