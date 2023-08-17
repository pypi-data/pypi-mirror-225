import numpy as np
import scipy


class eigenvector:

  def determinant(self, x):
    I = np.eye(self.A.shape[0])

    B = self.A - x * I

    return np.linalg.det(B)

  def eigval(self, tolerance=1e-8):
    eigenvalues = []
    for i in range(1, self.A.shape[0] + 1):
      x_solution = scipy.optimize.fsolve(self.determinant, x0=i)
      for val in x_solution:
        duplicate = False
        for eigenval in eigenvalues:
          if abs(val - eigenval) < tolerance:
            duplicate = True
            break
        if not duplicate:
          eigenvalues.append(val)
    self.eigenvalues = np.array(eigenvalues)

  def eigvec(self):
    self.eigenvectors = []
    I = np.eye(self.A.shape[0])

    for eigenval in self.eigenvalues:
      B = self.A - eigenval * I

      _, _, V = np.linalg.svd(B)
      eigenvector = V[-1]
      eigenvector = eigenvector / np.linalg.norm(eigenvector)
      if eigenvector[0] != 0:
        reciprocal = 1 / eigenvector[0]
        for i in range(len(eigenvector)):
          eigenvector[i] = reciprocal * eigenvector[i]
      self.eigenvectors.append(eigenvector)

    self.eigenvectors = np.array(self.eigenvectors)

  def __init__(self, matrix):
    self.A = matrix
    self.eigenvalues = None
    self.eigval()
    self.eigenvectors = None
    self.eigvec()


def inverse(matrix):
    
    augmented_matrix = np.hstack((matrix, np.identity(matrix.shape[0])))
    
    m, n = augmented_matrix.shape
    for col in range(min(m, n - 1)):
        pivot_row = col

        for row in range(col + 1, m):
            if abs(augmented_matrix[row, col]) > abs(augmented_matrix[pivot_row, col]):
                pivot_row = row

        augmented_matrix[[col, pivot_row]] = augmented_matrix[[pivot_row, col]]

        pivot_elem = augmented_matrix[col, col]
        if pivot_elem == 0:
            raise ValueError("Matrix is singular, cannot proceed.")

        augmented_matrix[col] /= pivot_elem

        for row in range(m):
            if row != col:
                factor = augmented_matrix[row, col]
                augmented_matrix[row] -= factor * augmented_matrix[col]

    
    inverse_matrix = augmented_matrix[:, matrix.shape[0]:]

    return inverse_matrix