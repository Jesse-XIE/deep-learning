import network3
from network3 import Network
from network3 import ConvPoolLayer,SoftmaxLayer,FullyConnectedLayer

def eta_fn(epoch):
    return 1./(.33 * epoch + 10)

training_data, validation_data, test_data = network3.load_data_shared()
mini_batch_size = 50
net = Network([
        FullyConnectedLayer(n_in=784, n_out=100),
        SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)
# net.SGD(training_data, 10, mini_batch_size, 0.1,
#         validation_data, test_data)
net.SGD(training_data, 10, mini_batch_size, eta_fn,
        validation_data, test_data)



# result:: 
# mb_size, eta,   valid_accu    test_accu
# 10,      0.05   97.89         97.83
# 50,      0.1    97.65         97.65
