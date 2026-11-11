import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import random

@dataclass
class TreeNode:
    """Enhanced tree node with environmental response factors"""
    x: float
    y: float
    angle: float
    length: float
    depth: int
    thickness: float
    season: str
    health: float  # 0 to 1
    light_exposure: float  # 0 to 1
    nutrient_level: float  # 0 to 1

class AdvancedTreeModel:
    """Advanced tree growth model with environmental factors"""
    
    # Species-specific growth parameters
    SPECIES_PARAMS = {
        'oak': {
            'base_angle': 35,
            'length_decay': 0.75,
            'max_depth': 8,
            'thickness_decay': 0.6,
            'branching_variation': 0.2,
            'light_sensitivity': 0.8,
            'nutrient_sensitivity': 0.7
        },
        'pine': {
            'base_angle': 45,
            'length_decay': 0.8,
            'max_depth': 10,
            'thickness_decay': 0.7,
            'branching_variation': 0.1,
            'light_sensitivity': 0.6,
            'nutrient_sensitivity': 0.5
        },
        'birch': {
            'base_angle': 40,
            'length_decay': 0.7,
            'max_depth': 9,
            'thickness_decay': 0.65,
            'branching_variation': 0.15,
            'light_sensitivity': 0.7,
            'nutrient_sensitivity': 0.6
        }
    }
    
    # Seasonal effects
    SEASON_EFFECTS = {
        'spring': {
            'growth_modifier': 1.2,
            'health_modifier': 1.1,
            'branching_modifier': 1.1
        },
        'summer': {
            'growth_modifier': 1.0,
            'health_modifier': 1.0,
            'branching_modifier': 1.0
        },
        'autumn': {
            'growth_modifier': 0.8,
            'health_modifier': 0.9,
            'branching_modifier': 0.9
        },
        'winter': {
            'growth_modifier': 0.6,
            'health_modifier': 0.7,
            'branching_modifier': 0.8
        }
    }
    
    def __init__(self, species: str = 'oak'):
        self.species = species
        self.params = self.SPECIES_PARAMS[species]
        
    def calculate_environmental_factor(self, 
                                    depth: int, 
                                    angle: float, 
                                    light_direction: float = 90) -> float:
        """Calculate environmental influence on growth"""
        # Light exposure decreases with depth and depends on angle
        angle_diff = abs(angle - light_direction)
        light_factor = np.cos(np.radians(angle_diff)) * (1 - depth/self.params['max_depth'])
        return max(0.1, light_factor)
        
    def generate_tree(self,
                     start_pos: Tuple[float, float],
                     season: str = 'summer',
                     light_direction: float = 90,
                     nutrient_level: float = 1.0,
                     environmental_stress: float = 0.0) -> List[TreeNode]:
        """Generate tree structure with environmental responses"""
        
        def grow_branch(node: TreeNode) -> List[TreeNode]:
            if node.depth >= self.params['max_depth'] or node.health < 0.1:
                return []
                
            branches = []
            season_effect = self.SEASON_EFFECTS[season]
            
            # Calculate growth factors
            light_effect = (node.light_exposure * self.params['light_sensitivity'])
            nutrient_effect = (node.nutrient_level * self.params['nutrient_sensitivity'])
            growth_factor = season_effect['growth_modifier'] * light_effect * nutrient_effect
            
            # Calculate new length and thickness
            new_length = node.length * self.params['length_decay'] * growth_factor
            new_thickness = node.thickness * self.params['thickness_decay']
            
            # Generate branches with variation
            base_variation = self.params['branching_variation'] * (1 + environmental_stress)
            angles = [
                node.angle + self.params['base_angle'] * (1 + random.uniform(-base_variation, base_variation)),
                node.angle - self.params['base_angle'] * (1 + random.uniform(-base_variation, base_variation))
            ]
            
            for angle in angles:
                # Calculate new position
                dx = new_length * np.cos(np.radians(angle))
                dy = new_length * np.sin(np.radians(angle))
                new_x = node.x + dx
                new_y = node.y + dy
                
                # Calculate new environmental factors
                new_light = self.calculate_environmental_factor(node.depth + 1, angle, light_direction)
                new_health = node.health * season_effect['health_modifier']
                new_nutrients = node.nutrient_level * 0.9  # Nutrients decrease with height
                
                # Create new node
                new_node = TreeNode(
                    x=new_x, y=new_y,
                    angle=angle,
                    length=new_length,
                    depth=node.depth + 1,
                    thickness=new_thickness,
                    season=season,
                    health=new_health,
                    light_exposure=new_light,
                    nutrient_level=new_nutrients
                )
                
                branches.append((node, new_node))
                branches.extend(grow_branch(new_node))
                
            return branches
        
        # Create root node
        root = TreeNode(
            x=start_pos[0], y=start_pos[1],
            angle=90,  # Start growing upward
            length=1.0,
            depth=0,
            thickness=0.2,
            season=season,
            health=1.0,
            light_exposure=1.0,
            nutrient_level=nutrient_level
        )
        
        return grow_branch(root)
    
    def visualize_tree(self, 
                      branches: List[Tuple[TreeNode, TreeNode]], 
                      show_factors: bool = True):
        """Visualize tree with environmental factors"""
        plt.figure(figsize=(15, 10))
        
        # Plot branches
        for start_node, end_node in branches:
            # Color based on health and season
            if start_node.season == 'summer':
                color = plt.cm.YlGn(start_node.health)
            elif start_node.season == 'autumn':
                color = plt.cm.YlOrRd(start_node.health)
            elif start_node.season == 'winter':
                color = plt.cm.Blues(start_node.health)
            else:  # spring
                color = plt.cm.YlGn(start_node.health * 1.2)
                
            # Line width based on thickness
            width = start_node.thickness * 3
            
            plt.plot([start_node.x, end_node.x],
                    [start_node.y, end_node.y],
                    color=color,
                    linewidth=width)
            
            # Optionally show environmental factors
            if show_factors and start_node.depth < 3:
                plt.text(start_node.x, start_node.y,
                        f'L:{start_node.light_exposure:.1f}\nN:{start_node.nutrient_level:.1f}',
                        fontsize=8)
        
        plt.title(f'{self.species.capitalize()} Tree in {branches[0][0].season.capitalize()}')
        plt.axis('equal')
        plt.grid(True, alpha=0.3)
        
    def compare_seasons(self):
        """Compare tree growth across seasons"""
        fig, axes = plt.subplots(2, 2, figsize=(20, 20))
        axes = axes.ravel()
        
        for i, season in enumerate(self.SEASON_EFFECTS.keys()):
            branches = self.generate_tree((0, 0), season=season)
            ax = axes[i]
            
            # Plot branches on the appropriate subplot
            for start_node, end_node in branches:
                if season == 'summer':
                    color = plt.cm.YlGn(start_node.health)
                elif season == 'autumn':
                    color = plt.cm.YlOrRd(start_node.health)
                elif season == 'winter':
                    color = plt.cm.Blues(start_node.health)
                else:  # spring
                    color = plt.cm.YlGn(start_node.health * 1.2)
                    
                width = start_node.thickness * 3
                
                ax.plot([start_node.x, end_node.x],
                       [start_node.y, end_node.y],
                       color=color,
                       linewidth=width)
            
            ax.set_title(f'{season.capitalize()}')
            ax.axis('equal')
            ax.grid(True, alpha=0.3)
        
        plt.suptitle(f'{self.species.capitalize()} Tree Through Seasons', fontsize=16)
        plt.tight_layout()
        
    def compare_species(self, season: str = 'summer'):
        """Compare different tree species"""
        fig, axes = plt.subplots(1, 3, figsize=(24, 8))
        original_species = self.species
        
        for i, species in enumerate(self.SPECIES_PARAMS.keys()):
            self.species = species
            self.params = self.SPECIES_PARAMS[species]
            branches = self.generate_tree((0, 0), season=season)
            
            # Plot on appropriate subplot
            ax = axes[i]
            for start_node, end_node in branches:
                color = plt.cm.YlGn(start_node.health)
                width = start_node.thickness * 3
                
                ax.plot([start_node.x, end_node.x],
                       [start_node.y, end_node.y],
                       color=color,
                       linewidth=width)
            
            ax.set_title(f'{species.capitalize()}')
            ax.axis('equal')
            ax.grid(True, alpha=0.3)
        
        # restore the model's own species (the loop above switches it)
        self.species = original_species
        self.params = self.SPECIES_PARAMS[original_species]
        
        plt.suptitle(f'Different Tree Species in {season.capitalize()}', fontsize=16)
        plt.tight_layout()

def demonstrate_tree_patterns():
    """Demonstrate various tree growth patterns"""
    tree_model = AdvancedTreeModel('oak')
    
    # 1. Basic tree with environmental factors
    print("Generating basic tree with environmental factors...")
    branches = tree_model.generate_tree((0, 0))
    tree_model.visualize_tree(branches)
    plt.show()
    
    # 2. Seasonal comparison
    print("\nComparing seasonal effects...")
    tree_model.compare_seasons()
    plt.show()
    
    # 3. Species comparison
    print("\nComparing different species...")
    tree_model.compare_species()
    plt.show()
    
    # 4. Environmental stress example
    print("\nDemonstrating environmental stress...")
    stressed_branches = tree_model.generate_tree(
        (0, 0),
        nutrient_level=0.5,
        environmental_stress=0.3
    )
    tree_model.visualize_tree(stressed_branches)
    plt.show()

if __name__ == "__main__":
    demonstrate_tree_patterns()