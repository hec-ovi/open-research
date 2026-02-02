#!/usr/bin/env python3
"""
Architecture Diagram Generator

Generates a professional architecture diagram for the Deep Research System.

Usage:
    python generate_architecture.py

Output:
    architecture_diagram.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set up the figure with dark theme
plt.style.use('dark_background')
fig, ax = plt.subplots(1, 1, figsize=(16, 12), facecolor='#0a0a0f')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')
ax.set_facecolor('#0a0a0f')

def draw_box(ax, x, y, width, height, title, subtitle="", color="#3b82f6", text_color="white"):
    """Draw a rounded box with title and subtitle."""
    # Main box
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02,rounding_size=1.5",
        facecolor='#13131f',
        edgecolor=color,
        linewidth=2,
        alpha=0.95
    )
    ax.add_patch(box)
    
    # Title
    ax.text(x, y + height/4, title, ha='center', va='center',
            fontsize=11, fontweight='bold', color=text_color)
    
    # Subtitle
    if subtitle:
        ax.text(x, y - height/4, subtitle, ha='center', va='center',
                fontsize=8, color='#94a3b8', style='italic')
    
    return box

def draw_arrow(ax, start, end, color="#64748b", style="->"):
    """Draw an arrow between two points."""
    arrow = FancyArrowPatch(
        start, end,
        arrowstyle=style,
        color=color,
        linewidth=2,
        mutation_scale=15,
        alpha=0.8
    )
    ax.add_patch(arrow)

def draw_agent_box(ax, x, y, name, description, color):
    """Draw an agent box with icon styling."""
    width, height = 16, 10
    
    # Main box
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02,rounding_size=1",
        facecolor=f'{color}20',  # 20% opacity
        edgecolor=color,
        linewidth=2
    )
    ax.add_patch(box)
    
    # Colored left border
    left_bar = plt.Rectangle((x - width/2, y - height/2), 1.5, height,
                              facecolor=color, edgecolor='none')
    ax.add_patch(left_bar)
    
    # Name
    ax.text(x + 0.75, y + 1.5, name, ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')
    
    # Description
    ax.text(x + 0.75, y - 2, description, ha='center', va='center',
            fontsize=7, color='#94a3b8')
    
    return box

# Title
ax.text(50, 97, 'Deep Research System', ha='center', va='center',
        fontsize=24, fontweight='bold', color='white')
ax.text(50, 93, 'Multi-Agent Orchestration Architecture', ha='center', va='center',
        fontsize=12, color='#64748b')

# ==================== MISSION CONTROL DASHBOARD ====================
draw_box(ax, 50, 80, 90, 18, "", "", "#3b82f6")
ax.text(50, 86, 'MISSION CONTROL DASHBOARD', ha='center', va='center',
        fontsize=14, fontweight='bold', color='#3b82f6')

# Dashboard components
components = [
    (15, 78, "Research Input", "Query Form", "#3b82f6"),
    (38, 78, "Agent Pipeline", "5 Agents Live", "#10b981"),
    (62, 78, "Event Log", "SSE Stream", "#8b5cf6"),
    (85, 78, "Report Viewer", "Markdown + DL", "#ec4899"),
]

for x, y, title, subtitle, color in components:
    draw_box(ax, x, y, 16, 8, title, subtitle, color)

# ==================== BACKEND API LAYER ====================
draw_box(ax, 50, 55, 90, 22, "", "", "#10b981")
ax.text(50, 64, 'BACKEND API (FastAPI + LangGraph)', ha='center', va='center',
        fontsize=13, fontweight='bold', color='#10b981')

# Agent pipeline - horizontal layout
agents = [
    (18, 54, "Planner", "Decompose", "#3b82f6"),
    (34, 54, "Finder", "Search", "#10b981"),
    (50, 54, "Summarizer", "Compress", "#f59e0b"),
    (66, 54, "Reviewer", "Check", "#8b5cf6"),
    (82, 54, "Writer", "Synthesize", "#ec4899"),
]

for x, y, name, desc, color in agents:
    draw_agent_box(ax, x, y, name, desc, color)

# Arrows between agents
for i in range(len(agents) - 1):
    draw_arrow(ax, (agents[i][0] + 8, agents[i][1]), (agents[i+1][0] - 8, agents[i+1][1]), "#475569")

# Iteration loop (Reviewer -> Planner)
# Draw curved arrow
from matplotlib.patches import Arc
arc = Arc((42, 42), 50, 20, angle=0, theta1=180, theta2=360,
          color='#8b5cf6', linewidth=2, linestyle='--', alpha=0.6)
ax.add_patch(arc)
ax.annotate('', xy=(18, 48), xytext=(18, 44),
            arrowprops=dict(arrowstyle='->', color='#8b5cf6', lw=2))
ax.text(42, 38, 'Iteration Loop (if gaps found)', ha='center', va='center',
        fontsize=8, color='#8b5cf6', style='italic')

# ==================== STORAGE LAYER ====================
draw_box(ax, 30, 30, 35, 12, "", "", "#64748b")
ax.text(30, 34, 'SQLite Checkpointer', ha='center', va='center',
        fontsize=11, fontweight='bold', color='white')
ax.text(30, 30, 'Session Persistence & Recovery', ha='center', va='center',
        fontsize=8, color='#94a3b8')

# ==================== INFERENCE LAYER ====================
draw_box(ax, 70, 30, 35, 12, "", "", "#f59e0b")
ax.text(70, 34, 'Ollama Inference', ha='center', va='center',
        fontsize=11, fontweight='bold', color='white')
ax.text(70, 30, 'gpt-oss:20b with ROCm', ha='center', va='center',
        fontsize=8, color='#94a3b8')

# Arrows from backend to storage/inference
draw_arrow(ax, (35, 48), (30, 36), "#64748b")
draw_arrow(ax, (65, 48), (70, 36), "#f59e0b")

# ==================== PROTOCOLS ====================
ax.text(50, 20, 'Protocols: HTTP / REST / SSE / JSON', ha='center', va='center',
        fontsize=9, color='#64748b', style='italic')

# ==================== LEGEND ====================
legend_y = 12
ax.text(10, legend_y + 4, 'Agent Colors:', ha='left', va='center',
        fontsize=9, fontweight='bold', color='white')

legend_items = [
    ("Planner", "#3b82f6"),
    ("Finder", "#10b981"),
    ("Summarizer", "#f59e0b"),
    ("Reviewer", "#8b5cf6"),
    ("Writer", "#ec4899"),
]

for i, (name, color) in enumerate(legend_items):
    x_pos = 10 + i * 18
    circle = plt.Circle((x_pos, legend_y), 1.5, color=color)
    ax.add_patch(circle)
    ax.text(x_pos + 4, legend_y, name, ha='left', va='center',
            fontsize=8, color='#94a3b8')

# Save the diagram
plt.tight_layout()
plt.savefig('architecture_diagram.png', dpi=150, bbox_inches='tight',
            facecolor='#0a0a0f', edgecolor='none', pad_inches=0.5)
print("✓ Architecture diagram saved to: architecture_diagram.png")

# Also save a light version for documentation
fig_light, ax_light = plt.subplots(1, 1, figsize=(16, 12), facecolor='white')
ax_light.set_xlim(0, 100)
ax_light.set_ylim(0, 100)
ax_light.axis('off')
ax_light.set_facecolor('white')

# Redraw with light theme
def draw_box_light(ax, x, y, width, height, title, subtitle="", color="#3b82f6"):
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02,rounding_size=1.5",
        facecolor='#f8fafc',
        edgecolor=color,
        linewidth=2
    )
    ax.add_patch(box)
    ax.text(x, y + height/4, title, ha='center', va='center',
            fontsize=11, fontweight='bold', color='#1e293b')
    if subtitle:
        ax.text(x, y - height/4, subtitle, ha='center', va='center',
                fontsize=8, color='#64748b', style='italic')

def draw_agent_box_light(ax, x, y, name, description, color):
    width, height = 16, 10
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02,rounding_size=1",
        facecolor='white',
        edgecolor=color,
        linewidth=2
    )
    ax.add_patch(box)
    left_bar = plt.Rectangle((x - width/2, y - height/2), 1.5, height,
                              facecolor=color, edgecolor='none')
    ax.add_patch(left_bar)
    ax.text(x + 0.75, y + 1.5, name, ha='center', va='center',
            fontsize=10, fontweight='bold', color='#1e293b')
    ax.text(x + 0.75, y - 2, description, ha='center', va='center',
            fontsize=7, color='#64748b')

# Light version title
ax_light.text(50, 97, 'Deep Research System', ha='center', va='center',
        fontsize=24, fontweight='bold', color='#1e293b')
ax_light.text(50, 93, 'Multi-Agent Orchestration Architecture', ha='center', va='center',
        fontsize=12, color='#64748b')

# Dashboard layer
draw_box_light(ax_light, 50, 80, 90, 18, "", "", "#3b82f6")
ax_light.text(50, 86, 'MISSION CONTROL DASHBOARD', ha='center', va='center',
        fontsize=14, fontweight='bold', color='#3b82f6')

components = [
    (15, 78, "Research Input", "Query Form", "#3b82f6"),
    (38, 78, "Agent Pipeline", "5 Agents Live", "#10b981"),
    (62, 78, "Event Log", "SSE Stream", "#8b5cf6"),
    (85, 78, "Report Viewer", "Markdown + DL", "#ec4899"),
]
for x, y, title, subtitle, color in components:
    draw_box_light(ax_light, x, y, 16, 8, title, subtitle, color)

# Backend layer
draw_box_light(ax_light, 50, 55, 90, 22, "", "", "#10b981")
ax_light.text(50, 64, 'BACKEND API (FastAPI + LangGraph)', ha='center', va='center',
        fontsize=13, fontweight='bold', color='#10b981')

agents = [
    (18, 54, "Planner", "Decompose", "#3b82f6"),
    (34, 54, "Finder", "Search", "#10b981"),
    (50, 54, "Summarizer", "Compress", "#f59e0b"),
    (66, 54, "Reviewer", "Check", "#8b5cf6"),
    (82, 54, "Writer", "Synthesize", "#ec4899"),
]
for x, y, name, desc, color in agents:
    draw_agent_box_light(ax_light, x, y, name, desc, color)

# Arrows
for i in range(len(agents) - 1):
    draw_arrow(ax_light, (agents[i][0] + 8, agents[i][1]), (agents[i+1][0] - 8, agents[i+1][1]), "#94a3b8")

# Storage and inference
draw_box_light(ax_light, 30, 30, 35, 12, "", "", "#64748b")
ax_light.text(30, 34, 'SQLite Checkpointer', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#1e293b')
ax_light.text(30, 30, 'Session Persistence & Recovery', ha='center', va='center',
        fontsize=8, color='#64748b')

draw_box_light(ax_light, 70, 30, 35, 12, "", "", "#f59e0b")
ax_light.text(70, 34, 'Ollama Inference', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#1e293b')
ax_light.text(70, 30, 'gpt-oss:20b with ROCm', ha='center', va='center',
        fontsize=8, color='#64748b')

draw_arrow(ax_light, (35, 48), (30, 36), "#64748b")
draw_arrow(ax_light, (65, 48), (70, 36), "#f59e0b")

ax_light.text(50, 20, 'Protocols: HTTP / REST / SSE / JSON', ha='center', va='center',
        fontsize=9, color='#64748b', style='italic')

# Legend
legend_y = 12
ax_light.text(10, legend_y + 4, 'Agent Colors:', ha='left', va='center',
        fontsize=9, fontweight='bold', color='#1e293b')
for i, (name, color) in enumerate(legend_items):
    x_pos = 10 + i * 18
    circle = plt.Circle((x_pos, legend_y), 1.5, color=color)
    ax_light.add_patch(circle)
    ax_light.text(x_pos + 4, legend_y, name, ha='left', va='center',
            fontsize=8, color='#475569')

plt.tight_layout()
plt.savefig('architecture_diagram_light.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none', pad_inches=0.5)
print("✓ Light theme diagram saved to: architecture_diagram_light.png")

plt.close('all')
print("\nDone! Generated both dark and light theme diagrams.")
