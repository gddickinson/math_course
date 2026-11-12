import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from typing import List, Tuple, Dict

class TreeDataAnalysis:
    """
    Analysis and comparison of example tree branching data with model predictions.
    The data are illustrative example values written for this course, not field measurements.
    """
    
    # Illustrative example values (not measurements; no published source)
    EXAMPLE_TREE_DATA = {
        'oak': {
            'branching_angles': [
                35.2, 37.1, 34.8, 36.5, 33.9, 35.8, 34.2, 36.9, 35.5, 34.7,
                36.2, 35.1, 34.9, 35.7, 36.1, 34.5, 35.9, 34.6, 35.3, 36.4
            ],
            'length_ratios': [
                0.72, 0.75, 0.73, 0.76, 0.74, 0.71, 0.75, 0.73, 0.74, 0.72,
                0.75, 0.73, 0.74, 0.72, 0.75, 0.76, 0.73, 0.74, 0.75, 0.71
            ],
            'thickness_ratios': [
                0.58, 0.61, 0.59, 0.62, 0.60, 0.59, 0.61, 0.58, 0.60, 0.59,
                0.61, 0.60, 0.59, 0.61, 0.58, 0.60, 0.59, 0.61, 0.60, 0.59
            ]
        },
        'pine': {
            'branching_angles': [
                45.5, 44.8, 46.2, 45.1, 44.9, 45.7, 46.1, 44.5, 45.9, 44.6,
                45.3, 46.4, 45.2, 44.7, 45.8, 46.3, 44.4, 45.6, 45.0, 46.5
            ],
            'length_ratios': [
                0.78, 0.81, 0.79, 0.82, 0.80, 0.79, 0.81, 0.78, 0.80, 0.79,
                0.81, 0.80, 0.79, 0.81, 0.78, 0.80, 0.79, 0.81, 0.80, 0.79
            ],
            'thickness_ratios': [
                0.68, 0.71, 0.69, 0.72, 0.70, 0.69, 0.71, 0.68, 0.70, 0.69,
                0.71, 0.70, 0.69, 0.71, 0.68, 0.70, 0.69, 0.71, 0.70, 0.69
            ]
        }
    }
    
    def __init__(self):
        self.model_data = {}
        
    def analyze_branching_patterns(self, species: str) -> Dict:
        """
        Analyze branching patterns of the example data and compare with model
        Returns statistical analysis of branching characteristics
        """
        example_data = self.EXAMPLE_TREE_DATA[species]
        
        analysis = {
            'branching_angles': {
                'mean': np.mean(example_data['branching_angles']),
                'std': np.std(example_data['branching_angles']),
                'ci': stats.t.interval(0.95, len(example_data['branching_angles'])-1,
                                    loc=np.mean(example_data['branching_angles']),
                                    scale=stats.sem(example_data['branching_angles']))
            },
            'length_ratios': {
                'mean': np.mean(example_data['length_ratios']),
                'std': np.std(example_data['length_ratios']),
                'ci': stats.t.interval(0.95, len(example_data['length_ratios'])-1,
                                    loc=np.mean(example_data['length_ratios']),
                                    scale=stats.sem(example_data['length_ratios']))
            },
            'thickness_ratios': {
                'mean': np.mean(example_data['thickness_ratios']),
                'std': np.std(example_data['thickness_ratios']),
                'ci': stats.t.interval(0.95, len(example_data['thickness_ratios'])-1,
                                    loc=np.mean(example_data['thickness_ratios']),
                                    scale=stats.sem(example_data['thickness_ratios']))
            }
        }
        
        return analysis

    def generate_model_predictions(self, species: str, n_samples: int = 20) -> Dict:
        """
        Generate model predictions for comparison with the example data
        """
        # Use the parameters from our previous tree model
        if species == 'oak':
            base_angle = 35
            length_decay = 0.75
            thickness_decay = 0.6
        else:  # pine
            base_angle = 45
            length_decay = 0.8
            thickness_decay = 0.7
            
        # Add some natural variation
        angles = base_angle + np.random.normal(0, 2, n_samples)
        lengths = length_decay + np.random.normal(0, 0.02, n_samples)
        thicknesses = thickness_decay + np.random.normal(0, 0.02, n_samples)
        
        return {
            'branching_angles': angles,
            'length_ratios': lengths,
            'thickness_ratios': thicknesses
        }

    def compare_with_model(self, species: str) -> Dict:
        """
        Compare the example data with model predictions
        Returns statistical comparisons and effect sizes
        """
        example_data = self.EXAMPLE_TREE_DATA[species]
        model_data = self.generate_model_predictions(species)
        
        comparisons = {}
        
        for measure in ['branching_angles', 'length_ratios', 'thickness_ratios']:
            # Perform t-test
            t_stat, p_value = stats.ttest_ind(
                example_data[measure],
                model_data[measure]
            )
            
            # Calculate effect size (Cohen's d)
            d = (np.mean(example_data[measure]) - np.mean(model_data[measure])) / \
                np.sqrt((np.var(example_data[measure]) + np.var(model_data[measure])) / 2)
                
            comparisons[measure] = {
                't_statistic': t_stat,
                'p_value': p_value,
                'effect_size': d
            }
            
        return comparisons

    def visualize_comparisons(self, species: str):
        """
        Create visualizations comparing the example data with model predictions
        """
        example_data = self.EXAMPLE_TREE_DATA[species]
        model_data = self.generate_model_predictions(species)
        
        fig, axes = plt.subplots(1, 3, figsize=(20, 6))
        measures = ['branching_angles', 'length_ratios', 'thickness_ratios']
        titles = ['Branching Angles', 'Length Ratios', 'Thickness Ratios']
        
        for ax, measure, title in zip(axes, measures, titles):
            # Create violin plots
            parts = ax.violinplot([example_data[measure], model_data[measure]],
                                showmeans=True, showextrema=True)
            
            # Customize colors
            parts['bodies'][0].set_facecolor('lightblue')
            parts['bodies'][1].set_facecolor('lightgreen')
            
            # Add box plots inside
            ax.boxplot([example_data[measure], model_data[measure]],
                      positions=[1, 2], widths=0.2)
            
            ax.set_title(title)
            ax.set_xticks([1, 2])
            ax.set_xticklabels(['Example data', 'Model'])
            ax.grid(True, alpha=0.3)
            
        plt.suptitle(f'Comparison of Example and Model Data for {species.capitalize()}')
        plt.tight_layout()

    def visualize_example_tree_structure(self, species: str):
        """
        Create visualization of a tree branching structure built from the example data
        """
        example_data = self.EXAMPLE_TREE_DATA[species]
        
        def plot_branch(ax, start, angle, length, depth=0, max_depth=4):
            if depth >= max_depth:
                return
                
            # Calculate end point
            end = (
                start[0] + length * np.cos(np.radians(angle)),
                start[1] + length * np.sin(np.radians(angle))
            )
            
            # Plot branch
            ax.plot([start[0], end[0]], [start[1], end[1]], 'brown', linewidth=3-depth/2)
            
            # Create sub-branches
            if depth < max_depth:
                angle_left = angle + np.mean(example_data['branching_angles'])
                angle_right = angle - np.mean(example_data['branching_angles'])
                new_length = length * np.mean(example_data['length_ratios'])
                
                plot_branch(ax, end, angle_left, new_length, depth + 1, max_depth)
                plot_branch(ax, end, angle_right, new_length, depth + 1, max_depth)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
        
        # Plot tree structure from the example means
        plot_branch(ax1, (0, 0), 90, 1)
        ax1.set_title(f'{species.capitalize()} Structure (example data)')
        ax1.axis('equal')
        ax1.grid(True, alpha=0.3)
        
        # Plot angle distribution
        ax2.hist(example_data['branching_angles'], bins=15, color='lightblue',
                alpha=0.7, density=True)
        ax2.set_title('Branching Angle Distribution')
        ax2.set_xlabel('Angle (degrees)')
        ax2.set_ylabel('Density')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()

def demonstrate_analysis():
    """Show analysis of the example tree data and model comparisons"""
    analyzer = TreeDataAnalysis()
    
    for species in ['oak', 'pine']:
        print(f"\nAnalyzing {species.capitalize()} Trees:")
        
        # 1. Basic analysis of the example data
        print("\nExample Data Analysis (illustrative values):")
        analysis = analyzer.analyze_branching_patterns(species)
        for measure, stats in analysis.items():
            print(f"\n{measure}:")
            print(f"Mean: {stats['mean']:.2f}")
            print(f"Std Dev: {stats['std']:.2f}")
            print(f"95% CI: ({stats['ci'][0]:.2f}, {stats['ci'][1]:.2f})")
        
        # 2. Compare with model
        print("\nModel Comparison:")
        comparisons = analyzer.compare_with_model(species)
        for measure, stats in comparisons.items():
            print(f"\n{measure}:")
            print(f"t-statistic: {stats['t_statistic']:.3f}")
            print(f"p-value: {stats['p_value']:.3f}")
            print(f"Effect size: {stats['effect_size']:.3f}")
        
        # 3. Visualizations
        print("\nGenerating visualizations...")
        analyzer.visualize_comparisons(species)
        plt.show()
        
        analyzer.visualize_example_tree_structure(species)
        plt.show()

if __name__ == "__main__":
    demonstrate_analysis()