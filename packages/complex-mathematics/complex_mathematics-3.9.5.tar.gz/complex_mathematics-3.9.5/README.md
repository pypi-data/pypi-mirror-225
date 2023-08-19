# complex_mathematics

![Version](https://img.shields.io/badge/version-3.7.5-blue)

---

**complex_mathematics is a Python module that can be used for many complex math related problems, with concepts from many different topics in mathematics, such as calculus, linear algebra, geometry, algebra, and more. It also has machine learning algorithms such as linear regression and K-Nearest-Neighbors.**

---

**To get started:**

Install with:

`pip install complex_mathematics`

---

**Linear Algebra:**

`from complex_mathematics.linalg import BLANK`

Eigenvectors:

The eigenvector class has one parameter, the matrix

The eigenvalues attribute holds the eigenvalues

The eigenvectors attribute holds the eigenvectors

```

from complex_mathematics.linalg import eigenvector
import numpy as np

mat = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])

eig = eigenvector(mat) #eigenvector(matrix)

print(eig.eigenvalues)
print(eig.eigenvectors)

```

Matrix Inverse:

The matrix inverse function has one parameter, the matrix

It returns the inverse

```

from complex_mathematics.linalg import inverse
import numpy as np

matrix = np.array([[1, 2], [3, 4]])

inv = inverse(matrix)

print(inv)

```

---

**Machine Learning:**

`from complex_mathematics.ml import BLANK`

Linear Regression:

The LinearRegression class has four parameters, the learning rate with a default 0.01, the max iterations (Only used when using an iterative optimization algorithm) with a default 10000, the tolerance, also for iterative algorithms, and optimization method with a default of stochastic gradient descent

Stochastic Gradient Descent(SGD):

```

import numpy as np
import random
from complex_mathematics.ml import LinearRegression
    

X = np.array([[i] for i in range(-50, 51)])
y = np.array([2*i + 1 + random.uniform(-1, 1) for i in range(-50, 51)])

model = LinearRegression() #LinearRegression(learning_rate = 0.01, max_iters = 10000, tolerance = 1e-10, optimization_method = "SGD")

model.fit(X, y) #model.fit(X, Y)

print(model.predict(10))

```

Normal Equations:

```

import numpy as np
import random
from complex_mathematics.ml import LinearRegression
    

X = np.array([i for i in range(-50, 51)])
y = np.array([2*i + 1 + random.uniform(-1, 1) for i in range(-50, 51)])

model = LinearRegression(optimization_method = "NormalEquations") #LinearRegression(learning_rate = 0.01, max_iters = 10000, tolerance = 1e-10, optimization_method = "SGD")

model.fit(X, y) #model.fit(X, Y)

print(model.predict(10))

```

K-Means Clustering:

The KMeans class has four parameters, the dataset, the number of centroids(k), the max iterations, with a default of 100, and the tolerance, with a default of 10^-4

```

from complex_mathematics.ml import KMeans
import numpy as np

data = np.array([
    [2, 3, 4],
    [3, 5, 6],
    [4, 4, 5],
    [2, 6, 3],
    [7, 2, 1],
    [6, 4, 2],
    [8, 5, 4],
    [9, 4, 3]
])

model = KMeans(data, 6) #KMeans(data, k, max_iters=100, tolerance=1e-4)

print(model.centroids, model.labels)

```

---

**Algebra:**

`from complex_mathematics.algebra import BLANK`

Quadratic Equation Solver:

The quadratic function has one parameter, the equation in string form

It returns the solutions in a numpy array

```

from complex_mathematics.algebra import quadratic

print(quadratic("-x^2-x+12"))

```

Polynomial Solver:

The polynomial solver has four parameters, a numpy array of the coefficients of the equation, the step (how much the current value increases by each iteration), with default 0.01, the tolerance, with default 1e-8, and the range of possible values you want to check(It goes from -srange to srange), with default 100

It returns the solutions in a numpy array

```

import numpy as np
from complex_mathematics.algebra import solve

coefs = np.array([1, 0, -16])

print(solve(coefs)) #solve(coefs, step=0.01, tolerance=1e-8, srange=100)

```

---

**Statistics:**

`from complex_mathematics.stats import BLANK`

Percent Change:

The percent change function has two parameters, the previous value and the new value

It returns the percent change

```

from complex_mathematics.stats import pchange

print(pchange(100, 110)) #pchange(a, b)

```

Mean:

The mean function has one parameter, the data

It returns the mean of the data

```

import numpy as np
from complex_mathematics.stats import mean

a = np.array([5, 15, 20, 25])

print(mean(a))

```

Median:

The median function has one parameter, the data

It returns the median of the data

```

import numpy as np
from complex_mathematics.stats import median

a = np.array([5, 15, 20, 25])

print(median(a))

```

<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](https://github.com/Arnav-MaIhotra/complex_mathematics/blob/main/LICENSE) for more information.
