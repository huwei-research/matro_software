"""Run with an installed MATRO package, from any directory."""
from matro import minimize

def objective(x):
    return (1-x[0])**2 + 100*(x[1]-x[0]**2)**2

if __name__ == '__main__':
    result = minimize(objective, [-1.2, 1.], maxfev=1500)
    print(result.x, result.fun, result.nfev, result.message)
