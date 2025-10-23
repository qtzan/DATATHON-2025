#!/usr/bin/env python3
"""
Operational Efficiency and Pricing Analysis for Vancouver City FC
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def analyze_operational_efficiency():
    """Analyze operational efficiency and cost-revenue relationships"""
    print("\n" + "="*80)
    print("SECTION 3E: OPERATIONAL EFFICIENCY ANALYSIS")
    print("="*80)
    
    # Load data
    stadium_ops = pd.read_excel('BOLT UBC First Byte - Stadium Operations.xlsx')
    merchandise = pd.read_excel('BOLT UBC First Byte - Merchandise Sales.xlsx')
    
    # Revenue efficiency by source
    source_efficiency = stadium_ops.groupby('Source')['Revenue'].agg(['sum', 'mean', 'count']).round(2)
    source_efficiency['Revenue_per_Event'] = source_efficiency['sum'] / source_efficiency['count']
    
    # Monthly efficiency trends
    monthly_efficiency = stadium_ops.groupby('Month')['Revenue'].sum().reset_index()
    monthly_efficiency['Cumulative_Revenue'] = monthly_efficiency['Revenue'].cumsum()
    monthly_efficiency['Monthly_Growth'] = monthly_efficiency['Revenue'].pct_change() * 100
    
    # Create visualizations
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue by Source', 'Monthly Revenue Growth',
                       'Revenue Efficiency by Source', 'Cumulative Revenue Trend'),
        specs=[[{"type": "bar"}, {"type": "scatter"}],
                 [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Revenue by source
    fig.add_trace(
        go.Bar(x=source_efficiency.index, y=source_efficiency['sum'],
               name='Total Revenue by Source', marker_color='lightblue'),
        row=1, col=1
    )
    
    # Monthly growth
    fig.add_trace(
        go.Scatter(x=monthly_efficiency['Month'], y=monthly_efficiency['Monthly_Growth'],
                  mode='lines+markers', name='Monthly Growth %', line=dict(color='green')),
        row=1, col=2
    )
    
    # Revenue efficiency
    fig.add_trace(
        go.Bar(x=source_efficiency.index, y=source_efficiency['Revenue_per_Event'],
               name='Revenue per Event', marker_color='orange'),
        row=2, col=1
    )
    
    # Cumulative revenue
    fig.add_trace(
        go.Scatter(x=monthly_efficiency['Month'], y=monthly_efficiency['Cumulative_Revenue'],
                  mode='lines+markers', name='Cumulative Revenue', line=dict(color='purple')),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Operational Efficiency Analysis",
        height=800,
        showlegend=True
    )
    
    fig.show()
    
    print("\nOPERATIONAL EFFICIENCY INSIGHTS:")
    print(f"Most efficient revenue source: {source_efficiency['Revenue_per_Event'].idxmax()}")
    print(f"Average revenue per event: ${source_efficiency['Revenue_per_Event'].mean():,.2f}")
    print(f"Total stadium revenue: ${source_efficiency['sum'].sum():,.2f}")
    
    return source_efficiency, monthly_efficiency

def analyze_pricing_promotions():
    """Analyze pricing, promotions, and partnerships impact"""
    print("\n" + "="*80)
    print("SECTION 3F: PRICING, PROMOTIONS, AND PARTNERSHIPS")
    print("="*80)
    
    # Load merchandise data
    merchandise = pd.read_excel('BOLT UBC First Byte - Merchandise Sales.xlsx')
    
    # Pricing analysis by category
    pricing_analysis = merchandise.groupby('Item_Category')['Unit_Price'].agg(['mean', 'min', 'max', 'std']).round(2)
    
    # Promotion impact analysis
    promotion_impact = merchandise.groupby(['Item_Category', 'Promotion'])['Unit_Price'].agg(['sum', 'count', 'mean']).round(2)
    
    # Channel performance
    channel_performance = merchandise.groupby('Channel')['Unit_Price'].agg(['sum', 'count', 'mean']).round(2)
    
    # Regional pricing analysis
    regional_pricing = merchandise.groupby('Customer_Region')['Unit_Price'].agg(['sum', 'count', 'mean']).round(2)
    
    # Create visualizations
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Average Price by Category', 'Promotion Impact by Category',
                       'Channel Performance', 'Regional Sales Analysis'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
                 [{"type": "bar"}, {"type": "pie"}]]
    )
    
    # Average price by category
    fig.add_trace(
        go.Bar(x=pricing_analysis.index, y=pricing_analysis['mean'],
               name='Avg Price by Category', marker_color='lightgreen'),
        row=1, col=1
    )
    
    # Promotion impact
    promoted = promotion_impact.xs(True, level='Promotion')['sum']
    non_promoted = promotion_impact.xs(False, level='Promotion')['sum']
    
    fig.add_trace(
        go.Bar(x=promoted.index, y=promoted.values,
               name='Promoted Revenue', marker_color='red'),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(x=non_promoted.index, y=non_promoted.values,
               name='Non-Promoted Revenue', marker_color='blue'),
        row=1, col=2
    )
    
    # Channel performance
    fig.add_trace(
        go.Bar(x=channel_performance.index, y=channel_performance['sum'],
               name='Channel Revenue', marker_color='purple'),
        row=2, col=1
    )
    
    # Regional sales
    fig.add_trace(
        go.Pie(labels=regional_pricing.index, values=regional_pricing['sum'],
               name="Regional Sales"),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Pricing, Promotions, and Partnerships Analysis",
        height=800,
        showlegend=True
    )
    
    fig.show()
    
    print("\nPRICING AND PROMOTION INSIGHTS:")
    print(f"Highest priced category: {pricing_analysis['mean'].idxmax()} (${pricing_analysis['mean'].max():.2f})")
    print(f"Lowest priced category: {pricing_analysis['mean'].idxmin()} (${pricing_analysis['mean'].min():.2f})")
    print(f"Promotion effectiveness: {promoted.sum() / non_promoted.sum():.2f}x revenue multiplier")
    print(f"Online vs Team Store revenue: {channel_performance.loc['Online', 'sum'] / channel_performance.loc['Team Store', 'sum']:.2f}x")
    
    return pricing_analysis, promotion_impact, channel_performance, regional_pricing

if __name__ == "__main__":
    # Run operational efficiency analysis
    source_eff, monthly_eff = analyze_operational_efficiency()
    
    # Run pricing and promotions analysis
    pricing_analysis, promotion_impact, channel_perf, regional_pricing = analyze_pricing_promotions()
