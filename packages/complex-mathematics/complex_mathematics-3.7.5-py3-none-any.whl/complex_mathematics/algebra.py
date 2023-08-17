import re
import math
import numpy as np

def quadratic(equation):
    equation = equation.replace(" ", "")
  
    pattern = r'(-?\d*)x\^2([-+]?\d*)x([-+]?\d+)'
    matches = re.match(pattern, equation)

    if not matches:
        raise ValueError("Invalid quadratic equation format. Please provide a valid quadratic equation.")

    a_str, b_str, c_str = matches.groups()

    a = int(a_str) if a_str and a_str not in '+-' else 1 if not a_str or a_str == '+' else -1
    b = int(b_str) if b_str and b_str not in '+-' else 1 if not b_str or b_str == '+' else -1
    c = int(c_str) if c_str and c_str not in '+-' else 1 if not c_str or c_str == '+' else -1

    try:
        pos = (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
        neg = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)
    except:
        pos, neg = None, None

    if pos == neg:
        return np.array([pos])

    return np.array([pos, neg])

def solve(coefs, step=0.01, tolerance=1e-8, srange=100):
  roots = []
  deg = coefs.shape[0] - 1
  i = 0
  while i <= srange:
    pres = 0
    for j in range(deg+1):
      pres += coefs[j] * i ** (deg - j)
    if abs(pres) < tolerance:
      roots.append(i)
      if i == 0:
        i += step
        continue
    ni = -i
    nres = 0
    for j in range(deg+1):
      nres += coefs[j] * ni ** (deg - j)
    if abs(nres) < tolerance:
      roots.append(ni)
    i += step
    if len(roots) == deg:
      break
      
  return np.array(roots)