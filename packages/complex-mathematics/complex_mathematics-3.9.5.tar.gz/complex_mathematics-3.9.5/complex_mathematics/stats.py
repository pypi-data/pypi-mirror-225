import numpy as np
import math

def pchange(a, b):
  return (b - a) / a * 100

def mean(data):
  sum = 0
  for i in data:
    sum += i
  sum /= data.shape[0]
  return sum
  

def median(data):
  sorted_data = sorted(data)
  n = len(sorted_data)
  
  if n % 2 == 1:
    return sorted_data[n // 2]
  else:
    middle_right = n // 2
    middle_left = middle_right - 1
    return (sorted_data[middle_left] + sorted_data[middle_right]) / 2
  
def sd(data):
  mu = mean(data)
  sum = 0
  for i in data:
    sum += ((i - mu) ** 2)
  sum /= (data.shape[0] - 1)
  res = math.sqrt(sum)
  
  return res