import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from textwrap import wrap
from matplotlib.patches import ConnectionPatch, Wedge, Circle, Arc, Polygon
import json

rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False
zones = [
        {"min": 0, "max": 3.5, "color": "#5BE12C"},  # Green
        {"min": 3.5, "max": 5, "color": "#F5CD19"},  # Yellow
        {"min": 5, "max": 10, "color": "#EA4228"}  # Red
    ]

def draw_multiple_gauges(data_str) -> None:
    """
    Draw multiple gauge/odometer visualizations side by side.
    
    Args:
        records: list of dicts with risk data including:
            - "risk_label": risk category name
            - "risk_value": numeric risk value
        zones: list of zone dicts with "min", "max", and "color" keys
    """
    records = data_str

    n = len(records)
    fig, axes = plt.subplots(1, n, figsize=(3 * n, 5.5))
    if n == 1:
        axes = [axes]

    for ax, item in zip(axes, records):
        draw_gauge_on_ax(ax, item['risk_label'], item['risk_value'], zones)

    plt.tight_layout()
    plt.savefig('D:\\SourceCode\\apache-tomcat-11.0.9\\webapps\ROOT\\risk_graph\\odometer.png')

def draw_gauge_on_ax(ax, risk_name: str, risk_value: float, 
                    zones: list, min_val: float = 0.0, max_val: float = 10.0) -> None:
    """
    Draw a single gauge/odometer visualization on a matplotlib axis.
    
    Args:
        ax: matplotlib axis object
        risk_name: Name of the risk to display
        risk_value: Current risk value
        zones: List of zone dicts with "min", "max", and "color" keys
        min_val: Minimum value for the gauge
        max_val: Maximum value for the gauge
    """
    # clamp value and round to nearest hundredths
    v = round(max(min_val, min(max_val, risk_value)), 2)

    # draw outer frame (270 degree arc)
    ax.add_patch(Arc((0, 0), 2.1, 2.1, theta1=225, theta2=-45, 
                 linewidth=3, edgecolor='#cccccc', fill=False))

    def to_angle(x):
        # Convert value to angle (225° to -45°)
        return 225 - (x - min_val) / (max_val - min_val) * 270

    # colored zones
    for zone in zones:
        a0, a1 = to_angle(zone["min"]), to_angle(zone["max"])
        ax.add_patch(Wedge((0, 0), 1.0, a1, a0,
                   width=0.15, facecolor=zone["color"], edgecolor='white'))

    # major ticks and labels
    for x in range(int(min_val), int(max_val) + 1):
        ang = math.radians(to_angle(x))
        x0, y0 = 0.85 * math.cos(ang), 0.85 * math.sin(ang)
        x1, y1 = 0.95 * math.cos(ang), 0.95 * math.sin(ang)
        ax.plot([x0, x1], [y0, y1], lw=2, color='black')
        xt, yt = 1.10 * math.cos(ang), 1.10 * math.sin(ang)
        ax.text(xt, yt, f"{x:.1f}", ha='center', va='center', 
              fontsize=12, color='black')

    # minor ticks
    step = 0.5
    n = int((max_val - min_val) / step) + 1
    for i in range(n):
        x = min_val + i * step
        if abs(x - round(x)) < 1e-6:
            continue
        ang = math.radians(to_angle(x))
        x0, y0 = 0.88 * math.cos(ang), 0.88 * math.sin(ang)
        x1, y1 = 0.95 * math.cos(ang), 0.95 * math.sin(ang)
        ax.plot([x0, x1], [y0, y1], lw=1, color='black')

    # Create pointer with needle at end
    ang = math.radians(to_angle(v))
    pointer_length = 0.85
    
    # Pointer shaft (tapered)
    shaft_width = 0.03
    shaft_end = 0.7
    
    # Calculate shaft points
    x_base1 = shaft_width * math.cos(ang + math.pi/2)
    y_base1 = shaft_width * math.sin(ang + math.pi/2)
    x_base2 = shaft_width * math.cos(ang - math.pi/2)
    y_base2 = shaft_width * math.sin(ang - math.pi/2)
    
    x_end1 = shaft_end * math.cos(ang) + shaft_width/3 * math.cos(ang + math.pi/2)
    y_end1 = shaft_end * math.sin(ang) + shaft_width/3 * math.sin(ang + math.pi/2)
    x_end2 = shaft_end * math.cos(ang) + shaft_width/3 * math.cos(ang - math.pi/2)
    y_end2 = shaft_end * math.sin(ang) + shaft_width/3 * math.sin(ang - math.pi/2)
    
    x_tip = pointer_length * math.cos(ang)
    y_tip = pointer_length * math.sin(ang)
    
    # Draw pointer as polygon
    ax.add_patch(Polygon([[x_base1, y_base1], 
                         [x_base2, y_base2],
                         [x_end2, y_end2],
                         [x_tip, y_tip],
                         [x_end1, y_end1]], 
                        closed=True, color='black'))

    # Center dot
    ax.add_patch(Circle((0, 0), 0.05, color='black'))

    # center text
    ax.text(0, -0.25, f"{v:.2f}", ha='center', va='center',
           fontsize=16, color='black', fontweight='bold')
    ax.text(0, -0.85, risk_name, ha='center', va='center',
           fontsize=14, color='black', fontweight='bold')

    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.1, 1.1)


if __name__ == "__main__":
    data_str = '''[
        {
          "quarter": 1,
          "risk_id": 10,
          "risk_label": "操作风险",
          "risk_value": 6.38,
          "row_id": 1,
          "year": 2024
        },
        {
          "quarter": 1,
          "risk_id": 20,
          "risk_label": "市场风险",
          "risk_value": 6.34,
          "row_id": 2,
          "year": 2024
        }
      ]'''
    draw_multiple_gauges(data_str)
