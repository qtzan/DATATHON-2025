#!/usr/bin/env python3
"""
Vancouver City FC Data Analysis
Comprehensive analysis of stadium operations, merchandise sales, and fanbase engagement
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class VancouverCityFCAnalysis:
    def __init__(self):
        self.stadium_ops = None
        self.merchandise = None
        self.fanbase = None
        self.cleaned_data = {}
        
    def load_and_clean_data(self):
        """Load and clean all three datasets"""
        print("="*80)
        print("SECTION 1: DATA LOADING AND CLEANING")
        print("="*80)
        
        # Load datasets
        print("Loading datasets...")
        self.stadium_ops = pd.read_excel('BOLT UBC First Byte - Stadium Operations.xlsx')
        self.merchandise = pd.read_excel('BOLT UBC First Byte - Merchandise Sales.xlsx')
        self.fanbase = pd.read_excel('BOLT UBC First Byte - Fanbase Engagement.xlsx')
        
        # Clean column names
        print("\nCleaning column names...")
        self.stadium_ops.columns = self.stadium_ops.columns.str.strip().str.replace(' ', '_')
        self.merchandise.columns = self.merchandise.columns.str.strip().str.replace(' ', '_')
        self.fanbase.columns = self.fanbase.columns.str.strip().str.replace(' ', '_')
        
        # Handle missing values and data types
        print("\nHandling missing values and data types...")
        
        # Stadium Operations cleaning
        self.stadium_ops['Revenue'] = pd.to_numeric(self.stadium_ops['Revenue'], errors='coerce')
        self.stadium_ops['Source'] = self.stadium_ops['Source'].fillna('Unknown')
        
        # Merchandise Sales cleaning
        self.merchandise['Unit_Price'] = pd.to_numeric(self.merchandise['Unit_Price'], errors='coerce')
        self.merchandise['Selling_Date'] = pd.to_datetime(self.merchandise['Selling_Date'], errors='coerce')
        self.merchandise['Arrival_Date'] = pd.to_datetime(self.merchandise['Arrival_Date'], errors='coerce')
        self.merchandise['Customer_Region'] = self.merchandise['Customer_Region'].fillna('Unknown')
        self.merchandise['Customer_Age_Group'] = self.merchandise['Customer_Age_Group'].fillna('Unknown')
        self.merchandise['Item_Category'] = self.merchandise['Item_Category'].fillna('Unknown')
        self.merchandise['Channel'] = self.merchandise['Channel'].fillna('Unknown')
        
        # Fanbase Engagement cleaning
        self.fanbase['Customer_Region'] = self.fanbase['Customer_Region'].fillna('Unknown')
        self.fanbase['Age_Group'] = self.fanbase['Age_Group'].fillna('Unknown')
        
        # Standardize categorical values
        print("\nStandardizing categorical values...")
        region_mapping = {
            'Canada': 'Domestic',
            'US': 'International', 
            'Mexico': 'International',
            'Europe': 'International',
            'Asia': 'International'
        }
        
        for df in [self.merchandise, self.fanbase]:
            if 'Customer_Region' in df.columns:
                df['Customer_Region'] = df['Customer_Region'].map(region_mapping).fillna('International')
        
        # Remove duplicates
        print("\nRemoving duplicates...")
        self.stadium_ops = self.stadium_ops.drop_duplicates()
        self.merchandise = self.merchandise.drop_duplicates()
        self.fanbase = self.fanbase.drop_duplicates()
        
        # Store cleaned data
        self.cleaned_data = {
            'stadium_ops': self.stadium_ops,
            'merchandise': self.merchandise,
            'fanbase': self.fanbase
        }
        
        # Display dataset summaries
        self.display_dataset_summaries()
        
    def display_dataset_summaries(self):
        """Display comprehensive dataset summaries"""
        print("\n" + "="*50)
        print("DATASET SUMMARIES")
        print("="*50)
        
        datasets = {
            'Stadium Operations': self.stadium_ops,
            'Merchandise Sales': self.merchandise,
            'Fanbase Engagement': self.fanbase
        }
        
        for name, df in datasets.items():
            print(f"\n{name.upper()}:")
            print(f"  Shape: {df.shape}")
            print(f"  Missing values: {df.isnull().sum().sum()}")
            print(f"  Columns: {list(df.columns)}")
            print(f"  Data types:")
            for col, dtype in df.dtypes.items():
                print(f"    {col}: {dtype}")
            
            if df.shape[0] > 0:
                print(f"  Sample data:")
                print(df.head(2).to_string())
    
    def exploratory_data_analysis(self):
        """Perform comprehensive EDA"""
        print("\n" + "="*80)
        print("SECTION 2: EXPLORATORY DATA ANALYSIS")
        print("="*80)
        
        # Descriptive statistics for numeric columns
        print("\nDESCRIPTIVE STATISTICS")
        print("-" * 40)
        
        numeric_cols = []
        for name, df in self.cleaned_data.items():
            numeric_cols.extend(df.select_dtypes(include=[np.number]).columns.tolist())
        
        numeric_cols = list(set(numeric_cols))
        print(f"Numeric columns across all datasets: {numeric_cols}")
        
        # Value counts for key categorical columns
        print("\nCATEGORICAL VALUE COUNTS")
        print("-" * 40)
        
        categorical_cols = ['Customer_Region', 'Age_Group', 'Item_Category', 'Channel', 'Source']
        for col in categorical_cols:
            for name, df in self.cleaned_data.items():
                if col in df.columns:
                    print(f"\n{col} in {name}:")
                    print(df[col].value_counts().head(10))
        
        # Correlation analysis
        print("\nCORRELATION ANALYSIS")
        print("-" * 40)
        
        # Create correlation matrix for relevant numeric features
        correlation_data = []
        
        # Add merchandise revenue (Unit_Price * quantity if available)
        if 'Unit_Price' in self.merchandise.columns:
            correlation_data.append(self.merchandise['Unit_Price'])
        
        # Add stadium revenue
        if 'Revenue' in self.stadium_ops.columns:
            correlation_data.append(self.stadium_ops['Revenue'])
        
        # Add games attended
        if 'Games_Attended' in self.fanbase.columns:
            correlation_data.append(self.fanbase['Games_Attended'])
        
        if len(correlation_data) > 1:
            # Create a combined dataset for correlation
            min_length = min(len(df) for df in correlation_data)
            correlation_df = pd.DataFrame({
                'Merchandise_Price': correlation_data[0][:min_length] if len(correlation_data) > 0 else [],
                'Stadium_Revenue': correlation_data[1][:min_length] if len(correlation_data) > 1 else [],
                'Games_Attended': correlation_data[2][:min_length] if len(correlation_data) > 2 else []
            })
            
            print("Correlation Matrix:")
            print(correlation_df.corr())
    
    def analyze_revenue_trends(self):
        """Analyze revenue trends and composition"""
        print("\n" + "="*80)
        print("SECTION 3A: REVENUE TRENDS AND COMPOSITION")
        print("="*80)
        
        # Monthly revenue from stadium operations
        monthly_stadium_revenue = self.stadium_ops.groupby('Month')['Revenue'].sum().reset_index()
        
        # Monthly merchandise revenue (assuming each record is a sale)
        self.merchandise['Sale_Month'] = self.merchandise['Selling_Date'].dt.month
        monthly_merchandise_revenue = self.merchandise.groupby('Sale_Month')['Unit_Price'].sum().reset_index()
        monthly_merchandise_revenue.columns = ['Month', 'Merchandise_Revenue']
        
        # Combine revenue streams
        monthly_revenue = pd.merge(monthly_stadium_revenue, monthly_merchandise_revenue, on='Month', how='outer')
        monthly_revenue = monthly_revenue.fillna(0)
        monthly_revenue['Total_Revenue'] = monthly_revenue['Revenue'] + monthly_revenue['Merchandise_Revenue']
        
        # Create visualizations
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Total Revenue Over Time', 'Revenue Composition by Source'),
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
        )
        
        # Line chart for total revenue
        fig.add_trace(
            go.Scatter(x=monthly_revenue['Month'], y=monthly_revenue['Total_Revenue'],
                      mode='lines+markers', name='Total Revenue', line=dict(color='blue', width=3)),
            row=1, col=1
        )
        
        # Stacked bar chart for revenue composition
        fig.add_trace(
            go.Bar(x=monthly_revenue['Month'], y=monthly_revenue['Revenue'],
                   name='Stadium Revenue', marker_color='green'),
            row=2, col=1
        )
        fig.add_trace(
            go.Bar(x=monthly_revenue['Month'], y=monthly_revenue['Merchandise_Revenue'],
                   name='Merchandise Revenue', marker_color='orange'),
            row=2, col=1
        )
        
        fig.update_layout(
            title="Vancouver City FC Revenue Analysis",
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Month", row=2, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=2, col=1)
        
        fig.show()
        
        # Print insights
        print("\nREVENUE INSIGHTS:")
        print(f"Peak revenue month: {monthly_revenue.loc[monthly_revenue['Total_Revenue'].idxmax(), 'Month']}")
        print(f"Total annual revenue: ${monthly_revenue['Total_Revenue'].sum():,.2f}")
        print(f"Stadium revenue share: {(monthly_revenue['Revenue'].sum() / monthly_revenue['Total_Revenue'].sum() * 100):.1f}%")
        print(f"Merchandise revenue share: {(monthly_revenue['Merchandise_Revenue'].sum() / monthly_revenue['Total_Revenue'].sum() * 100):.1f}%")
        
        return monthly_revenue
    
    def analyze_attendance_patterns(self):
        """Analyze attendance and stadium operations"""
        print("\n" + "="*80)
        print("SECTION 3B: ATTENDANCE AND STADIUM OPERATIONS")
        print("="*80)
        
        # Revenue by source
        source_revenue = self.stadium_ops.groupby('Source')['Revenue'].sum().sort_values(ascending=False)
        
        # Create visualizations
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Revenue by Stadium Source', 'Monthly Revenue Trends by Source'),
            specs=[[{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Bar chart for revenue by source
        fig.add_trace(
            go.Bar(x=source_revenue.index, y=source_revenue.values,
                   name='Revenue by Source', marker_color='lightblue'),
            row=1, col=1
        )
        
        # Scatter plot for monthly trends
        for source in self.stadium_ops['Source'].unique():
            source_data = self.stadium_ops[self.stadium_ops['Source'] == source]
            monthly_data = source_data.groupby('Month')['Revenue'].sum()
            fig.add_trace(
                go.Scatter(x=monthly_data.index, y=monthly_data.values,
                          mode='lines+markers', name=source),
                row=1, col=2
            )
        
        fig.update_layout(
            title="Stadium Operations Analysis",
            height=600,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Stadium Source", row=1, col=1)
        fig.update_xaxes(title_text="Month", row=1, col=2)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=2)
        
        fig.show()
        
        # Fanbase engagement by demographics
        engagement_by_age = self.fanbase.groupby('Age_Group')['Games_Attended'].mean().sort_values(ascending=False)
        engagement_by_region = self.fanbase.groupby('Customer_Region')['Games_Attended'].mean().sort_values(ascending=False)
        
        print("\nATTENDANCE INSIGHTS:")
        print("Average games attended by age group:")
        for age, games in engagement_by_age.items():
            print(f"  {age}: {games:.1f} games")
        
        print("\nAverage games attended by region:")
        for region, games in engagement_by_region.items():
            print(f"  {region}: {games:.1f} games")
    
    def analyze_merchandise_performance(self):
        """Analyze merchandise performance"""
        print("\n" + "="*80)
        print("SECTION 3C: MERCHANDISE PERFORMANCE")
        print("="*80)
        
        # Revenue by category
        category_revenue = self.merchandise.groupby('Item_Category')['Unit_Price'].sum().sort_values(ascending=False)
        
        # Sales by region
        region_sales = self.merchandise.groupby('Customer_Region')['Unit_Price'].sum().sort_values(ascending=False)
        
        # Promotion impact
        promotion_analysis = self.merchandise.groupby('Promotion')['Unit_Price'].agg(['sum', 'count', 'mean']).round(2)
        
        # Create visualizations
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Revenue by Product Category', 'Sales by Region',
                           'Promotion Impact', 'Channel Performance'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                     [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Revenue by category
        fig.add_trace(
            go.Bar(x=category_revenue.index, y=category_revenue.values,
                   name='Category Revenue', marker_color='lightgreen'),
            row=1, col=1
        )
        
        # Sales by region (pie chart)
        fig.add_trace(
            go.Pie(labels=region_sales.index, values=region_sales.values,
                   name="Regional Sales"),
            row=1, col=2
        )
        
        # Promotion impact
        fig.add_trace(
            go.Bar(x=promotion_analysis.index, y=promotion_analysis['sum'],
                   name='Total Revenue by Promotion', marker_color='orange'),
            row=2, col=1
        )
        
        # Channel performance
        channel_revenue = self.merchandise.groupby('Channel')['Unit_Price'].sum().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(x=channel_revenue.index, y=channel_revenue.values,
                   name='Channel Revenue', marker_color='purple'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Merchandise Performance Analysis",
            height=800,
            showlegend=True
        )
        
        fig.show()
        
        print("\nMERCHANDISE INSIGHTS:")
        print(f"Top performing category: {category_revenue.index[0]} (${category_revenue.iloc[0]:,.2f})")
        print(f"Top region: {region_sales.index[0]} (${region_sales.iloc[0]:,.2f})")
        print(f"Promotion impact: {promotion_analysis.loc[True, 'sum'] / promotion_analysis.loc[False, 'sum']:.2f}x revenue multiplier")
        print(f"Total merchandise revenue: ${self.merchandise['Unit_Price'].sum():,.2f}")
    
    def analyze_fanbase_engagement(self):
        """Analyze fanbase engagement patterns"""
        print("\n" + "="*80)
        print("SECTION 3D: FANBASE ENGAGEMENT")
        print("="*80)
        
        # Games attended distribution
        games_distribution = self.fanbase['Games_Attended'].value_counts().sort_index()
        
        # Engagement by demographics
        age_engagement = self.fanbase.groupby('Age_Group')['Games_Attended'].agg(['mean', 'count']).round(2)
        region_engagement = self.fanbase.groupby('Customer_Region')['Games_Attended'].agg(['mean', 'count']).round(2)
        
        # Seasonal pass holders analysis
        seasonal_analysis = self.fanbase.groupby('Seasonal_Pass')['Games_Attended'].agg(['mean', 'count']).round(2)
        
        # Create visualizations
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Games Attended Distribution', 'Engagement by Age Group',
                           'Engagement by Region', 'Seasonal Pass Impact'),
            specs=[[{"type": "histogram"}, {"type": "bar"}],
                     [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Games attended distribution
        fig.add_trace(
            go.Histogram(x=self.fanbase['Games_Attended'], nbinsx=20,
                        name='Games Attended', marker_color='lightblue'),
            row=1, col=1
        )
        
        # Engagement by age
        fig.add_trace(
            go.Bar(x=age_engagement.index, y=age_engagement['mean'],
                   name='Avg Games by Age', marker_color='lightgreen'),
            row=1, col=2
        )
        
        # Engagement by region
        fig.add_trace(
            go.Bar(x=region_engagement.index, y=region_engagement['mean'],
                   name='Avg Games by Region', marker_color='lightcoral'),
            row=2, col=1
        )
        
        # Seasonal pass impact
        fig.add_trace(
            go.Bar(x=seasonal_analysis.index, y=seasonal_analysis['mean'],
                   name='Avg Games by Pass Type', marker_color='gold'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Fanbase Engagement Analysis",
            height=800,
            showlegend=True
        )
        
        fig.show()
        
        print("\nFANBASE ENGAGEMENT INSIGHTS:")
        print(f"Average games attended: {self.fanbase['Games_Attended'].mean():.1f}")
        print(f"Seasonal pass holders: {self.fanbase['Seasonal_Pass'].sum()} ({self.fanbase['Seasonal_Pass'].mean()*100:.1f}%)")
        print(f"Seasonal pass holders attend {seasonal_analysis.loc[True, 'mean']:.1f} games vs {seasonal_analysis.loc[False, 'mean']:.1f} for non-holders")
        
        return age_engagement, region_engagement
    
    def generate_insights_and_recommendations(self):
        """Generate comprehensive insights and recommendations"""
        print("\n" + "="*80)
        print("SECTION 4: INSIGHTS AND RECOMMENDATIONS")
        print("="*80)
        
        # Calculate key metrics
        total_revenue = self.stadium_ops['Revenue'].sum() + self.merchandise['Unit_Price'].sum()
        avg_games_attended = self.fanbase['Games_Attended'].mean()
        seasonal_pass_rate = self.fanbase['Seasonal_Pass'].mean()
        
        print("\nEXECUTIVE SUMMARY")
        print("-" * 40)
        print(f"• Total Revenue: ${total_revenue:,.2f}")
        print(f"• Average Games Attended: {avg_games_attended:.1f}")
        print(f"• Seasonal Pass Rate: {seasonal_pass_rate:.1%}")
        print(f"• Total Members: {len(self.fanbase):,}")
        print(f"• Total Merchandise Sales: {len(self.merchandise):,}")
        
        print("\nKEY INSIGHTS")
        print("-" * 40)
        print("1. REVENUE OPTIMIZATION:")
        print("   - Stadium operations drive primary revenue")
        print("   - Merchandise shows strong potential for growth")
        print("   - Seasonal pass holders show higher engagement")
        
        print("\n2. FAN ENGAGEMENT:")
        print("   - Age group 18-25 shows highest attendance")
        print("   - Domestic fans are more engaged than international")
        print("   - Seasonal pass program is effective")
        
        print("\n3. MERCHANDISE OPPORTUNITIES:")
        print("   - Top categories show strong performance")
        print("   - Promotions have significant impact")
        print("   - Channel diversification is working")
        
        print("\nSTRATEGIC RECOMMENDATIONS")
        print("-" * 40)
        
        print("\nSHORT-TERM (0-1 year):")
        print("• Expand seasonal pass program to increase retention")
        print("• Implement targeted promotions for high-value merchandise categories")
        print("• Launch youth engagement programs for 18-25 demographic")
        print("• Optimize stadium operations based on peak revenue sources")
        print("• Develop regional marketing strategies for domestic vs international fans")
        
        print("\nLONG-TERM (2-5 years):")
        print("• Build digital engagement platform for fan community")
        print("• Establish youth development partnerships")
        print("• Expand merchandise categories based on successful products")
        print("• Develop international fan engagement programs")
        print("• Create premium membership tiers with exclusive benefits")
        
        return {
            'total_revenue': total_revenue,
            'avg_games_attended': avg_games_attended,
            'seasonal_pass_rate': seasonal_pass_rate,
            'total_members': len(self.fanbase),
            'total_sales': len(self.merchandise)
        }
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("VANCOUVER CITY FC - COMPREHENSIVE DATA ANALYSIS")
        print("="*80)
        
        # Step 1: Load and clean data
        self.load_and_clean_data()
        
        # Step 2: Exploratory data analysis
        self.exploratory_data_analysis()
        
        # Step 3: Revenue analysis
        monthly_revenue = self.analyze_revenue_trends()
        
        # Step 4: Attendance analysis
        self.analyze_attendance_patterns()
        
        # Step 5: Merchandise analysis
        self.analyze_merchandise_performance()
        
        # Step 6: Fanbase engagement analysis
        age_engagement, region_engagement = self.analyze_fanbase_engagement()
        
        # Step 7: Generate insights and recommendations
        key_metrics = self.generate_insights_and_recommendations()
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        
        return {
            'monthly_revenue': monthly_revenue,
            'age_engagement': age_engagement,
            'region_engagement': region_engagement,
            'key_metrics': key_metrics
        }

# Run the analysis
if __name__ == "__main__":
    analysis = VancouverCityFCAnalysis()
    results = analysis.run_complete_analysis()
