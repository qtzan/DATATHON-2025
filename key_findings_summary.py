#!/usr/bin/env python3
"""
Key Findings Summary and Dashboard for Vancouver City FC
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_summary_table():
    """Create comprehensive summary table of key findings"""
    
    # Key metrics summary
    summary_data = {
        'Metric': [
            'Total Revenue',
            'Stadium Revenue Share',
            'Merchandise Revenue Share', 
            'Total Members',
            'Average Games Attended',
            'Seasonal Pass Rate',
            'Seasonal Pass Holder Games',
            'Non-Seasonal Pass Games',
            'Online Merchandise Share',
            'Team Store Merchandise Share',
            'Top Merchandise Category',
            'Most Efficient Stadium Source',
            'Peak Revenue Month',
            'Promotion Effectiveness',
            'International Fan Share'
        ],
        'Value': [
            '$19,690,647',
            '67.2%',
            '32.8%',
            '70,000',
            '5.7 games',
            '6.8%',
            '22.4 games',
            '4.5 games',
            '80%',
            '20%',
            'Jersey ($4.1M)',
            'Lower Bowl',
            'February',
            '0.56x multiplier',
            '10%'
        ],
        'Insight': [
            'Strong revenue base with growth potential',
            'Primary revenue driver, stable performance',
            'Significant growth opportunity identified',
            'Large, engaged fanbase',
            'Consistent engagement across demographics',
            'Low adoption with high engagement multiplier',
            'Exceptional loyalty and retention',
            'Standard engagement level',
            'Dominant sales channel with 4x advantage',
            'Physical presence for community connection',
            'Premium product with strong performance',
            'Highest revenue per event efficiency',
            'Seasonal peak performance month',
            'Underperforming, needs optimization',
            'Growth opportunity for expansion'
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    
    print("="*80)
    print("VANCOUVER CITY FC - KEY FINDINGS SUMMARY")
    print("="*80)
    print(summary_df.to_string(index=False))
    
    return summary_df

def create_executive_dashboard():
    """Create executive dashboard with key visualizations"""
    
    # Load data for dashboard
    stadium_ops = pd.read_excel('BOLT UBC First Byte - Stadium Operations.xlsx')
    merchandise = pd.read_excel('BOLT UBC First Byte - Merchandise Sales.xlsx')
    fanbase = pd.read_excel('BOLT UBC First Byte - Fanbase Engagement.xlsx')
    
    # Create dashboard
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('Revenue by Source', 'Monthly Revenue Trend',
                       'Merchandise Category Performance', 'Fan Engagement by Age',
                       'Seasonal Pass Impact', 'Channel Performance'),
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Revenue by source
    source_revenue = stadium_ops.groupby('Source')['Revenue'].sum().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=source_revenue.index, y=source_revenue.values,
               name='Stadium Revenue', marker_color='lightblue'),
        row=1, col=1
    )
    
    # Monthly revenue trend
    monthly_revenue = stadium_ops.groupby('Month')['Revenue'].sum()
    fig.add_trace(
        go.Scatter(x=monthly_revenue.index, y=monthly_revenue.values,
                  mode='lines+markers', name='Monthly Revenue', line=dict(color='green')),
        row=1, col=2
    )
    
    # Merchandise category performance
    category_revenue = merchandise.groupby('Item_Category')['Unit_Price'].sum().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=category_revenue.index, y=category_revenue.values,
               name='Category Revenue', marker_color='lightgreen'),
        row=2, col=1
    )
    
    # Fan engagement by age
    age_engagement = fanbase.groupby('Age_Group')['Games_Attended'].mean()
    fig.add_trace(
        go.Bar(x=age_engagement.index, y=age_engagement.values,
               name='Avg Games by Age', marker_color='lightcoral'),
        row=2, col=2
    )
    
    # Seasonal pass impact
    seasonal_impact = fanbase.groupby('Seasonal_Pass')['Games_Attended'].mean()
    fig.add_trace(
        go.Bar(x=seasonal_impact.index, y=seasonal_impact.values,
               name='Games by Pass Type', marker_color='gold'),
        row=3, col=1
    )
    
    # Channel performance
    channel_revenue = merchandise.groupby('Channel')['Unit_Price'].sum()
    fig.add_trace(
        go.Bar(x=channel_revenue.index, y=channel_revenue.values,
               name='Channel Revenue', marker_color='purple'),
        row=3, col=2
    )
    
    fig.update_layout(
        title="Vancouver City FC - Executive Dashboard",
        height=1200,
        showlegend=True
    )
    
    fig.show()
    
    return fig

def generate_recommendations_table():
    """Generate structured recommendations table"""
    
    recommendations_data = {
        'Priority': ['High', 'High', 'Medium', 'Medium', 'Low', 'Low'],
        'Timeframe': ['0-6 months', '0-6 months', '6-12 months', '6-12 months', '12-24 months', '12-24 months'],
        'Initiative': [
            'Expand Seasonal Pass Program',
            'Optimize Merchandise Promotions',
            'Enhance Online Presence',
            'Develop Youth Programs',
            'International Fan Engagement',
            'Premium Membership Tiers'
        ],
        'Expected Impact': [
            '5x engagement multiplier',
            'Fix 0.56x promotion effectiveness',
            'Leverage 4x online advantage',
            'Target 44.8% 18-25 demographic',
            'Grow 10% international segment',
            'Create premium revenue streams'
        ],
        'Investment Required': [
            'Low - Marketing focus',
            'Low - Strategy optimization',
            'Medium - Platform development',
            'Medium - Program development',
            'High - Market expansion',
            'High - System development'
        ],
        'ROI Timeline': [
            '3-6 months',
            '1-3 months',
            '6-12 months',
            '12-18 months',
            '18-36 months',
            '12-24 months'
        ]
    }
    
    recommendations_df = pd.DataFrame(recommendations_data)
    
    print("\n" + "="*80)
    print("STRATEGIC RECOMMENDATIONS MATRIX")
    print("="*80)
    print(recommendations_df.to_string(index=False))
    
    return recommendations_df

if __name__ == "__main__":
    # Create summary table
    summary_df = create_summary_table()
    
    # Create executive dashboard
    dashboard = create_executive_dashboard()
    
    # Generate recommendations
    recommendations_df = generate_recommendations_table()
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - ALL DELIVERABLES GENERATED")
    print("="*80)
