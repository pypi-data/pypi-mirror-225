"""
An optimizer is used to adjust the network parameters based on gradients computed from back propagtion
"""
import numpy as np

from amrnet.nn import NeuralNet

class Optimizer:
    
    def step(self, net: NeuralNet) -> None:
        
        raise NotImplementedError
    
    
class SGD(Optimizer):
    
    def __init__(self, lr: float = 0.01) -> None:
        
        self.lr = lr
        
        
    def step(self, net: NeuralNet) -> None:
        
        for param, grad in net.params_and_grads():
            
            param -= self.lr * grad
            
            
class Momentum(SGD):
    
    def __init__(self, lr: float = 0.01, momentum: float = 0.9) -> None:
        
        super().__init__(lr)
        
        self.momentum = momentum
        
        
    def step(self, net: NeuralNet) -> None:
        
        v = 0
        
        for param, grad in net.params_and_grads():
            
            v = self.momentum * v + (1 - self.momentum) * grad
            
            
            
            param -=  self.lr * v