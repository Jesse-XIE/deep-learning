import network3
from network3 import Network
from network3 import ConvPoolLayer,SoftmaxLayer,FullyConnectedLayer
from net_manager import NetManager
import datetime


def eta_fn_wrapper(a, b):
    def eta_fn(epoch):
        return 1./(a * epoch + b)
    return eta_fn
eta_a = .33
eta_b = 10.
mini_batch_size = 50
auto_stop_epochs = 10
lmbda = 0.0
metas = []
eta_fn = eta_fn_wrapper(eta_a, eta_b)

training_data, validation_data, test_data = network3.load_data_shared()
net = Network([
        FullyConnectedLayer(n_in=784, n_out=100),
        SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)

net.SGD(training_data, validation_data, test_data, auto_stop_epochs, mini_batch_size, 
             eta_fn, lmbda)




# result:: 
# mb_size, eta,   valid_accu    test_accu
# 10,      0.05   97.89         97.83
# 50,      0.1    97.65         97.65
