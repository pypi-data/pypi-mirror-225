import numpy as np
import math

class LinearRegression:

  def __init__(self, learning_rate = 0.01, max_iters = 100000, tolerance = 1e-10, optimization_method = "SGD"):
    self.learning_rate = learning_rate
    self.max_iters = max_iters
    self.tolerance = tolerance
    self.params = None
    self.bias = None
    self.om = optimization_method

  def h(self, X):
        return np.dot(X, self.params) + self.bias

  def j(self, X, y):
      se = np.mean((self.h(X) - y) ** 2)/2
      return se

  def fit(self, X, Y):
    if self.om == "SGD":
      self.num_features = X.shape[1]
      self.num_samples = X.shape[0]

      self.params = np.zeros(self.num_features)
      self.bias = 0

      if Y.size != self.num_samples:
          raise ValueError("Number of samples in X and Y do not match.")

      iters = 0

      prev_cost = float('inf')

      for _ in range(self.max_iters):
        index = np.random.randint(self.num_samples)
        
        x = X[index]
        y = Y[index]

        predicted = np.dot(x, self.params) + self.bias

        grad_coef = (2/self.num_samples) * np.dot(x.T, predicted - y)
        grad_inte = (2/self.num_samples) * np.sum(predicted - y)

        self.params -= self.learning_rate * grad_coef
        self.bias -= self.learning_rate * grad_inte

        current_cost = self.j(X, Y)

        if abs(current_cost - prev_cost) < self.tolerance:
            break

        prev_cost = current_cost

    elif self.om == "NormalEquations":
      X = np.c_[np.ones((X.shape[0], 1)), X]

      des = np.linalg.inv(X.T.dot(X)).dot(X.T.dot(y))

      self.bias = des[0]
      self.params = des[1:]

  def predict(self, x):
    return np.dot(x, self.params) + self.bias
  

class KMeans:
  def __init__(self, data, k, max_iters=100, tolerance=1e-4):
    def dist(p1, p2):
      return math.sqrt(np.sum((p1 - p2) ** 2))
    n_samples, n_features = data.shape
    centroids = data[np.random.choice(n_samples, k, replace=False)]
    old_centroids = np.zeros((k, n_features))
    labels = np.zeros(n_samples)

    for _ in range(max_iters):
      for i in range(n_samples):
        distances = [dist(data[i], centroid) for centroid in centroids]
        labels[i] = np.argmin(distances)

      old_centroids[:] = centroids

      for i in range(k):
        cluster_points = data[labels == i]
        if len(cluster_points) > 0:
          centroids[i] = np.mean(cluster_points, axis=0)

      if np.allclose(centroids, old_centroids, rtol=tolerance):
        break

    self.centroids = centroids
    self.labels = labels