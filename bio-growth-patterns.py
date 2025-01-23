import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from typing import List, Tuple, Dict
import math
from dataclasses import dataclass

@dataclass
class TreeNode:
    """Represents a point in the tree structure"""
    x: float
    y: float
    angle: float
    length: float
    depth: int

class BioGrowthPatterns:
    def __init__(self):
        self.golden_ratio = (1 + np.sqrt(5)) / 2
        
    def generate_tree(self, 
                     start_pos: Tuple[float, float], 
                     angle: float = 90, 
                     length: float = 1.0,
                     branching_angle: float = 30,
                     depth: int = 8,
                     length_decay: float = 0.7) -> List[Tuple[TreeNode, TreeNode]]:
        """
        Generate fractal tree pattern using recursive branching
        Returns list of line segments (start_node, end_node)
        """
        if depth == 0:
            return []
            
        # Calculate end point of current branch
        x0, y0 = start_pos
        rad_angle = np.radians(angle)
        x1 = x0 + length * np.cos(rad_angle)
        y1 = y0 + length * np.sin(rad_angle)
        
        # Create nodes for current branch
        start_node = TreeNode(x0, y0, angle, length, depth)
        end_node = TreeNode(x1, y1, angle, length, depth)
        current_branch = (start_node, end_node)
        
        # Generate left and right branches
        branches = [current_branch]
        left_branches = self.generate_tree(
            (x1, y1), 
            angle + branching_angle, 
            length * length_decay,
            branching_angle,
            depth - 1,
            length_decay
        )
        right_branches = self.generate_tree(
            (x1, y1), 
            angle - branching_angle, 
            length * length_decay,
            branching_angle,
            depth - 1,
            length_decay
        )
        
        return branches + left_branches + right_branches

    def generate_shell_spiral(self, 
                            n_points: int = 1000, 
                            growth_rate: float = 0.1,
                            spiral_tightness: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate logarithmic spiral pattern similar to nautilus shell
        """
        theta = np.linspace(0, 6*np.pi, n_points)
        # Logarithmic spiral formula: r = a * e^(b*theta)
        r = spiral_tightness * np.exp(growth_rate * theta)
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        return x, y

    def simulate_population_growth(self, 
                                initial_pop: int,
                                growth_rate: float,
                                carrying_capacity: float,
                                time_steps: int,
                                model: str = 'logistic') -> Dict:
        """
        Simulate population growth using different models
        """
        time = np.arange(time_steps)
        population = np.zeros(time_steps)
        population[0] = initial_pop
        
        if model == 'exponential':
            for t in range(1, time_steps):
                population[t] = population[t-1] * (1 + growth_rate)
                
        elif model == 'logistic':
            for t in range(1, time_steps):
                population[t] = population[t-1] + growth_rate * population[t-1] * \
                              (1 - population[t-1]/carrying_capacity)
                              
        elif model == 'allee':
            # Allee effect: population needs minimum size to grow
            allee_threshold = initial_pop * 0.5
            for t in range(1, time_steps):
                allee_factor = (population[t-1] - allee_threshold) / carrying_capacity
                population[t] = population[t-1] + growth_rate * population[t-1] * \
                              allee_factor * (1 - population[t-1]/carrying_capacity)
        
        return {
            'time': time,
            'population': population,
            'model': model,
            'parameters': {
                'initial_pop': initial_pop,
                'growth_rate': growth_rate,
                'carrying_capacity': carrying_capacity
            }
        }

    def visualize_tree(self, branches: List[Tuple[TreeNode, TreeNode]], title: str = "Fractal Tree Pattern"):
        """Visualize tree branching pattern"""
        plt.figure(figsize=(10, 12))
        
        # Plot each branch with color based on depth
        max_depth = max(branch[0].depth for branch in branches)
        for start_node, end_node in branches:
            color = plt.cm.viridis(start_node.depth / max_depth)
            plt.plot([start_node.x, end_node.x], 
                    [start_node.y, end_node.y], 
                    color=color, 
                    linewidth=start_node.depth/2)
        
        plt.title(title)
        plt.axis('equal')
        plt.grid(True, alpha=0.3)
        plt.show()

    def visualize_shell(self, title: str = "Shell Growth Pattern"):
        """Visualize shell spiral patterns"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 15))
        fig.suptitle(title, fontsize=16)
        
        # Different growth patterns
        growth_rates = [0.1, 0.2, 0.15, 0.18]
        tightness = [1.0, 0.8, 1.2, 0.9]
        colors = ['gold', 'coral', 'turquoise', 'violet']
        axes = [ax1, ax2, ax3, ax4]
        
        for ax, rate, tight, color in zip(axes, growth_rates, tightness, colors):
            x, y = self.generate_shell_spiral(growth_rate=rate, spiral_tightness=tight)
            ax.plot(x, y, color=color, linewidth=2)
            ax.set_title(f'Growth Rate: {rate:.2f}, Tightness: {tight:.2f}')
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

    def visualize_population(self, title: str = "Population Growth Patterns"):
        """Visualize different population growth models"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
        fig.suptitle(title, fontsize=16)
        
        # Compare different models
        models = ['exponential', 'logistic', 'allee']
        colors = ['blue', 'green', 'red']
        
        # First plot: Same parameters
        ax1.set_title("Comparison of Growth Models")
        for model, color in zip(models, colors):
            result = self.simulate_population_growth(
                initial_pop=100,
                growth_rate=0.1,
                carrying_capacity=1000,
                time_steps=100,
                model=model
            )
            ax1.plot(result['time'], result['population'], 
                    color=color, label=model.capitalize())
        
        ax1.grid(True)
        ax1.legend()
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Population')
        
        # Second plot: Logistic model with different parameters
        ax2.set_title("Logistic Growth with Different Parameters")
        growth_rates = [0.05, 0.1, 0.2]
        colors = ['lightblue', 'blue', 'darkblue']
        
        for rate, color in zip(growth_rates, colors):
            result = self.simulate_population_growth(
                initial_pop=100,
                growth_rate=rate,
                carrying_capacity=1000,
                time_steps=100,
                model='logistic'
            )
            ax2.plot(result['time'], result['population'], 
                    color=color, label=f'Growth Rate: {rate}')
        
        ax2.grid(True)
        ax2.legend()
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Population')
        
        plt.tight_layout()
        plt.show()

def demonstrate_patterns():
    """Demonstrate various biological growth patterns"""
    bp = BioGrowthPatterns()
    
    # 1. Tree Patterns
    print("Generating tree patterns...")
    # Regular tree
    branches = bp.generate_tree((0, 0), branching_angle=30, depth=8)
    bp.visualize_tree(branches, "Regular Branching Pattern")
    
    # Wide branching tree
    branches_wide = bp.generate_tree((0, 0), branching_angle=45, depth=7)
    bp.visualize_tree(branches_wide, "Wide Branching Pattern")
    
    # 2. Shell Patterns
    print("\nGenerating shell patterns...")
    bp.visualize_shell("Nautilus Shell Growth Patterns")
    
    # 3. Population Patterns
    print("\nGenerating population growth patterns...")
    bp.visualize_population("Population Growth Models")

if __name__ == "__main__":
    demonstrate_patterns()