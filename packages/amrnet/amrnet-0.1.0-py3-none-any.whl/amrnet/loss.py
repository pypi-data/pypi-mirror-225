"""

A loss function measures how godd our predictions are.

Which is used to adjust network parameters

"""


import numpy as np

from amrnet.tensor import Tensor



class Loss:
    
    
    def loss(self,predicted: Tensor, actual: Tensor) -> float:
        
        raise NotImplementedError
    

    def grad(self, predicted: Tensor, actual: Tensor) -> Tensor:
        
        raise NotImplementedError
    
    
    
    
    
class TSE(Loss):
    
    """
    Total Squared Error
    
    """
    
    
    def loss(self,predicted: Tensor, actual: Tensor) -> float:
        
        return np.sum((predicted - actual) ** 2)
    

    def grad(self, predicted: Tensor, actual: Tensor) -> Tensor:
        
        return 2 * (predicted - actual)
    
    
class MSE(Loss):
    
    """
    Mean Squared Error
    
    """
    
    def loss(self,predicted: Tensor, actual: Tensor) -> float:
        
        return np.sum((predicted - actual) ** 2) / len(actual)
    

    def grad(self, predicted: Tensor, actual: Tensor) -> Tensor:
        
        return 2 * (predicted - actual) / len(actual)
    
    
class MAE(Loss):
    
    def loss(self, predicted: Tensor, actual: Tensor) -> float:
        return np.sum(np.abs(predicted - actual)) / len(actual)
    
    def grad(self, predicted: Tensor, actual: Tensor) -> Tensor:
        
        return (1 * ((predicted - actual) >= 0) - 1 * ((predicted - actual) < 0)) / len(actual)
    
    
class LogCosh(Loss):
    
    def loss(self,predicted: Tensor, actual: Tensor) -> float:
        
        return np.sum(np.log10(np.cosh(predicted - actual)))
    

    def grad(self, predicted: Tensor, actual: Tensor) -> Tensor:
        
        return np.tanh(predicted - actual) / np.log(10)
    
    
