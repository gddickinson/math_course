import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AncientMathVisualizer:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Ancient Mathematics Visualizer")
        self.root.geometry("1200x800")
        
        # Create frames
        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.pack(fill=tk.X)
        
        self.output_frame = ttk.Frame(self.root, padding="10")
        self.output_frame.pack(fill=tk.BOTH, expand=True)
        
        self._setup_controls()
        self._setup_output_area()
        
    def _setup_controls(self):
        # Egyptian Multiplication controls
        ttk.Label(self.control_frame, text="Egyptian Multiplication:").grid(row=0, column=0, padx=5)
        self.mult1 = ttk.Entry(self.control_frame, width=10)
        self.mult1.grid(row=0, column=1, padx=5)
        self.mult1.insert(0, "14")
        
        ttk.Label(self.control_frame, text="×").grid(row=0, column=2, padx=5)
        self.mult2 = ttk.Entry(self.control_frame, width=10)
        self.mult2.grid(row=0, column=3, padx=5)
        self.mult2.insert(0, "12")
        
        ttk.Button(self.control_frame, text="Calculate Multiplication", 
                  command=self.show_egyptian_mult).grid(row=0, column=4, padx=5)
        
        # Babylonian Square Root controls
        ttk.Label(self.control_frame, text="Babylonian Square Root:").grid(row=1, column=0, padx=5)
        self.sqrt_num = ttk.Entry(self.control_frame, width=10)
        self.sqrt_num.grid(row=1, column=1, padx=5)
        self.sqrt_num.insert(0, "2")
        
        ttk.Button(self.control_frame, text="Calculate Square Root", 
                  command=self.show_babylonian_sqrt).grid(row=1, column=4, padx=5)
        
    def _setup_output_area(self):
        # Create text area for steps
        self.text_output = tk.Text(self.output_frame, height=10, width=50)
        self.text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create figure for visualization
        self.fig = plt.Figure(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.output_frame)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
    def egyptian_multiply(self, a, b):
        steps = []
        result = 0
        
        while b > 0:
            steps.append({
                'multiplier': b,
                'multiplicand': a,
                'include': bool(b & 1)
            })
            if b & 1:
                result += a
            a *= 2
            b //= 2
            
        return steps, result
    
    def show_egyptian_mult(self):
        try:
            a = int(self.mult1.get())
            b = int(self.mult2.get())
        except ValueError:
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, "Please enter valid numbers")
            return
        
        steps, result = self.egyptian_multiply(a, b)
        
        # Clear previous output
        self.text_output.delete(1.0, tk.END)
        self.fig.clear()
        
        # Text output
        self.text_output.insert(tk.END, f"Multiplying {a} × {b}\n\n")
        self.text_output.insert(tk.END, "Step-by-step process:\n")
        self.text_output.insert(tk.END, "Multiplier  Multiplicand  Include\n")
        self.text_output.insert(tk.END, "-" * 40 + "\n")
        
        for step in steps:
            include = "Yes" if step['include'] else "No"
            self.text_output.insert(tk.END, 
                f"{step['multiplier']:^10d} {step['multiplicand']:^12d} {include:^8s}\n")
        
        self.text_output.insert(tk.END, f"\nResult: {result}")
        
        # Visualization
        ax = self.fig.add_subplot(111)
        
        # Create rectangle visualization
        y_pos = len(steps)
        for step in steps:
            if step['include']:
                rect = Rectangle((0, y_pos-0.5), step['multiplicand'], 0.8, 
                               facecolor='lightblue', edgecolor='blue')
                ax.add_patch(rect)
                ax.text(step['multiplicand']/2, y_pos, 
                       f"{step['multiplicand']}", ha='center', va='center')
            y_pos -= 1
            
        ax.set_xlim(0, max(step['multiplicand'] for step in steps) * 1.1)
        ax.set_ylim(0, len(steps) + 1)
        ax.set_title(f"Egyptian Multiplication: {a} × {b}")
        ax.set_xlabel("Value")
        ax.set_ylabel("Step")
        
        self.canvas.draw()
        
    def babylonian_sqrt(self, n, iterations=10):
        steps = []
        x = n / 2  # Initial guess
        
        for i in range(iterations):
            next_x = (x + n/x) / 2
            steps.append({
                'iteration': i + 1,
                'estimate': next_x,
                'error': abs(next_x - x)
            })
            
            if abs(next_x - x) < 1e-10:
                break
                
            x = next_x
            
        return steps
        
    def show_babylonian_sqrt(self):
        try:
            n = float(self.sqrt_num.get())
        except ValueError:
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, "Please enter a valid number")
            return
        
        steps = self.babylonian_sqrt(n)
        
        # Clear previous output
        self.text_output.delete(1.0, tk.END)
        self.fig.clear()
        
        # Text output
        self.text_output.insert(tk.END, f"Calculating square root of {n}\n\n")
        self.text_output.insert(tk.END, "Step-by-step process:\n")
        self.text_output.insert(tk.END, "Iteration  Estimate      Error\n")
        self.text_output.insert(tk.END, "-" * 35 + "\n")
        
        for step in steps:
            self.text_output.insert(tk.END,
                f"{step['iteration']:^9d} {step['estimate']:^12.6f} {step['error']:^12.6g}\n")
        
        # Visualization
        ax1 = self.fig.add_subplot(121)
        ax2 = self.fig.add_subplot(122)
        
        # Convergence plot
        iterations = range(1, len(steps) + 1)
        estimates = [step['estimate'] for step in steps]
        errors = [step['error'] for step in steps]
        
        ax1.plot(iterations, estimates, 'bo-')
        ax1.axhline(y=np.sqrt(n), color='r', linestyle='--', label=f'√{n}')
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Estimate')
        ax1.set_title('Convergence of Estimates')
        ax1.grid(True)
        ax1.legend()
        
        ax2.semilogy(iterations, errors, 'go-')
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Error (log scale)')
        ax2.set_title('Error Convergence')
        ax2.grid(True)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AncientMathVisualizer()
    app.run()
