"""
Layers make up neural nets

Each layer needs to do a forward pass

then propagate its gradients backwards

"""

import numpy as np

from amrnet.tensor import Tensor


class Layer:
    
    def __init__(self) -> None:
        self.params = {}
        self.grads = {}
    
    
    def forward(self, inputs: Tensor) -> Tensor:
        """
        Produce the output coressponding to these inputs
        """
        
        raise NotImplementedError
    
    
    def backward(self, grad: Tensor) -> Tensor:
        """
        Back propagate this gradient through the layer
        """
        
        raise NotImplementedError
    
    

class Linear(Layer):
    
    """
    output = inputs @ w + b
    
    """
    
    
    def __init__(self, input_size: int, output_size: int) -> None:
        
        super().__init__()
        
        # inputs are (batch_size,input_size)
        
        # outputs are (batch_size,output_size)
        
        self.params['w'] = np.random.randn(input_size,output_size)
        
        self.params['b'] = np.random.randn(output_size)
        
        
    def forward(self, inputs: Tensor) -> Tensor:
        """
        output = inputs @ w + b
        
        """
        
        self.inputs = inputs
        return inputs @ self.params['w'] + self.params['b']
    
    
    def backward(self, grad: Tensor) -> Tensor:
        
        
        self.grads['b'] = np.sum(grad,axis=0)
        
        self.grads['w'] = self.inputs.T @ grad
        
        return grad @  self.params['w'].T
    


 
    
class Activation(Layer):
    
    """
    Applies a function elementwise to its inputs
    """
    
    def __init__(self, fn , fn_prime, *args) -> None:
        super().__init__()
        
        self.fn = fn
        
        self.fn_prime = fn_prime
        
        self.args = args
        
        
    def forward(self, inputs: Tensor) -> Tensor:
        
        self.inputs = inputs
        
        return self.fn(inputs,*self.args)
    
    def backward(self, grad: Tensor) -> Tensor:
        
        
        return self.fn_prime(self.inputs,*self.args) * grad
        
        
        
        
        
def tanh(x: Tensor) -> Tensor:
    
    return np.tanh(x)


def tanh_prime(x: Tensor) -> Tensor:
    
    y = tanh(x)
    
    return 1- y ** 2



class Tanh(Activation):
    
    def __init__(self) -> None:
        super().__init__(tanh, tanh_prime)
        

def relu(x):
    return np.maximum(0,x)     

def relu_prime(x):
    
    return 1 * (x > 0)
      
        
class RelU(Activation):
    
    def __init__(self) -> None:
        
        super().__init__(relu, relu_prime)
        
        
def leaky_relu(x,negative_slope):
    
    return np.maximum(x * negative_slope,x)

def leaky_relu_prime(x,negative_slope):
    
    return 1 * (x > 0) + negative_slope * (x <= 0)
    
        
class LeakyRelU(Activation):
    
    def __init__(self, negative_slope=0.01) -> None:
        super().__init__(leaky_relu, leaky_relu_prime,negative_slope)