#!/usr/bin/env python3
"""
Create simple custom charts with specified color gradient
"""

import plotly.graph_objects as go
import plotly.express as px

# Color gradient from #84a9ff to #f5f8ff
def create_gradient_colors(n_colors):
    """Create gradient colors from #84a9ff to #f5f8ff"""
    start_color = [132, 169, 255]  # #84a9ff
    end_color = [245, 248, 255]    # #f5f8ff
    
    colors = []
    for i in range(n_colors):
        ratio = i / (n_colors - 1) if n_colors > 1 else 0
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        colors.append(f'rgb({r},{g},{b})')
    
    return colors

def create_fan_engagement_chart():
    """Create fan engagement chart with custom styling"""
    
    # Data
    age_groups = ['18-25', '26-40', '41-60', '60+', '<18']
    total_games = [178073, 101472, 60499, 19638, 40117]
    
    # Create gradient colors
    colors = create_gradient_colors(len(age_groups))
    
    fig = go.Figure(data=[
        go.Bar(
            x=age_groups,
            y=total_games,
            marker_color=colors,
            text=[f'{x:,}' for x in total_games],
            textposition='auto',
            textfont=dict(size=16, color='#2c3e50')
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Total Games Attended by Age Group',
            font=dict(size=24, color='#2c3e50'),
            x=0.5
        ),
        xaxis=dict(
            title=dict(text='Age Group', font=dict(size=18, color='#2c3e50')),
            tickfont=dict(size=14, color='#2c3e50')
        ),
        yaxis=dict(
            title=dict(text='Total Games Attended', font=dict(size=18, color='#2c3e50')),
            tickfont=dict(size=14, color='#2c3e50')
        ),
        plot_bgcolor='#f5f8ff',
        paper_bgcolor='#f5f8ff',
        font=dict(size=14, color='#2c3e50'),
        margin=dict(t=80, b=80, l=80, r=80),
        height=500,
        width=800
    )
    
    fig.write_image('fan_engagement_custom.png', scale=2)
    print("Created fan_engagement_custom.png")

def create_revenue_composition_chart():
    """Create revenue composition chart with custom styling"""
    
    # Data
    labels = ['Stadium Operations', 'Merchandise Sales']
    values = [13233516, 6457131]
    colors = ['#84a9ff', '#b8c9ff']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            marker_colors=colors,
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}',
            textfont=dict(size=16, color='#2c3e50')
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Revenue Composition Analysis',
            font=dict(size=24, color='#2c3e50'),
            x=0.5
        ),
        plot_bgcolor='#f5f8ff',
        paper_bgcolor='#f5f8ff',
        font=dict(size=14, color='#2c3e50'),
        margin=dict(t=80, b=80, l=80, r=80),
        height=500,
        width=800,
        showlegend=True,
        legend=dict(
            font=dict(size=16, color='#2c3e50'),
            x=0.5,
            y=-0.1,
            orientation='h'
        )
    )
    
    fig.write_image('revenue_composition_custom.png', scale=2)
    print("Created revenue_composition_custom.png")

def create_stadium_sources_chart():
    """Create stadium sources chart with custom styling"""
    
    # Data
    sources = ['Lower Bowl', 'Food', 'Advertising', 'Concert', 'Upper Bowl', 'Season', 'Premium', 'Conference']
    revenues = [24669304, 19948319, 5098950, 4875000, 3855705, 3807502, 2322177, 1562500]
    
    # Create gradient colors
    colors = create_gradient_colors(len(sources))
    
    fig = go.Figure(data=[
        go.Bar(
            x=sources,
            y=revenues,
            marker_color=colors,
            text=[f'${x:,.0f}' for x in revenues],
            textposition='auto',
            textfont=dict(size=14, color='#2c3e50')
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Stadium Revenue by Source Analysis',
            font=dict(size=24, color='#2c3e50'),
            x=0.5
        ),
        xaxis=dict(
            title='Stadium Source',
            title=dict(text='', font=dict(size=18, color='#2c3e50')),
            tickfont=dict(size=12, color='#2c3e50')
        ),
        yaxis=dict(
            title='Revenue ($)',
            title=dict(text='', font=dict(size=18, color='#2c3e50')),
            tickfont=dict(size=14, color='#2c3e50')
        ),
        plot_bgcolor='#f5f8ff',
        paper_bgcolor='#f5f8ff',
        font=dict(size=14, color='#2c3e50'),
        margin=dict(t=80, b=80, l=80, r=80),
        height=500,
        width=800
    )
    
    fig.write_image('stadium_sources_custom.png', scale=2)
    print("Created stadium_sources_custom.png")

def create_merchandise_categories_chart():
    """Create merchandise categories chart with custom styling"""
    
    # Data
    categories = ['Jersey', 'Hoodie', 'Youth Jersey', 'Youth Hoodie', 'Cap', 'Scarf', 'Mug', 'Poster']
    revenues = [4105976, 1044825, 597960, 222650, 173810, 150800, 95550, 65560]
    
    # Create gradient colors
    colors = create_gradient_colors(len(categories))
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=revenues,
            marker_color=colors,
            text=[f'${x:,.0f}' for x in revenues],
            textposition='auto',
            textfont=dict(size=12, color='#2c3e50')
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Merchandise Revenue by Category',
            font=dict(size=24, color='#2c3e50'),
            x=0.5
        ),
        xaxis=dict(
            title='Product Category',
            title=dict(text='', font=dict(size=18, color='#2c3e50')),
            tickfont=dict(size=12, color='#2c3e50')
        ),
        yaxis=dict(
            title='Revenue ($)',
            title=dict(text='', font=dict(size=18, color='#2c3e50')),
            tickfont=dict(size=14, color='#2c3e50')
        ),
        plot_bgcolor='#f5f8ff',
        paper_bgcolor='#f5f8ff',
        font=dict(size=14, color='#2c3e50'),
        margin=dict(t=80, b=80, l=80, r=80),
        height=500,
        width=800
    )
    
    fig.write_image('merchandise_categories_custom.png', scale=2)
    print("Created merchandise_categories_custom.png")

def create_seasonal_pass_chart():
    """Create seasonal pass chart with custom styling"""
    
    # Data
    pass_types = ['No Pass', 'Seasonal Pass']
    games = [4.5, 22.4]
    colors = ['#84a9ff', '#f5f8ff']
    
    fig = go.Figure(data=[
        go.Bar(
            x=pass_types,
            y=games,
            marker_color=colors,
            text=[f'{x:.1f}' for x in games],
            textposition='auto',
            textfont=dict(size=16, color='#2c3e50')
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Seasonal Pass Impact Analysis',
            font=dict(size=24, color='#2c3e50'),
            x=0.5
        ),
        xaxis=dict(
            title='Pass Type',
            title=dict(text='', font=dict(size=18, color='#2c3e50')),
            tickfont=dict(size=14, color='#2c3e50')
        ),
        yaxis=dict(
            title='Average Games Attended',
            title=dict(text='', font=dict(size=18, color='#2c3e50')),
            tickfont=dict(size=14, color='#2c3e50')
        ),
        plot_bgcolor='#f5f8ff',
        paper_bgcolor='#f5f8ff',
        font=dict(size=14, color='#2c3e50'),
        margin=dict(t=80, b=80, l=80, r=80),
        height=500,
        width=800
    )
    
    fig.write_image('seasonal_pass_custom.png', scale=2)
    print("Created seasonal_pass_custom.png")

def create_channel_performance_chart():
    """Create channel performance chart with custom styling"""
    
    # Data
    labels = ['Online', 'Team Store']
    values = [5172119, 1285012]
    colors = ['#84a9ff', '#b8c9ff']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            marker_colors=colors,
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}',
            textfont=dict(size=16, color='#2c3e50')
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Sales Channel Performance Analysis',
            font=dict(size=24, color='#2c3e50'),
            x=0.5
        ),
        plot_bgcolor='#f5f8ff',
        paper_bgcolor='#f5f8ff',
        font=dict(size=14, color='#2c3e50'),
        margin=dict(t=80, b=80, l=80, r=80),
        height=500,
        width=800,
        showlegend=True,
        legend=dict(
            font=dict(size=16, color='#2c3e50'),
            x=0.5,
            y=-0.1,
            orientation='h'
        )
    )
    
    fig.write_image('channel_performance_custom.png', scale=2)
    print("Created channel_performance_custom.png")

def create_promotion_impact_chart():
    """Create promotion impact chart with custom styling"""
    
    # Data
    promotion_types = ['No Promotion', 'With Promotion']
    revenues = [4130819, 2326312]
    colors = ['#84a9ff', '#b8c9ff']
    
    fig = go.Figure(data=[
        go.Bar(
            x=promotion_types,
            y=revenues,
            marker_color=colors,
            text=[f'${x:,.0f}' for x in revenues],
            textposition='auto',
            textfont=dict(size=16, color='#2c3e50')
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Promotion Impact Analysis',
            font=dict(size=24, color='#2c3e50'),
            x=0.5
        ),
        xaxis=dict(
            title='Promotion Type',
            title=dict(text='', font=dict(size=18, color='#2c3e50')),
            tickfont=dict(size=14, color='#2c3e50')
        ),
        yaxis=dict(
            title='Revenue ($)',
            title=dict(text='', font=dict(size=18, color='#2c3e50')),
            tickfont=dict(size=14, color='#2c3e50')
        ),
        plot_bgcolor='#f5f8ff',
        paper_bgcolor='#f5f8ff',
        font=dict(size=14, color='#2c3e50'),
        margin=dict(t=80, b=80, l=80, r=80),
        height=500,
        width=800
    )
    
    fig.write_image('promotion_impact_custom.png', scale=2)
    print("Created promotion_impact_custom.png")

if __name__ == "__main__":
    print("Creating custom charts with #84a9ff to #f5f8ff gradient...")
    
    try:
        create_fan_engagement_chart()
        create_revenue_composition_chart()
        create_stadium_sources_chart()
        create_merchandise_categories_chart()
        create_seasonal_pass_chart()
        create_channel_performance_chart()
        create_promotion_impact_chart()
        
        print("\nAll custom charts created successfully!")
        print("Files created:")
        print("- fan_engagement_custom.png")
        print("- revenue_composition_custom.png")
        print("- stadium_sources_custom.png")
        print("- merchandise_categories_custom.png")
        print("- seasonal_pass_custom.png")
        print("- channel_performance_custom.png")
        print("- promotion_impact_custom.png")
        
    except Exception as e:
        print(f"Error creating charts: {e}")
