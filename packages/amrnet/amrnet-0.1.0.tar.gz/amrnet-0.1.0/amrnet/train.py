"""
function that trains our neural net
"""


from amrnet.tensor import Tensor

from amrnet.nn import NeuralNet

from amrnet.loss import Loss, TSE

from amrnet.optimizers import Optimizer, SGD

from amrnet.data import DataIterator, BatchIterator



def train(net: NeuralNet,
          inputs: Tensor,
          targets: Tensor,
          num_epochs: int = 5000,
          iterator: DataIterator = BatchIterator(),
          loss: Loss = TSE(),
          optimizer: Optimizer = SGD()) -> None:
    
    
    for epoch in range(num_epochs):
        
        epoch_loss = 0.0
        
        for batch_inputs, batch_targets in iterator(inputs, targets):
            
            
            
            predicted = net.forward(batch_inputs)
            
            epoch_loss += loss.loss(predicted, batch_targets)
            
            grad = loss.grad(predicted, batch_targets)
            
            net.backward(grad)
            
            optimizer.step(net)
            
        print(f'epoch {epoch} loss: {epoch_loss}')

