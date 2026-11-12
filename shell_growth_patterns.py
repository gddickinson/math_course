import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from dataclasses import dataclass

@dataclass
class ShellParameters:
    """Parameters defining shell growth patterns"""
    species: str
    growth_rate: float  # Rate of spiral expansion
    whorl_spacing: float  # Space between successive whorls
    aperture_growth: float  # Rate of aperture expansion
    coiling_axis: float  # Angle of coiling axis
    surface_pattern: str  # Type of surface pattern

class ShellGrowthAnalysis:
    """Analysis of shell growth patterns across different species"""
    
    # Illustrative example parameters (not fitted to measured shells)
    SPECIES_PARAMETERS = {
        'nautilus': ShellParameters(
            species='Nautilus pompilius',
            growth_rate=0.17,  # radius x e^(2*pi*0.17) ~ 2.9 per whorl (a golden spiral would be b ~ 0.306)
            whorl_spacing=0.33,
            aperture_growth=1.05,
            coiling_axis=0.0,
            surface_pattern='chambers'
        ),
        'ammonite': ShellParameters(
            species='Ammonite fossil',
            growth_rate=0.16,
            whorl_spacing=0.31,
            aperture_growth=1.04,
            coiling_axis=0.0,
            surface_pattern='ribs'
        ),
        'gastropod': ShellParameters(
            species='Turritella communis',
            growth_rate=0.2,
            whorl_spacing=0.4,
            aperture_growth=1.1,
            coiling_axis=15.0,  # Helicospiral
            surface_pattern='smooth'
        )
    }
    
    def __init__(self):
        self.golden_ratio = (1 + np.sqrt(5)) / 2
    
    def generate_shell_spiral(self,
                            params: ShellParameters,
                            n_points: int = 1000,
                            n_whorls: int = 4) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate 3D spiral coordinates for shell shape
        """
        # Generate spiral parameters
        t = np.linspace(0, n_whorls * 2 * np.pi, n_points)
        
        # Calculate growth factor
        growth_factor = np.exp(params.growth_rate)
        
        # Generate basic logarithmic spiral
        r = growth_factor**t
        
        # Calculate 3D coordinates
        x = r * np.cos(t)
        y = r * np.sin(t)
        
        # Add height component for species with non-zero coiling axis
        z = t * np.tan(np.radians(params.coiling_axis)) * params.whorl_spacing
        
        return x, y, z
    
    def calculate_growth_metrics(self, params: ShellParameters) -> Dict:
        """
        Calculate key growth metrics for shell
        """
        metrics = {
            'growth_ratio': np.exp(2 * np.pi * params.growth_rate),
            'golden_ratio_deviation': abs(np.exp(2 * np.pi * params.growth_rate) - self.golden_ratio),
            'whorl_expansion_rate': params.aperture_growth,
            'volume_increase_rate': params.aperture_growth**3
        }
        
        return metrics
    
    def analyze_surface_pattern(self, params: ShellParameters, r: np.ndarray, t: np.ndarray) -> np.ndarray:
        """
        Generate surface pattern variations
        """
        if params.surface_pattern == 'chambers':
            # Nautilus-like chamber pattern
            pattern = np.sin(t * 8) * 0.1 * r
        elif params.surface_pattern == 'ribs':
            # Ammonite-like ribbing
            pattern = np.sin(t * 20) * 0.05 * r
        else:
            # Smooth pattern
            pattern = np.zeros_like(r)
            
        return pattern
    
    def visualize_shell(self, params: ShellParameters):
        """
        Create 3D visualization of shell
        """
        fig = plt.figure(figsize=(15, 5))
        
        # Generate shell coordinates
        x, y, z = self.generate_shell_spiral(params)
        
        # Create three views: top, side, and 3D
        # Top view
        ax1 = fig.add_subplot(131)
        ax1.plot(x, y, 'b-', linewidth=1)
        ax1.set_title(f'{params.species}\nTop View')
        ax1.axis('equal')
        ax1.grid(True)
        
        # Side view
        ax2 = fig.add_subplot(132)
        ax2.plot(x, z, 'b-', linewidth=1)
        ax2.set_title('Side View')
        ax2.axis('equal')
        ax2.grid(True)
        
        # 3D view
        ax3 = fig.add_subplot(133, projection='3d')
        ax3.plot(x, y, z, 'b-', linewidth=1)
        ax3.set_title('3D View')
        
        plt.tight_layout()
        plt.show()
    
    def compare_species(self):
        """
        Compare growth patterns of different species
        """
        fig = plt.figure(figsize=(15, 10))
        
        for i, (species, params) in enumerate(self.SPECIES_PARAMETERS.items(), 1):
            # Calculate metrics
            metrics = self.calculate_growth_metrics(params)
            
            # Generate shell coordinates
            x, y, z = self.generate_shell_spiral(params)
            
            # Create subplot
            ax = fig.add_subplot(2, 2, i)
            scatter = ax.scatter(x, y, c=z, cmap='viridis')
            ax.set_title(f'{species}\nGrowth Ratio: {metrics["growth_ratio"]:.3f}')
            ax.axis('equal')
            ax.grid(True)
            
            # Add colorbar
            plt.colorbar(scatter, ax=ax, label='Height')
        
        # Add comparison metrics
        ax = fig.add_subplot(2, 2, 4)
        ax.axis('off')
        metrics_text = ""
        for species, params in self.SPECIES_PARAMETERS.items():
            metrics = self.calculate_growth_metrics(params)
            metrics_text += f"\n{species}:\n"
            metrics_text += f"Growth Ratio: {metrics['growth_ratio']:.3f}\n"
            metrics_text += f"Golden Ratio Deviation: {metrics['golden_ratio_deviation']:.3f}\n"
            metrics_text += f"Whorl Expansion: {metrics['whorl_expansion_rate']:.3f}\n"
            
        ax.text(0.1, 0.1, metrics_text, fontsize=10, verticalalignment='bottom')
        
        plt.suptitle('Comparison of Shell Growth Patterns', fontsize=16)
        plt.tight_layout()
        plt.show()
    
    def analyze_growth_evolution(self, params: ShellParameters, time_steps: int = 5):
        """
        Visualize shell growth over time
        """
        fig = plt.figure(figsize=(15, 5))
        
        for i, whorl in enumerate(np.linspace(1, 4, time_steps), 1):
            ax = fig.add_subplot(1, time_steps, i)
            
            # Generate partial shell
            x, y, z = self.generate_shell_spiral(params, n_whorls=whorl)
            
            ax.plot(x, y, 'b-', linewidth=1)
            ax.set_title(f'Stage {i}\n({whorl:.1f} whorls)')
            ax.axis('equal')
            ax.grid(True)
        
        plt.suptitle(f'Growth Evolution of {params.species}', fontsize=16)
        plt.tight_layout()
        plt.show()

def demonstrate_shell_analysis():
    """Demonstrate shell growth pattern analysis"""
    analyzer = ShellGrowthAnalysis()
    
    # 1. Compare different species
    print("Comparing different species...")
    analyzer.compare_species()
    
    # 2. Detailed analysis of each species
    for species, params in analyzer.SPECIES_PARAMETERS.items():
        print(f"\nAnalyzing {species}...")
        print("Growth metrics:")
        metrics = analyzer.calculate_growth_metrics(params)
        for metric, value in metrics.items():
            print(f"{metric}: {value:.3f}")
        
        # Visualize individual shell
        analyzer.visualize_shell(params)
        
        # Show growth evolution
        analyzer.analyze_growth_evolution(params)

if __name__ == "__main__":
    demonstrate_shell_analysis()