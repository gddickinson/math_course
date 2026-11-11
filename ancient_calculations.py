import numpy as np
import matplotlib.pyplot as plt

class EgyptianMultiplication:
    """
    Implementation of Egyptian multiplication method (also known as Russian Peasant Multiplication)
    This method only requires the ability to multiply and divide by 2, and to add numbers.
    """
    def __init__(self, multiplicand, multiplier):
        self.multiplicand = multiplicand
        self.multiplier = multiplier
        self.steps = []
        
    def multiply(self):
        """Perform Egyptian multiplication, recording each step"""
        a, b = self.multiplicand, self.multiplier
        result = 0
        self.steps = []  # start a fresh table on every call
        
        while b > 0:
            self.steps.append({
                'multiplier': b,
                'multiplicand': a,
                'include': bool(b & 1)  # Check if odd
            })
            
            if b & 1:  # If b is odd
                result += a
            
            a *= 2
            b //= 2
            
        return result
    
    def show_work(self):
        """Display the multiplication process"""
        result = self.multiply()  # fills self.steps
        print(f"\nMultiplying {self.multiplicand} × {self.multiplier}")
        print("\nEgyptian method steps:")
        print("Multiplier  Multiplicand  Include in sum")
        print("-" * 40)
        
        for step in self.steps:
            include = "Yes" if step['include'] else "No"
            print(f"{step['multiplier']:^10d} {step['multiplicand']:^12d} {include:^13s}")
            
        print(f"\nResult: {result}")


class BabylonianSquareRoot:
    """
    Implementation of Babylonian method for calculating square roots
    This is one of the earliest known numerical algorithms
    """
    def __init__(self, number, iterations=10):
        self.number = number
        self.iterations = iterations
        self.steps = []
        
    def calculate(self):
        """Calculate square root using Babylonian method"""
        if self.number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        self.steps = []  # start a fresh table on every call
        if self.number == 0:
            return 0.0  # the initial guess n/2 would divide by zero
            
        # Initial guess - Babylonians often used this simple but effective starting point
        x = self.number / 2
        
        for i in range(self.iterations):
            next_x = (x + self.number / x) / 2
            self.steps.append({
                'iteration': i + 1,
                'estimate': next_x,
                'error': abs(next_x - x)
            })
            
            if abs(next_x - x) < 1e-10:  # Convergence check
                break
                
            x = next_x
            
        return x
    
    def show_work(self):
        """Display the square root calculation process"""
        result = self.calculate()
        print(f"\nCalculating square root of {self.number}")
        print("\nBabylonian method steps:")
        print("Iteration  Estimate      Error")
        print("-" * 35)
        
        for step in self.steps:
            print(f"{step['iteration']:^9d} {step['estimate']:^12.6f} {step['error']:^12.6g}")
            
        print(f"\nFinal result: {result:,.6f}")
        
    def plot_convergence(self):
        """Plot the convergence of the square root estimation"""
        iterations = range(1, len(self.steps) + 1)
        errors = [step['error'] for step in self.steps]
        
        plt.figure(figsize=(10, 6))
        plt.semilogy(iterations, errors, 'bo-')
        plt.grid(True)
        plt.xlabel('Iteration')
        plt.ylabel('Error (log scale)')
        plt.title(f'Convergence of Babylonian Square Root Method for √{self.number}')
        plt.show()


def demonstrate_calculations():
    """Demonstrate both calculation methods with examples"""
    # Egyptian Multiplication Example
    print("Egyptian Multiplication Example:")
    egypt_mult = EgyptianMultiplication(14, 12)
    egypt_mult.show_work()
    
    # Babylonian Square Root Example
    print("\nBabylonian Square Root Example:")
    babylon_sqrt = BabylonianSquareRoot(2)
    babylon_sqrt.show_work()
    babylon_sqrt.plot_convergence()

if __name__ == "__main__":
    demonstrate_calculations()
