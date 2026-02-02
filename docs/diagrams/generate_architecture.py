#!/usr/bin/env python3
"""
Architecture Diagram Generator - Improved Readability

Generates a professional architecture diagram for the Deep Research System.
Higher DPI and larger fonts for better readability.

Usage:
    python generate_architecture.py

Output:
    architecture_diagram.png (dark theme)
    architecture_diagram_light.png (light theme)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set up the figure with dark theme - HIGHER DPI for clarity
plt.style.use('dark_background')
fig, ax = plt.subplots(1, 1, figsize=(14, 10), facecolor='#0a0a0f', dpi=150)
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
        linewidth=2.5,
        alpha=0.95
    )
    ax.add_patch(box)
    
    # Title - LARGER FONT
    ax.text(x, y + height/4, title, ha='center', va='center',
            fontsize=13, fontweight='bold', color=text_color)
    
    # Subtitle - LARGER FONT
    if subtitle:
        ax.text(x, y - height/4, subtitle, ha='center', va='center',
                fontsize=10, color='#94a3b8', style='italic')
    
    return box

def draw_arrow(ax, start, end, color="#64748b", style="->", lw=2):
    """Draw an arrow between two points."""
    arrow = FancyArrowPatch(
        start, end,
        arrowstyle=style,
        color=color,
        linewidth=lw,
        mutation_scale=18,
        alpha=0.8
    )
    ax.add_patch(arrow)

def draw_agent_box(ax, x, y, name, description, color):
    """Draw an agent box with icon styling."""
    width, height = 17, 12
    
    # Main box
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02,rounding_size=1",
        facecolor=f'{color}18',  # 18% opacity
        edgecolor=color,
        linewidth=2.5
    )
    ax.add_patch(box)
    
    # Colored left border - THICKER
    left_bar = plt.Rectangle((x - width/2, y - height/2), 2, height,
                              facecolor=color, edgecolor='none', alpha=0.9)
    ax.add_patch(left_bar)
    
    # Name - LARGER FONT
    ax.text(x + 0.8, y + 2, name, ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')
    
    # Description - LARGER FONT
    ax.text(x + 0.8, y - 2.5, description, ha='center', va='center',
            fontsize=9, color='#94a3b8')
    
    return box

# Title - LARGER
ax.text(50, 97, 'Deep Research System', ha='center', va='center',
        fontsize=28, fontweight='bold', color='white')
ax.text(50, 93, 'Multi-Agent Orchestration Architecture', ha='center', va='center',
        fontsize=14, color='#64748b')

# ==================== MISSION CONTROL DASHBOARD ====================
draw_box(ax, 50, 80, 90, 18, "", "", "#3b82f6")
ax.text(50, 86, 'MISSION CONTROL DASHBOARD', ha='center', va='center',
        fontsize=16, fontweight='bold', color='#3b82f6')

# Dashboard components
components = [
    (15, 78, "Research Input", "Query Form", "#3b82f6"),
    (38, 78, "Agent Pipeline", "5 Agents Live", "#10b981"),
    (62, 78, "Event Log", "SSE Stream", "#8b5cf6"),
    (85, 78, "Report Viewer", "Markdown + PDF", "#ec4899"),
]

for x, y, title, subtitle, color in components:
    draw_box(ax, x, y, 17, 8, title, subtitle, color)

# ==================== BACKEND API LAYER ====================
draw_box(ax, 50, 55, 90, 22, "", "", "#10b981")
ax.text(50, 64, 'BACKEND API (FastAPI + LangGraph)', ha='center', va='center',
        fontsize=15, fontweight='bold', color='#10b981')

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

# Arrows between agents - THICKER
for i in range(len(agents) - 1):
    draw_arrow(ax, (agents[i][0] + 8.5, agents[i][1]), (agents[i+1][0] - 8.5, agents[i+1][1]), "#475569", lw=2.5)

# Iteration loop (Reviewer -> Planner)
# Draw curved arrow
from matplotlib.patches import Arc
arc = Arc((42, 42), 52, 22, angle=0, theta1=180, theta2=360,
          color='#8b5cf6', linewidth=2.5, linestyle='--', alpha=0.7)
ax.add_patch(arc)
ax.annotate('', xy=(18, 48), xytext=(18, 43),
            arrowprops=dict(arrowstyle='->', color='#8b5cf6', lw=2.5))
ax.text(42, 37, 'Iteration Loop (if gaps found)', ha='center', va='center',
        fontsize=10, color='#8b5cf6', style='italic')

# ==================== STORAGE LAYER ====================
draw_box(ax, 28, 30, 32, 12, "", "", "#64748b")
ax.text(28, 34, 'SQLite Checkpointer', ha='center', va='center',
        fontsize=13, fontweight='bold', color='white')
ax.text(28, 30, 'Session Persistence', ha='center', va='center',
        fontsize=10, color='#94a3b8')

# ==================== INFERENCE LAYER ====================
draw_box(ax, 72, 30, 32, 12, "", "", "#f59e0b")
ax.text(72, 34, 'Ollama Inference', ha='center', va='center',
        fontsize=13, fontweight='bold', color='white')
ax.text(72, 30, 'gpt-oss:20b + ROCm', ha='center', va='center',
        fontsize=10, color='#94a3b8')

# Arrows from backend to storage/inference
ax.annotate('', xy=(28, 36), xytext=(35, 48),
            arrowprops=dict(arrowstyle='->', color='#64748b', lw=2, alpha=0.6))
ax.annotate('', xy=(72, 36), xytext=(65, 48),
            arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=2, alpha=0.6))

# ==================== PROTOCOLS ====================
ax.text(50, 20, 'Protocols: HTTP / REST / SSE / JSON', ha='center', va='center',
        fontsize=11, color='#64748b', style='italic')

# ==================== LEGEND ====================
legend_y = 12
ax.text(8, legend_y + 4, 'Agents:', ha='left', va='center',
        fontsize=11, fontweight='bold', color='white')

legend_items = [
    ("Planner", "#3b82f6"),
    ("Finder", "#10b981"),
    ("Summarizer", "#f59e0b"),
    ("Reviewer", "#8b5cf6"),
    ("Writer", "#ec4899"),
]

for i, (name, color) in enumerate(legend_items):
    x_pos = 8 + i * 19
    circle = plt.Circle((x_pos, legend_y), 1.8, color=color)
    ax.add_patch(circle)
    ax.text(x_pos + 4, legend_y, name, ha='left', va='center',
            fontsize=10, color='#94a3b8')

# Save the diagram - HIGHER DPI
plt.tight_layout()
plt.savefig('architecture_diagram.png', dpi=200, bbox_inches='tight',
            facecolor='#0a0a0f', edgecolor='none', pad_inches=0.3)
print("✓ Architecture diagram saved to: architecture_diagram.png")

# Also save a light version for documentation
fig_light, ax_light = plt.subplots(1, 1, figsize=(14, 10), facecolor='white', dpi=150)
ax_light.set_xlim(0, 100)
ax_light.set_ylim(0, 100)
ax_light.axis('off')
ax_light.set_facecolor('white')

# Light version functions
def draw_box_light(ax, x, y, width, height, title, subtitle="", color="#3b82f6"):
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02,rounding_size=1.5",
        facecolor='#f8fafc',
        edgecolor=color,
        linewidth=2.5
    )
    ax.add_patch(box)
    ax.text(x, y + height/4, title, ha='center', va='center',
            fontsize=13, fontweight='bold', color='#1e293b')
    if subtitle:
        ax.text(x, y - height/4, subtitle, ha='center', va='center',
                fontsize=10, color='#64748b', style='italic')

def draw_agent_box_light(ax, x, y, name, description, color):
    width, height = 17, 12
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02,rounding_size=1",
        facecolor='white',
        edgecolor=color,
        linewidth=2.5
    )
    ax.add_patch(box)
    left_bar = plt.Rectangle((x - width/2, y - height/2), 2, height,
                              facecolor=color, edgecolor='none', alpha=0.9)
    ax.add_patch(left_bar)
    ax.text(x + 0.8, y + 2, name, ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1e293b')
    ax.text(x + 0.8, y - 2.5, description, ha='center', va='center',
            fontsize=9, color='#64748b')

# Light version title
ax_light.text(50, 97, 'Deep Research System', ha='center', va='center',
        fontsize=28, fontweight='bold', color='#1e293b')
ax_light.text(50, 93, 'Multi-Agent Orchestration Architecture', ha='center', va='center',
        fontsize=14, color='#64748b')

# Dashboard layer
draw_box_light(ax_light, 50, 80, 90, 18, "", "", "#3b82f6")
ax_light.text(50, 86, 'MISSION CONTROL DASHBOARD', ha='center', va='center',
        fontsize=16, fontweight='bold', color='#3b82f6')

components = [
    (15, 78, "Research Input", "Query Form", "#3b82f6"),
    (38, 78, "Agent Pipeline", "5 Agents Live", "#10b981"),
    (62, 78, "Event Log", "SSE Stream", "#8b5cf6"),
    (85, 78, "Report Viewer", "Markdown + PDF", "#ec4899"),
]
for x, y, title, subtitle, color in components:
    draw_box_light(ax_light, x, y, 17, 8, title, subtitle, color)

# Backend layer
draw_box_light(ax_light, 50, 55, 90, 22, "", "", "#10b981")
ax_light.text(50, 64, 'BACKEND API (FastAPI + LangGraph)', ha='center', va='center',
        fontsize=15, fontweight='bold', color='#10b981')

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
    ax_light.annotate('', xy=(agents[i+1][0] - 8.5, agents[i+1][1]), xytext=(agents[i][0] + 8.5, agents[i][1]),
                arrowprops=dict(arrowstyle='->', color='#94a3b8', lw=2.5))

# Iteration arc
arc_light = Arc((42, 42), 52, 22, angle=0, theta1=180, theta2=360,
          color='#8b5cf6', linewidth=2.5, linestyle='--', alpha=0.7)
ax_light.add_patch(arc_light)
ax_light.annotate('', xy=(18, 48), xytext=(18, 43),
            arrowprops=dict(arrowstyle='->', color='#8b5cf6', lw=2.5))
ax_light.text(42, 37, 'Iteration Loop (if gaps found)', ha='center', va='center',
        fontsize=10, color='#8b5cf6', style='italic')

# Storage and inference
draw_box_light(ax_light, 28, 30, 32, 12, "", "", "#64748b")
ax_light.text(28, 34, 'SQLite Checkpointer', ha='center', va='center',
        fontsize=13, fontweight='bold', color='#1e293b')
ax_light.text(28, 30, 'Session Persistence', ha='center', va='center',
        fontsize=10, color='#64748b')

draw_box_light(ax_light, 72, 30, 32, 12, "", "", "#f59e0b")
ax_light.text(72, 34, 'Ollama Inference', ha='center', va='center',
        fontsize=13, fontweight='bold', color='#1e293b')
ax_light.text(72, 30, 'gpt-oss:20b + ROCm', ha='center', va='center',
        fontsize=10, color='#64748b')

ax_light.annotate('', xy=(28, 36), xytext=(35, 48),
            arrowprops=dict(arrowstyle='->', color='#64748b', lw=2, alpha=0.6))
ax_light.annotate('', xy=(72, 36), xytext=(65, 48),
            arrowprops=dict(arrowstyle='->', color='#f59e0b', lw=2, alpha=0.6))

ax_light.text(50, 20, 'Protocols: HTTP / REST / SSE / JSON', ha='center', va='center',
        fontsize=11, color='#64748b', style='italic')

# Legend
legend_y = 12
ax_light.text(8, legend_y + 4, 'Agents:', ha='left', va='center',
        fontsize=11, fontweight='bold', color='#1e293b')
for i, (name, color) in enumerate(legend_items):
    x_pos = 8 + i * 19
    circle = plt.Circle((x_pos, legend_y), 1.8, color=color)
    ax_light.add_patch(circle)
    ax_light.text(x_pos + 4, legend_y, name, ha='left', va='center',
            fontsize=10, color='#475569')

plt.tight_layout()
plt.savefig('architecture_diagram_light.png', dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none', pad_inches=0.3)
print("✓ Light theme diagram saved to: architecture_diagram_light.png")

plt.close('all')
print("\n✅ Done! Generated both dark and light theme diagrams at 200 DPI.")
