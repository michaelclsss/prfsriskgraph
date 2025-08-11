import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from textwrap import wrap
from matplotlib.patches import Circle

def plot_risk_assessment(data):
    # Set Chinese font
    rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
    rcParams['axes.unicode_minus'] = False
    print("==========================")
    print(data)
    # Create figure with two columns
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1])  # Equal width columns
    
    # Left axis for bubbles
    ax1 = fig.add_subplot(gs[0])
    
    # Right axis for text
    ax2 = fig.add_subplot(gs[1])
    ax2.axis('off')  # Turn off axis for text block

    # Extract and sort risk data
    combined = sorted(
        [(risk["risk_label"], risk["risk_value"], risk["comments"]) 
         for risk in data],
        key=lambda x: x[1], 
        reverse=True
    )
    risk_names, risk_indices, risk_comments = zip(*combined)

    # Categorize risks
    high_risks = [r for r in combined if r[1] >= 5.0]
    medium_risks = [r for r in combined if 3.5 <= r[1] < 5.0]
    low_risks = [r for r in combined if r[1] < 3.5]

    # Create positions and styles for bubbles
    x_pos = []
    y_pos = []
    colors = []
    sizes = []
    labels = []
    values = []
    
    # High risks (red, left)
    for i, (name, val, comment) in enumerate(high_risks):
        x_pos.append(1)
        y_pos.append(i+1)
        colors.append('#FF6B6B')
        sizes.append(2000)
        labels.append(name)
        values.append(val)
    
    # Medium risks (yellow, middle)
    for i, (name, val, comment) in enumerate(medium_risks):
        x_pos.append(2)
        y_pos.append(i+1 + len(high_risks)*0.2)
        colors.append('#FFD166')
        sizes.append(1500)
        labels.append(name)
        values.append(val)
    
    # Low risks (green, right)
    for i, (name, val, comment) in enumerate(low_risks):
        x_pos.append(3)
        y_pos.append(i+1 + len(high_risks)*0.4)
        colors.append('#06D6A0')
        sizes.append(1000)
        labels.append(name)
        values.append(val)

    # Create scatter plot
    scatter = ax1.scatter(
        x=x_pos,
        y=y_pos,
        s=sizes,
        c=colors,
        edgecolors='black',
        alpha=0.85,
        zorder=3
    )

    # Add labels and values to bubbles
    for x, y, name, val in zip(x_pos, y_pos, labels, values):
        # Risk name
        ax1.text(
            x=x,
            y=y-0.3,
            s=name,
            ha='center',
            va='top',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.7, pad=1,
                     boxstyle='round,pad=0.1', edgecolor='lightgray')
        )
        
        # Value inside bubble if it's high or medium risk
        if val >= 3.5:
            ax1.text(
                x=x,
                y=y,
                s=f"{val:.1f}",
                ha='center',
                va='center',
                fontsize=10,
                color='black',
                weight='bold'
            )

    # Customize bubble chart axes
    ax1.set_yticks([])
    ax1.set_ylim(0, max(y_pos)+1 if y_pos else 4)
    ax1.set_xticks([1, 2, 3], ['高风险', '中风险', '低风险'], fontsize=12)
    ax1.set_xlim(0.5, 3.5)
    
    # Add colored backgrounds
    ax1.axvspan(0.5, 1.5, facecolor='#FF6B6B', alpha=0.2)
    ax1.axvspan(1.5, 2.5, facecolor='#FFD166', alpha=0.2)
    ax1.axvspan(2.5, 3.5, facecolor='#06D6A0', alpha=0.2)

    # Clean up axes
    for spine in ['top', 'right', 'left']:
        ax1.spines[spine].set_visible(False)
    
    # Title
    ax1.set_title('操作风险二级风险评估', fontsize=14, pad=20)

    # Add title for text block
    ax2.text(
        0.02, 1.02,
        "风险详细说明",
        fontsize=12,
        weight='bold',
        ha='left',
        va='bottom'
    )

    # Create formatted text block for comments with colored circles
    y_position = 0.98  # Starting y position for text
    for i, (name, val, comment) in enumerate(combined, 1):
        # Determine color based on risk level
        if val >= 5.0:
            color = '#FF6B6B'  # High risk (red)
        elif val >= 3.5:
            color = '#FFD166'  # Medium risk (yellow)
        else:
            color = '#06D6A0'  # Low risk (green)
        
        # Add colored circle indicator
        circle = Circle((0.015, y_position - 0.015), 0.008, color=color, zorder=3)
        ax2.add_patch(circle)
        
        # Wrap comment text
        wrapped_comment = '\n'.join(wrap(f"{comment}", width=50))
        
        # Add risk name and value
        ax2.text(
            0.03, y_position,
            f"{i}. {name} ({val:.1f}):",
            ha='left',
            va='top',
            fontsize=10,
            weight='bold'
        )
        
        # Add comment text
        ax2.text(
            0.03, y_position - 0.04,
            wrapped_comment,
            ha='left',
            va='top',
            fontsize=9,
            linespacing=1.6
        )
        
        # Adjust y position based on number of lines in comment
        y_position -= 0.04 * (wrapped_comment.count('\n') + 3)

    plt.tight_layout()
    plt.savefig(f"D:\\SourceCode\\apache-tomcat-11.0.9\\webapps\ROOT\\risk_graph\\circles.png", dpi=300, bbox_inches='tight')
    plt.close()

