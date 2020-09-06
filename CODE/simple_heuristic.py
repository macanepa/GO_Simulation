import numpy as np
def exp(p, lambda_):
    return ((-1/lambda_)*np.log(1 - p))


for i in range(100):
    print(exp(0.5, 5))

