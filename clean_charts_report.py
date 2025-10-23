#!/usr/bin/env python3
"""
Vancouver City FC - Clean Charts Report
Generate clean, static charts as images
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style for clean, professional charts
plt.style.use('dark_background')
sns.set_palette("husl")

def create_clean_charts():
    """Create clean, professional charts as images"""
    
    # Load and clean data
    print("Loading and cleaning datasets...")
    stadium_ops = pd.read_excel('BOLT UBC First Byte - Stadium Operations.xlsx')
    merchandise = pd.read_excel('BOLT UBC First Byte - Merchandise Sales.xlsx')
    fanbase = pd.read_excel('BOLT UBC First Byte - Fanbase Engagement.xlsx')
    
    # Clean data
    merchandise['Customer_Region'] = merchandise['Customer_Region'].fillna('International')
    merchandise['Customer_Age_Group'] = merchandise['Customer_Age_Group'].fillna('Unknown')
    merchandise['Selling_Date'] = pd.to_datetime(merchandise['Selling_Date'], errors='coerce')
    merchandise['Sale_Month'] = merchandise['Selling_Date'].dt.month
    
    # Standardize regions
    region_mapping = {'Canada': 'Domestic', 'US': 'International', 'Mexico': 'International'}
    for df in [merchandise, fanbase]:
        if 'Customer_Region' in df.columns:
            df['Customer_Region'] = df['Customer_Region'].map(region_mapping).fillna('International')
    
    # Calculate key metrics
    total_revenue = stadium_ops['Revenue'].sum() + merchandise['Unit_Price'].sum()
    stadium_revenue = stadium_ops['Revenue'].sum()
    merchandise_revenue = merchandise['Unit_Price'].sum()
    
    print("Creating clean charts...")
    
    # Chart 1: Revenue Composition Pie Chart
    fig, ax = plt.subplots(figsize=(16, 14))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#1e1e2e')
    
    revenue_data = {
        'Stadium Operations': stadium_revenue,
        'Merchandise Sales': merchandise_revenue
    }
    
    colors = ['#00ffff', '#ff0080']
    wedges, texts, autotexts = ax.pie(
        revenue_data.values(), 
        labels=revenue_data.keys(),
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        textprops={'color': 'white', 'fontsize': 32, 'weight': 'bold'},
        wedgeprops={'linewidth': 4, 'edgecolor': 'white'}
    )
    
    # Add value labels with better spacing and positioning
    for i, (wedge, value) in enumerate(zip(wedges, revenue_data.values())):
        angle = (wedge.theta2 + wedge.theta1) / 2
        # Position labels further out to avoid overlapping
        x = 0.9 * np.cos(np.radians(angle))
        y = 0.9 * np.sin(np.radians(angle))
        ax.text(x, y, f'${value:,.0f}', ha='center', va='center', 
                fontsize=24, color='white', weight='bold',
                bbox=dict(boxstyle="round,pad=0.4", facecolor='black', alpha=0.8, edgecolor='white', linewidth=1))
    
    ax.set_title('Revenue Composition', fontsize=40, color='#00ffff', weight='bold', pad=40)
    plt.tight_layout()
    plt.savefig('revenue_composition.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    plt.close()
    
    # Chart 2a: Games Attended by Age Group
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#1e1e2e')
    
    age_attendance = fanbase.groupby('Age_Group')['Games_Attended'].mean().sort_values(ascending=True)
    
    # Use distinct colors for each age group
    colors = ['#00ffff', '#ff6b35', '#4ecdc4', '#45b7d1', '#96ceb4']
    bars = ax.barh(age_attendance.index, age_attendance.values, 
                   color=colors[:len(age_attendance)], alpha=0.8, edgecolor='white', linewidth=3)
    
    # Add value labels with better positioning and background
    for i, (bar, value) in enumerate(zip(bars, age_attendance.values)):
        ax.text(value + 0.3, bar.get_y() + bar.get_height()/2, 
                f'{value:.1f}', va='center', ha='left', 
                color='white', fontsize=22, weight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
    
    ax.set_title('Games Attended by Age Group', fontsize=32, color='#00ffff', weight='bold', pad=30)
    ax.set_xlabel('Average Games Attended', color='white', fontsize=24)
    ax.set_ylabel('Age Group', color='white', fontsize=24)
    ax.tick_params(colors='white', labelsize=20)
    ax.grid(True, alpha=0.3, color='#00ffff')
    
    plt.tight_layout()
    plt.savefig('fan_age_groups.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    plt.close()
    
    # Chart 2b: Seasonal Pass Impact
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#1e1e2e')
    
    seasonal_impact = fanbase.groupby('Seasonal_Pass')['Games_Attended'].mean()
    labels = ['Non-Seasonal Pass', 'Seasonal Pass']
    values = [seasonal_impact[False], seasonal_impact[True]]
    # Use high contrast colors
    colors = ['#ff4757', '#00ffff']
    
    bars = ax.bar(labels, values, color=colors, alpha=0.8, edgecolor='white', linewidth=4)
    
    # Add value labels with better spacing and background
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{value:.1f}', ha='center', va='bottom', 
                color='white', fontsize=24, weight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
    
    ax.set_title('Seasonal Pass Impact', fontsize=32, color='#00ffff', weight='bold', pad=30)
    ax.set_ylabel('Average Games Attended', color='white', fontsize=24)
    ax.tick_params(colors='white', labelsize=20)
    ax.grid(True, alpha=0.3, color='#00ffff')
    
    plt.tight_layout()
    plt.savefig('fan_seasonal_pass.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    plt.close()
    
    
    # Chart 3a: Revenue by Category
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#1e1e2e')
    
    category_revenue = merchandise.groupby('Item_Category')['Unit_Price'].sum().sort_values(ascending=True)
    
    # Use distinct colors for better contrast
    colors = ['#00ffff', '#ff6b35', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
    bars = ax.barh(category_revenue.index, category_revenue.values, 
                   color=colors[:len(category_revenue)], alpha=0.8, edgecolor='white', linewidth=3)
    
    # Add value labels with better positioning and background
    for i, (bar, value) in enumerate(zip(bars, category_revenue.values)):
        ax.text(value + max(category_revenue.values) * 0.03, bar.get_y() + bar.get_height()/2, 
                f'${value:,.0f}', va='center', ha='left', 
                color='white', fontsize=20, weight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
    
    ax.set_title('Revenue by Category', fontsize=32, color='#00ffff', weight='bold', pad=30)
    ax.set_xlabel('Revenue ($)', color='white', fontsize=24)
    ax.tick_params(colors='white', labelsize=18)
    ax.grid(True, alpha=0.3, color='#00ffff')
    
    plt.tight_layout()
    plt.savefig('merchandise_category.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    plt.close()
    
    # Chart 3b: Channel Performance
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#1e1e2e')
    
    channel_analysis = merchandise.groupby('Channel')['Unit_Price'].sum()
    # Use more contrasting colors
    colors = ['#00ffff', '#ff4757']
    
    wedges, texts, autotexts = ax.pie(
        channel_analysis.values,
        labels=channel_analysis.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        textprops={'color': 'white', 'fontsize': 24, 'weight': 'bold'},
        wedgeprops={'linewidth': 4, 'edgecolor': 'white'}
    )
    
    ax.set_title('Channel Performance', fontsize=32, color='#00ffff', weight='bold', pad=30)
    
    plt.tight_layout()
    plt.savefig('merchandise_channel.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    plt.close()
    
    # Chart 3c: Promotion Impact
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#1e1e2e')
    
    promotion_analysis = merchandise.groupby('Promotion')['Unit_Price'].sum()
    labels = ['No Promotion', 'Promotion']
    values = [promotion_analysis[False], promotion_analysis[True]]
    # Use high contrast colors
    colors = ['#ff4757', '#00ffff']
    
    bars = ax.bar(labels, values, color=colors, alpha=0.8, edgecolor='white', linewidth=4)
    
    # Add value labels with better spacing and background
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values) * 0.03, 
                f'${value:,.0f}', ha='center', va='bottom', 
                color='white', fontsize=22, weight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
    
    ax.set_title('Promotion Impact', fontsize=32, color='#00ffff', weight='bold', pad=30)
    ax.set_ylabel('Revenue ($)', color='white', fontsize=24)
    ax.tick_params(colors='white', labelsize=20)
    ax.grid(True, alpha=0.3, color='#00ffff')
    
    plt.tight_layout()
    plt.savefig('merchandise_promotion.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    plt.close()
    
    # Chart 4: Monthly Revenue Trends
    fig, ax = plt.subplots(figsize=(24, 14))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#1e1e2e')
    
    # Monthly stadium revenue
    monthly_stadium = stadium_ops.groupby('Month')['Revenue'].sum()
    monthly_merchandise = merchandise.groupby('Sale_Month')['Unit_Price'].sum()
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    x = np.arange(len(months))
    width = 0.4  # Increased width for better separation
    
    bars1 = ax.bar(x - width/2, monthly_stadium.values, width, 
                   label='Stadium Operations', color='#00ffff', alpha=0.8, 
                   edgecolor='white', linewidth=4)
    bars2 = ax.bar(x + width/2, monthly_merchandise.values, width, 
                   label='Merchandise Sales', color='#ff4757', alpha=0.8, 
                   edgecolor='white', linewidth=4)
    
    # Add value labels on bars with much better spacing and background
    max_height = max(monthly_stadium.max(), monthly_merchandise.max())
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        
        # Only show labels for significant values to reduce clutter
        if height1 > max_height * 0.1:  # Only show if > 10% of max
            ax.text(bar1.get_x() + bar1.get_width()/2, height1 + max_height * 0.03,
                   f'${height1:,.0f}', ha='center', va='bottom', 
                   color='white', fontsize=16, weight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8))
        
        if height2 > max_height * 0.1:  # Only show if > 10% of max
            ax.text(bar2.get_x() + bar2.get_width()/2, height2 + max_height * 0.03,
                   f'${height2:,.0f}', ha='center', va='bottom', 
                   color='white', fontsize=16, weight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8))
    
    ax.set_title('Monthly Revenue Trends', fontsize=36, color='#00ffff', weight='bold', pad=50)
    ax.set_xlabel('Month', color='white', fontsize=28)
    ax.set_ylabel('Revenue ($)', color='white', fontsize=28)
    ax.set_xticks(x)
    ax.set_xticklabels(months, color='white', fontsize=22)
    ax.tick_params(colors='white', labelsize=22)
    ax.legend(fontsize=24, loc='upper right', framealpha=0.9)
    ax.grid(True, alpha=0.3, color='#00ffff')
    
    # Add more space between bars and labels
    ax.set_ylim(0, max_height * 1.15)
    
    plt.tight_layout()
    plt.savefig('monthly_trends.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    plt.close()
    
    print("✓ Clean charts created:")
    print("  - revenue_composition.png")
    print("  - fan_age_groups.png")
    print("  - fan_seasonal_pass.png")
    print("  - merchandise_category.png")
    print("  - merchandise_channel.png")
    print("  - merchandise_promotion.png")
    print("  - monthly_trends.png")

if __name__ == "__main__":
    create_clean_charts()
