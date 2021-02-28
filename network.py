import random
import numpy as np


class Network(object):

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in list(zip(sizes[:-1], sizes[1:]))]

    def feedforward(self, a):
        '''Return output of network with "a" as input.'''
        for b, w in list(zip(self.biases, self.weights)):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        '''Train neural network using mini-batch stochastic gradient descent.
            The "training_data" is a list of tuples, "(x,y)' representing the
            training inputs and desired outputs. The "epochs", is num of epochs,
            mini_batch_size, is num of inputs in mini-batch, "eta" is the learning
            rate. If"test_data" is provided, after each epoch, the network
             will be evaluated against the test data, with partial progress printed.'''
        if test_data:
            n_test = len(test_data)
            n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print(f'Epoch {j}: {(self.evaluate(test_data))} / {n_test}')
            else:
                print(f'Epoch {j} complete.')

    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        by applying gradient descent using backpropogation to a
        single mini batch. The "mini_batch" is a list of tuples
        "(x,y)', and "eta" is the learning rate."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in list(zip(nabla_b, delta_nabla_b))]
            nabla_w = [nw+dnw for nw, dnw in list(zip(nabla_w, delta_nabla_w))]
        self.weights = [w-(eta/len(mini_batch))*nw for w, nw in list(zip(self.weights, nabla_w))]
        self.biases = [b-(eta/len(mini_batch))*nb for b, nb in list(zip(self.biases, nabla_b))]

    def backprop(self, x, y):
        """Return a tuple, '(nabla_b, nabla_w)' representing the gradient
        for the cost function 'C_x'. 'nabla_b' and 'nalba_w' are layer-by-layer
        lists of numpy arrays, similar to 'self.biases' and 'self.weights'."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store activations
        zs = [] # list to store z vectors
        for b, w in list(zip(self.biases, self.weights)):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
            # backward pass
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return nabla_b, nabla_w
    
    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of the partial derivatives for C_x with respect to a
        for the output_activations."""
        return (output_activations - y)



# Other functions
def sigmoid(z):
    """Return sigmoid function applied to input "z"."""
    return 1.0/(1.0+np.exp(-z))


def sigmoid_prime(z):
    """Derivative of the sigmoid function"""
    return sigmoid(z)*(1-sigmoid(z))



