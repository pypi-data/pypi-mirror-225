# complex_mathematics

![Version](https://img.shields.io/badge/version-2.4.3-blue)

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

```

from complex_mathematics.linalg import eigenvector
import numpy as np

mat = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])

eig = eigenvector(mat) #eigenvector(matrix)

print(eig.eigenvalues)
print(eig.eigenvectors)

```

---

**Machine Learning:**

`from complex_mathematics.ml import BLANK`

Linear Regression (Stochastic gradient descent):

```

import numpy as np
import random
from complex_mathematics.ml import LinearRegression
    

X = np.array([[i] for i in range(-50, 51)])
y = np.array([2*i + 1 + random.uniform(-1, 1) for i in range(-50, 51)])

model = LinearRegression() #LinearRegression(learning_rate = 0.01, max_iters = 10000, tolerance = 1e-10)

model.fit(X, y, True) #model.fit(X, Y, progress = False)

print(model.predict(10))

```

K-Means Clustering:

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

```

from complex_mathematics.algebra import quadratic

print(quadratic("-x^2-x+12"))

```

---

<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](https://github.com/Arnav-MaIhotra/complex_mathematics/blob/main/LICENSE) for more information.
