"""
SCALED SOLAR SYSTEM MODEL
Professional Educational Tool for Space Science Training

Generates multiple visualizations showing:
- Planet positions and sizes
- Orbital mechanics
- Comparative scaling methods
- Planet reference data
"""

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import MaxNLocator
import numpy as np
import csv
from datetime import datetime

# =============================================================================
# PLANET DATA (from training material)
# =============================================================================
PLANETS = {
    'Mercury': {
        'diameter_km': 4879,
        'distance_au': 0.4,
        'orbital_period_days': 88,
        'color': '#8C7853',
        'type': 'Terrestrial',
        'temp_min': -160,
        'temp_max': 430,
    },
    'Venus': {
        'diameter_km': 12104,
        'distance_au': 0.7,
        'orbital_period_days': 225,
        'color': '#FFC649',
        'type': 'Terrestrial',
        'temp_min': 480,
        'temp_max': 480,
    },
    'Earth': {
        'diameter_km': 12742,
        'distance_au': 1.0,
        'orbital_period_days': 365.25,
        'color': '#4A90E2',
        'type': 'Terrestrial',
        'temp_min': -89,
        'temp_max': 70,
    },
    'Mars': {
        'diameter_km': 6779,
        'distance_au': 1.52,
        'orbital_period_days': 687,
        'color': '#E27B58',
        'type': 'Terrestrial',
        'temp_min': -143,
        'temp_max': -35,
    },
    'Jupiter': {
        'diameter_km': 139820,
        'distance_au': 5.2,
        'orbital_period_days': 4333,
        'color': '#C88B3A',
        'type': 'Gas Giant',
        'temp_min': -108,
        'temp_max': 24,
    },
    'Saturn': {
        'diameter_km': 116460,
        'distance_au': 9.5,
        'orbital_period_days': 10759,
        'color': '#EAD6A5',
        'type': 'Gas Giant',
        'temp_min': -140,
        'temp_max': -80,
    },
    'Uranus': {
        'diameter_km': 50724,
        'distance_au': 19.2,
        'orbital_period_days': 30688,
        'color': '#4FD0E7',
        'type': 'Ice Giant',
        'temp_min': -197,
        'temp_max': -197,
    },
    'Neptune': {
        'diameter_km': 49244,
        'distance_au': 30.1,
        'orbital_period_days': 60182,
        'color': '#4B70DD',
        'type': 'Ice Giant',
        'temp_min': -197,
        'temp_max': -200,
    },
}

SUN_DIAMETER_KM = 1391000
SUN_COLOR = '#FDB813'


# =============================================================================
# CORE MODEL CLASS
# =============================================================================
class SolarSystemModel:
    """Calculate positions, scale sizes, manage orbital mechanics"""
    
    def __init__(self):
        self.reference_date = datetime(2024, 1, 1)
    
    def calculate_position(self, planet_name, day=0):
        """
        Calculate planet position at given day
        Returns (x_au, y_au) coordinates
        """
        planet = PLANETS[planet_name]
        period = planet['orbital_period_days']
        
        # Angle in radians (0 to 2π)
        angle = (day % period) / period * 2 * math.pi
        
        # Position in AU
        distance = planet['distance_au']
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)
        
        return x, y
    
    def scale_distance(self, au, scale_factor=30):
        """Convert AU to display units"""
        return au * scale_factor
    
    def scale_size_logarithmic(self, diameter_km):
        """
        Scale planet size using logarithm
        Makes small planets visible while showing size differences
        """
        if diameter_km <= 0:
            return 0.1
        return max(0.3, math.log10(diameter_km) / 1.8)
    
    def get_planet_info(self, planet_name):
        """Return planet data"""
        return PLANETS[planet_name]


# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================

def plot_full_solar_system():
    """
    Main visualization: All 8 planets with Sun
    Shows orbital paths and planet positions
    """
    model = SolarSystemModel()
    
    fig, ax = plt.subplots(figsize=(16, 16), dpi=100)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # DRAW SUN
    sun_radius = model.scale_size_logarithmic(SUN_DIAMETER_KM)
    sun = patches.Circle((0, 0), sun_radius, color=SUN_COLOR, zorder=100)
    ax.add_patch(sun)
    ax.text(0, -sun_radius - 1.5, 'Sun', ha='center', fontsize=10, 
            weight='bold', family='monospace')
    
    # DRAW PLANETS
    for planet_name in sorted(PLANETS.keys()):
        planet = PLANETS[planet_name]
        
        # Orbital path
        orbit_radius = model.scale_distance(planet['distance_au'])
        orbit_circle = patches.Circle((0, 0), orbit_radius, fill=False, 
                                     edgecolor='#CCCCCC', linewidth=0.8, 
                                     linestyle='-', alpha=0.5)
        ax.add_patch(orbit_circle)
        
        # Planet position (day 0)
        x_au, y_au = model.calculate_position(planet_name, day=0)
        x_display = model.scale_distance(x_au)
        y_display = model.scale_distance(y_au)
        
        # Planet circle
        planet_radius = model.scale_size_logarithmic(planet['diameter_km'])
        planet_circle = patches.Circle((x_display, y_display), planet_radius,
                                       color=planet['color'], zorder=50,
                                       edgecolor='#333333', linewidth=0.8)
        ax.add_patch(planet_circle)
        
        # Label
        label_y = y_display + planet_radius + 1.2
        ax.text(x_display, label_y, planet_name, ha='center', fontsize=9,
                weight='bold', family='monospace')
    
    # FORMATTING
    ax.set_xlim(-35, 35)
    ax.set_ylim(-35, 35)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.1, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.title('SCALED SOLAR SYSTEM\nAll 8 Planets (Day 0)', 
             fontsize=16, weight='bold', pad=20, family='monospace')
    
    plt.tight_layout()
    plt.savefig('solar_system_complete.png', dpi=150, facecolor='white', 
               bbox_inches='tight')
    print('✓ Saved: solar_system_complete.png')
    plt.close()


def plot_inner_planets():
    """
    Close-up view of terrestrial planets
    Mercury, Venus, Earth, Mars
    """
    model = SolarSystemModel()
    
    fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # SUN
    sun_radius = model.scale_size_logarithmic(SUN_DIAMETER_KM)
    sun = patches.Circle((0, 0), sun_radius, color=SUN_COLOR, zorder=100)
    ax.add_patch(sun)
    
    # INNER PLANETS ONLY
    inner = ['Mercury', 'Venus', 'Earth', 'Mars']
    
    for planet_name in inner:
        planet = PLANETS[planet_name]
        
        orbit_radius = model.scale_distance(planet['distance_au'])
        orbit_circle = patches.Circle((0, 0), orbit_radius, fill=False,
                                     edgecolor='#CCCCCC', linewidth=0.8,
                                     linestyle='-', alpha=0.5)
        ax.add_patch(orbit_circle)
        
        x_au, y_au = model.calculate_position(planet_name, day=0)
        x_display = model.scale_distance(x_au)
        y_display = model.scale_distance(y_au)
        
        planet_radius = model.scale_size_logarithmic(planet['diameter_km'])
        planet_circle = patches.Circle((x_display, y_display), planet_radius,
                                       color=planet['color'], zorder=50,
                                       edgecolor='#333333', linewidth=0.8)
        ax.add_patch(planet_circle)
        
        ax.text(x_display, y_display + planet_radius + 0.8, planet_name,
               ha='center', fontsize=9, weight='bold', family='monospace')
    
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.1, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.title('INNER PLANETS (Terrestrial)\nMercury, Venus, Earth, Mars',
             fontsize=14, weight='bold', pad=20, family='monospace')
    
    plt.tight_layout()
    plt.savefig('solar_system_inner.png', dpi=150, facecolor='white',
               bbox_inches='tight')
    print('✓ Saved: solar_system_inner.png')
    plt.close()


def plot_outer_planets():
    """
    View of giant planets
    Jupiter, Saturn, Uranus, Neptune
    """
    model = SolarSystemModel()
    
    fig, ax = plt.subplots(figsize=(14, 14), dpi=100)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # SUN
    sun_radius = model.scale_size_logarithmic(SUN_DIAMETER_KM)
    sun = patches.Circle((0, 0), sun_radius, color=SUN_COLOR, zorder=100)
    ax.add_patch(sun)
    
    # OUTER PLANETS ONLY
    outer = ['Jupiter', 'Saturn', 'Uranus', 'Neptune']
    
    for planet_name in outer:
        planet = PLANETS[planet_name]
        
        orbit_radius = model.scale_distance(planet['distance_au'])
        orbit_circle = patches.Circle((0, 0), orbit_radius, fill=False,
                                     edgecolor='#CCCCCC', linewidth=0.8,
                                     linestyle='-', alpha=0.5)
        ax.add_patch(orbit_circle)
        
        x_au, y_au = model.calculate_position(planet_name, day=0)
        x_display = model.scale_distance(x_au)
        y_display = model.scale_distance(y_au)
        
        planet_radius = model.scale_size_logarithmic(planet['diameter_km'])
        planet_circle = patches.Circle((x_display, y_display), planet_radius,
                                       color=planet['color'], zorder=50,
                                       edgecolor='#333333', linewidth=0.8)
        ax.add_patch(planet_circle)
        
        ax.text(x_display, y_display + planet_radius + 1.2, planet_name,
               ha='center', fontsize=10, weight='bold', family='monospace')
    
    ax.set_xlim(-35, 35)
    ax.set_ylim(-35, 35)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.1, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.title('OUTER PLANETS (Gas & Ice Giants)\nJupiter, Saturn, Uranus, Neptune',
             fontsize=14, weight='bold', pad=20, family='monospace')
    
    plt.tight_layout()
    plt.savefig('solar_system_outer.png', dpi=150, facecolor='white',
               bbox_inches='tight')
    print('✓ Saved: solar_system_outer.png')
    plt.close()


def plot_size_comparison():
    """
    Show actual relative sizes of planets
    Demonstrates scale differences
    """
    model = SolarSystemModel()
    
    fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Sort by diameter
    planets_by_size = sorted(PLANETS.items(), 
                            key=lambda x: x[1]['diameter_km'], 
                            reverse=True)
    
    # Position planets horizontally
    x_positions = np.linspace(1, 15, len(planets_by_size))
    
    for idx, (planet_name, planet) in enumerate(planets_by_size):
        x = x_positions[idx]
        
        # Scale size (relative to largest)
        radius = model.scale_size_logarithmic(planet['diameter_km']) * 1.5
        
        circle = patches.Circle((x, 5), radius, color=planet['color'],
                               edgecolor='#333333', linewidth=1, zorder=50)
        ax.add_patch(circle)
        
        # Label
        ax.text(x, 0.5, planet_name, ha='center', fontsize=10,
               weight='bold', family='monospace')
        ax.text(x, 9.5, f"{planet['diameter_km']:,} km", ha='center',
               fontsize=8, family='monospace', color='#666666')
    
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title('RELATIVE PLANET SIZES\n(Not to distance scale)',
             fontsize=14, weight='bold', pad=20, family='monospace')
    
    plt.tight_layout()
    plt.savefig('solar_system_sizes.png', dpi=150, facecolor='white',
               bbox_inches='tight')
    print('✓ Saved: solar_system_sizes.png')
    plt.close()


def export_planet_data():
    """
    Export all planet data to CSV file
    """
    with open('planet_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(['Planet', 'Type', 'Diameter (km)', 'Distance (AU)', 
                        'Orbital Period (days)', 'Orbital Period (years)',
                        'Temp Min (°C)', 'Temp Max (°C)', 'Color Code'])
        
        # Data
        for planet_name in sorted(PLANETS.keys()):
            p = PLANETS[planet_name]
            writer.writerow([
                planet_name,
                p['type'],
                p['diameter_km'],
                p['distance_au'],
                p['orbital_period_days'],
                round(p['orbital_period_days'] / 365.25, 2),
                p['temp_min'],
                p['temp_max'],
                p['color'],
            ])
    
    print('✓ Saved: planet_data.csv')


def print_planet_statistics():
    """
    Print detailed statistics about planets
    """
    print('\n' + '='*70)
    print('SOLAR SYSTEM STATISTICS')
    print('='*70)
    
    model = SolarSystemModel()
    
    for planet_name in sorted(PLANETS.keys()):
        p = PLANETS[planet_name]
        
        print(f'\n{planet_name.upper()}')
        print('-' * 50)
        print(f'  Type:              {p["type"]}')
        print(f'  Diameter:          {p["diameter_km"]:>15,} km')
        print(f'  Distance from Sun: {p["distance_au"]:>15} AU')
        print(f'  Orbital Period:    {p["orbital_period_days"]:>15.2f} days ' + 
              f'({p["orbital_period_days"]/365.25:.2f} years)')
        print(f'  Temperature:       {p["temp_min"]:>15}°C to {p["temp_max"]}°C')
        print(f'  Color (hex):       {p["color"]:>15}')


# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == '__main__':
    print('\n' + '='*70)
    print('SCALED SOLAR SYSTEM MODEL')
    print('Educational Training Tool for Space Science')
    print('='*70)
    
    print('\nGenerating visualizations...\n')
    
    print('[1/4] Complete solar system...')
    plot_full_solar_system()
    
    print('[2/4] Inner planets (close-up)...')
    plot_inner_planets()
    
    print('[3/4] Outer planets (close-up)...')
    plot_outer_planets()
    
    print('[4/4] Planet size comparison...')
    plot_size_comparison()
    
    print('\nExporting data...')
    export_planet_data()
    
    print('\nPrinting statistics...')
    print_planet_statistics()
    
    print('\n' + '='*70)
    print('OUTPUT FILES GENERATED:')
    print('='*70)
    print('  Images:')
    print('    • solar_system_complete.png  - All 8 planets')
    print('    • solar_system_inner.png     - Mercury, Venus, Earth, Mars')
    print('    • solar_system_outer.png     - Jupiter, Saturn, Uranus, Neptune')
    print('    • solar_system_sizes.png     - Relative size comparison')
    print('  Data:')
    print('    • planet_data.csv            - Complete planet statistics')
    print('='*70 + '\n')