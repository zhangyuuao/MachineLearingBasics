"""
Introduction to Machine Learning

Lab 3: Regularized linear regression

TODO: Add your information here.
    IMPORTANT: Please ensure this script
    (1) Run script_lab3.py on Python >=3.6;
    (2) No errors;
    (3) Finish in tolerable time on a single CPU (e.g., <=10 mins);
Student name(s): 张宇尧
Student ID(s): 2020201710
"""

import numpy as np
# don't add any other packages


# data simulator and testing function (Don't change them)
def linear_data_simulator(n_train: int = 50,
                          n_test: int = 10,
                          dim: int = 10,
                          v_noise: float = 2,
                          prior: str = 'Gauss',
                          noise: str = 'Gauss',
                          r_seed: int = 42) -> dict:
    """
    Simulate the training and testing data generated by a polynomial model
    :param n_train: the number of training data
    :param n_test: the number of testing data
    :param dim: the dimension of feature
    :param v_noise: the hyper-parameter controlling the variance of data noise
    :param prior: the prior distribution of model parameters, Gauss or Laplace
    :param noise: the noise type, Gauss or Laplace
    :param r_seed: the random seed
    :return:
        a dictionary containing training set, testing set, and the ground truth parameters
    """
    x_train = np.random.RandomState(r_seed).rand(n_train, dim)
    x_test = np.random.RandomState(r_seed).rand(n_test, dim)
    if prior == 'Gauss':
        weights = np.random.RandomState(r_seed).randn(dim, 1)
    else:
        weights = np.random.RandomState(r_seed).laplace(loc=0, scale=1, size=(dim, 1))
    if noise == 'Gauss':
        y_train = x_train @ weights + v_noise * np.random.RandomState(r_seed).randn(n_train, 1)
        y_test = x_test @ weights + v_noise * np.random.RandomState(r_seed).randn(n_test, 1)
    else:
        y_train = x_train @ weights + np.random.RandomState(r_seed).laplace(loc=0, scale=v_noise, size=(n_train, 1))
        y_test = x_test @ weights + np.random.RandomState(r_seed).laplace(loc=0, scale=v_noise, size=(n_test, 1))
    data = {'train': [x_train, y_train],
            'test': [x_test, y_test],
            'real': weights}
    return data


def mse(x: np.ndarray, x_est: np.ndarray) -> float:
    return np.sum((x - x_est) ** 2) / x.shape[0]


def testing(x: np.ndarray, y: np.ndarray, weights: np.ndarray) -> float:
    """
    Compute the MSE of regression based on current model
    :param x: testing data with size (N, )
    :param y: testing label with size (N, 1)
    :param weights: model parameter with size (D, 1)
    :return:
        MSE
    """
    y_est = x @ weights
    return mse(y, y_est)


# Task 1: Implement the training function of the ridge regression model,
# which derives the closed form solution directly
def training(x: np.ndarray, y: np.ndarray, gamma: float) -> np.ndarray:
    """
    The training function of ridge regression model

    min_w ||y - Xw||_2^2 + gamma * ||w||_2^2

    :param x: input data with size (N, dim)
    :param y: labels of data with size (N, 1)
    :param gamma: the weight of the ridge regularizer
    :return:
        a weight vector with size (dim, 1)
    """
    # TODO: Change the code below and add the closed form solution of ridge regression
    w = np.linalg.inv(x.T @ x + gamma * np.identity(x.shape[1])) @ x.T @ y
    return np.zeros((x.shape[1], 1))


# Task 2: Implement the training function of the ridge regression model,
# which implements the stochastic gradient descent (sgd) algorithm.
def training_sgd(x: np.ndarray,
                 y: np.ndarray,
                 gamma: float,
                 epoch: int = 10,
                 batch_size: int = 10,
                 lr: float = 1e-4,
                 r_seed: int = 1) -> np.ndarray:
    """
    The stochastic gradient descent method of ridge regression.
    :param x: input data with size (N, dim)
    :param y: labels of data with size (N, 1)
    :param gamma: the weight of ridge regularizer
    :param epoch: the number of epochs
    :param batch_size: the batch size for sgd
    :param lr: the learning rate
    :param r_seed: random seed
    :return:
        a weight vector with size (order, 1)
    """
    num = x.shape[0]
    dim = x.shape[1]
    w = np.random.RandomState(r_seed).randn(dim, 1)
    # TODO: Given the initialization above, implement your own SGD algorithm for ridge regression
    np.random.seed(r_seed)
    for i in range(epoch) :
        rand_index = np.random.randint(0, x.shape[0], batch_size)
        x_s = x[rand_index]
        y_s = y[rand_index]
        grad = 2 * x_s.T @ (x_s @ w - y_s) + 2 * gamma * w
        w = w - lr * grad
    return w


# Task 3: Implement the training function of lasso regression
def soft_thresholding(x: np.ndarray, thres: float) -> np.ndarray:
    """
    The soft-thresholding operator
    :param x: input array with arbitrary size
    :param thres: the threshold
    :return:
        sign(x) * max{0, |x|-thres}
    """
    # TODO: Change the code below and implement the soft-thresholding operation
    x = np.sign(x) * np.maximum(0, np.abs(x) - thres)
    return x


def training_lasso(x: np.ndarray,
                   y: np.ndarray,
                   gamma: float,
                   iteration: int = 100,
                   r_seed: int = 1) -> np.ndarray:
    """
    The training function of lasso regression model

    min_w ||y - Xw||_2^2 + gamma * ||w||_1

    :param x: input data with size (N, dim)
    :param y: labels of data with size (N, 1)
    :param gamma: the weight of the lasso regularizer
    :param iteration: the number of iterations for soft-thresholding
    :param r_seed: the random seed for initializing model.
    :return:
        a weight vector with size (dim, 1)
    """
    dim = x.shape[1]
    w = np.random.RandomState(r_seed).randn(dim, 1)
    # TODO: Given the initialization above, implement your own iterative soft-thresholding algorithm for lasso
    #  Hint: call the "soft_thresholding" function you implemented iteratively
    for i in range(iteration) :
        for j in range(0, dim) :
            x_d = x[:,j].reshape(-1,1) # attention: ndarray with size of (50,) is not a vector,so apply this function .reshape(-1,1) to convert it to a column vector
            x_c = np.delete(x,j,axis=1)
            w_c = np.delete(w,j,axis=0)
            w[j] = soft_thresholding((x_d.T @ (y - x_c @ w_c)) / (np.sum(x_d ** 2)), gamma / (np.sum(x_d ** 2)))
    return w

# Task 4: Implement the training function of the linear regression with elastic net regression
def training_elastic(x: np.ndarray,
                     y: np.ndarray,
                     gamma1: float,
                     gamma2: float,
                     iteration: int = 100,
                     r_seed: int = 1) -> np.ndarray:
    """
    The training function of lasso regression model

    min_w ||y - Xw||_2^2 + gamma1 * ||w||_1 + gamma2 * ||w||_2^2

    :param x: input data with size (N, dim)
    :param y: labels of data with size (N, 1)
    :param gamma1: the weight of the lasso regularizer
    :param gamma2: the weight of the ridge regularizer
    :param iteration: the number of iterations for soft-thresholding
    :param r_seed: the random seed for initializing model.
    :return:
        a weight vector with size (dim, 1)
    """
    # TODO: Change the code below and implement an algorithm to solve the linear regression with elastic net regularizer
    #  Hint: Try to reformulate the problem to a lasso.
    dim = x.shape[1]
    w = np.random.RandomState(r_seed).randn(dim, 1)
    x_gamma2 = np.ones((dim, dim)) * np.sqrt(gamma2)
    y_zeros = np.zeros((dim, 1))
    for i in range(iteration) :
        for j in range(dim) :
            X = np.r_[x, x_gamma2]
            Y = np.r_[y, y_zeros]
            X_d = X[:,j].reshape(-1,1)
            X_c = np.delete(X,j,axis=1)
            W_c = np.delete(w,j,axis=0)
            w[j] = soft_thresholding((X_d.T @ (Y - X_c @ W_c)) / (np.sum(X_d ** 2)), gamma1 / (np.sum(X_d ** 2)))
    return w


# Task 5: Implement the iteratively reweighted least square (IRLS) to solve min_w ||y - Xw||_1
def training_irls(x: np.ndarray,
                  y: np.ndarray,
                  iteration: int = 100,
                  r_seed: int = 1) -> np.ndarray:
    """
    min_w ||y - Xw||_1 (MAE minimization)

    :param x: testing data with size (N, dim)
    :param y: testing label with size (N, 1)
    :param iteration: the number of iterations for soft-thresholding
    :param r_seed: the random seed for initializing model.
    :return:
        a weight vector with size (dim, 1)
    """
    dim = x.shape[1]
    num = x.shape[0]
    w = np.random.RandomState(r_seed).randn(dim, 1)
    # TODO: Given the initialization above, implement your own IRLS algorithm for robust linear regression
    for i in range(iteration) :
        A_t = np.zeros((num, num))
        for j in range(num) :
            alpha_ij = 1 / np.abs(y[j] - x[j].reshape(1,-1) @ w) 
            A_t[j][j] = np.sqrt(alpha_ij)
        w = np.linalg.inv(x.T @ A_t @ x) @ x.T @ A_t @ y
    return w


# Testing script
if __name__ == '__main__':
    data1 = linear_data_simulator(prior='Gauss', noise='Gauss')
    data2 = linear_data_simulator(prior='Laplace', noise='Gauss')
    data3 = linear_data_simulator(prior='Gauss', noise='Laplace')
    w1 = training(data1['train'][0], data1['train'][1], gamma=1)
    w2 = training_sgd(data1['train'][0], data1['train'][1], gamma=1)
    w3 = training_lasso(data2['train'][0], data2['train'][1], gamma=1)
    w4 = training_elastic(data2['train'][0], data2['train'][1], gamma1=1, gamma2=1)
    w5 = training_irls(data3['train'][0], data3['train'][1])

    mse_w1 = mse(data1['real'], w1)
    mse_w2 = mse(data1['real'], w2)
    mse_w3 = mse(data2['real'], w3)
    mse_w4 = mse(data2['real'], w4)
    mse_w5 = mse(data3['real'], w5)

    mse_y1 = testing(data1['test'][0], data1['test'][1], w1)
    mse_y2 = testing(data1['test'][0], data1['test'][1], w2)
    mse_y3 = testing(data2['test'][0], data2['test'][1], w3)
    mse_y4 = testing(data2['test'][0], data2['test'][1], w4)
    mse_y5 = testing(data3['test'][0], data3['test'][1], w5)

    print('Ridge regression, mse-w={:.4f}, mse-y={:.4f}'.format(mse_w1, mse_y1))
    print('Ridge regression (SGD), mse-w={:.4f}, mse-y={:.4f}'.format(mse_w2, mse_y2))
    print('Lasso regularizer, mse-w={:.4f}, mse-y={:.4f}'.format(mse_w3, mse_y3))
    print('Elastic Net regularizer, mse-w={:.4f}, mse-y={:.4f}'.format(mse_w4, mse_y4))
    print('IRLS, mse-w={:.4f}, mse-y={:.4f}'.format(mse_w5, mse_y5))
