import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

# Create overlapping phases data (showing dependencies)
phases_data = {
    "Phase": ["Foundation", "AI Pipeline", "Core Feats", "Advanced", "Test & Deploy"],
    "Start_Week": [1, 2.5, 5.5, 8.5, 11.5],  # Overlapping starts
    "End_Week": [4, 6.5, 9.5, 12.5, 14],
    "Duration": [3, 4, 4, 4, 2.5]
}

# Create figure
fig = go.Figure()

# Colors for phases
colors = ["#1FB8CD", "#DB4545", "#2E8B57", "#5D878F", "#D2BA4C"]

# Add overlapping phase bars with transparency
for i, (phase, start, end, duration) in enumerate(zip(
    phases_data["Phase"], 
    phases_data["Start_Week"], 
    phases_data["End_Week"], 
    phases_data["Duration"]
)):
    fig.add_trace(go.Bar(
        x=[duration],
        y=[phase],
        base=[start-1],
        orientation='h',
        name=phase,
        marker_color=colors[i],
        opacity=0.8,
        showlegend=True
    ))

# Add milestone markers with better positioning
milestones = ["Infra Ready", "AI Operational", "Core Complete", "Prod Ready", "Launch Ready"]
milestone_weeks = [3.5, 6, 9, 12, 14]
milestone_phases = ["Foundation", "AI Pipeline", "Core Feats", "Advanced", "Test & Deploy"]

for i, (milestone, week, phase) in enumerate(zip(milestones, milestone_weeks, milestone_phases)):
    fig.add_trace(go.Scatter(
        x=[week],
        y=[phase],
        mode='markers+text',
        marker=dict(symbol='diamond', size=15, color='black', line=dict(width=2, color='white')),
        text=milestone,
        textposition='top center',
        textfont=dict(size=10, color='black'),
        showlegend=False,
        name=f"Milestone: {milestone}"
    ))

# Add dependency arrows between phases
arrow_positions = [
    (3.5, "Foundation", 2.5, "AI Pipeline"),
    (6, "AI Pipeline", 5.5, "Core Feats"),  
    (9, "Core Feats", 8.5, "Advanced"),
    (12, "Advanced", 11.5, "Test & Deploy")
]

for start_week, start_phase, end_week, end_phase in arrow_positions:
    fig.add_annotation(
        x=end_week, y=end_phase,
        ax=start_week, ay=start_phase,
        xref='x', yref='y',
        axref='x', ayref='y',
        arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='gray',
        showarrow=True
    )

# Update layout with better spacing
fig.update_layout(
    title="JourneyLens Dev Timeline",
    xaxis_title="Week", 
    yaxis_title="Phase",
    barmode='overlay',
    legend=dict(
        orientation='h', 
        yanchor='bottom', 
        y=1.02, 
        xanchor='center', 
        x=0.5
    ),
    height=500
)

fig.update_xaxes(range=[0, 15], dtick=2, showgrid=True)
fig.update_yaxes(
    categoryorder="array", 
    categoryarray=["Test & Deploy", "Advanced", "Core Feats", "AI Pipeline", "Foundation"]
)

# Add vertical lines for key milestones
for week in milestone_weeks:
    fig.add_vline(x=week, line_dash="dash", line_color="gray", opacity=0.5)

fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image("gantt_chart.png")
fig.write_image("gantt_chart.svg", format="svg")