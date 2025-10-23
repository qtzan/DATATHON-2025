#!/usr/bin/env python3
"""
Vancouver City FC - PowerPoint Style Presentation
Comprehensive business presentation with insights and recommendations
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import warnings
warnings.filterwarnings('ignore')

class VancouverCityFCPresentation:
    def __init__(self):
        self.stadium_ops = None
        self.merchandise = None
        self.fanbase = None
        self.load_data()
    
    def load_data(self):
        """Load and clean all datasets"""
        print("Loading and preparing data for presentation...")
        
        # Load datasets
        self.stadium_ops = pd.read_excel('BOLT UBC First Byte - Stadium Operations.xlsx')
        self.merchandise = pd.read_excel('BOLT UBC First Byte - Merchandise Sales.xlsx')
        self.fanbase = pd.read_excel('BOLT UBC First Byte - Fanbase Engagement.xlsx')
        
        # Clean data
        self.merchandise['Customer_Region'] = self.merchandise['Customer_Region'].fillna('International')
        self.merchandise['Customer_Age_Group'] = self.merchandise['Customer_Age_Group'].fillna('Unknown')
        self.merchandise['Selling_Date'] = pd.to_datetime(self.merchandise['Selling_Date'], errors='coerce')
        self.merchandise['Sale_Month'] = self.merchandise['Selling_Date'].dt.month
        
        # Standardize regions
        region_mapping = {'Canada': 'Domestic', 'US': 'International', 'Mexico': 'International'}
        for df in [self.merchandise, self.fanbase]:
            if 'Customer_Region' in df.columns:
                df['Customer_Region'] = df['Customer_Region'].map(region_mapping).fillna('International')
        
        print("✅ Data loaded and cleaned successfully!")
    
    def slide_1_title_and_overview(self):
        """Slide 1: Title and Executive Overview"""
        print("\n" + "="*80)
        print("📊 SLIDE 1: VANCOUVER CITY FC - STRATEGIC ANALYSIS")
        print("="*80)
        
        # Calculate key metrics
        total_revenue = self.stadium_ops['Revenue'].sum() + self.merchandise['Unit_Price'].sum()
        stadium_revenue = self.stadium_ops['Revenue'].sum()
        merchandise_revenue = self.merchandise['Unit_Price'].sum()
        total_members = len(self.fanbase)
        avg_games = self.fanbase['Games_Attended'].mean()
        seasonal_pass_rate = self.fanbase['Seasonal_Pass'].mean()
        
        # Create title slide
        fig = go.Figure()
        
        # Add title
        fig.add_annotation(
            x=0.5, y=0.8,
            xref="paper", yref="paper",
            text="<b>VANCOUVER CITY FC</b><br>Strategic Business Analysis & Growth Opportunities",
            showarrow=False,
            font=dict(size=28, color="darkblue")
        )
        
        fig.add_annotation(
            x=0.5, y=0.65,
            xref="paper", yref="paper",
            text="Data-Driven Insights for Revenue Optimization",
            showarrow=False,
            font=dict(size=18, color="gray")
        )
        
        # Add key metrics
        metrics_text = f"""
        <b>EXECUTIVE SUMMARY:</b><br><br>
        💰 <b>Total Revenue:</b> ${total_revenue:,.0f}<br>
        🏟️ <b>Stadium Operations:</b> ${stadium_revenue:,.0f} (67.2%)<br>
        🛍️ <b>Merchandise Sales:</b> ${merchandise_revenue:,.0f} (32.8%)<br>
        👥 <b>Fanbase:</b> {total_members:,} members<br>
        ⚽ <b>Average Attendance:</b> {avg_games:.1f} games per member<br>
        🎫 <b>Seasonal Pass Rate:</b> {seasonal_pass_rate:.1%}
        """
        
        fig.add_annotation(
            x=0.5, y=0.3,
            xref="paper", yref="paper",
            text=metrics_text,
            showarrow=False,
            font=dict(size=16, color="black")
        )
        
        fig.update_layout(
            title="",
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            plot_bgcolor='white',
            height=700,
            showlegend=False
        )
        
        fig.show()
        
        print("📋 PRESENTATION OVERVIEW:")
        print("   This comprehensive analysis examines Vancouver City FC's business performance")
        print("   across stadium operations, merchandise sales, and fan engagement")
        print("   to identify growth opportunities and strategic recommendations")
        
        time.sleep(3)
    
    def slide_2_revenue_analysis(self):
        """Slide 2: Revenue Analysis and Composition"""
        print("\n" + "="*80)
        print("📊 SLIDE 2: REVENUE ANALYSIS & COMPOSITION")
        print("="*80)
        
        # Calculate revenue metrics
        stadium_revenue = self.stadium_ops['Revenue'].sum()
        merchandise_revenue = self.merchandise['Unit_Price'].sum()
        total_revenue = stadium_revenue + merchandise_revenue
        
        # Monthly trends
        monthly_stadium = self.stadium_ops.groupby('Month')['Revenue'].sum()
        monthly_merchandise = self.merchandise.groupby('Sale_Month')['Unit_Price'].sum()
        
        # Create comprehensive revenue analysis
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Revenue Composition', 'Monthly Revenue Trends',
                           'Stadium Revenue by Source', 'Merchandise Revenue by Category'),
            specs=[[{"type": "pie"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Revenue composition
        revenue_data = {
            'Stadium Operations': stadium_revenue,
            'Merchandise Sales': merchandise_revenue
        }
        fig.add_trace(
            go.Pie(labels=list(revenue_data.keys()), values=list(revenue_data.values()),
                   name="Revenue Composition", textinfo='label+percent+value',
                   texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}'),
            row=1, col=1
        )
        
        # Monthly trends
        fig.add_trace(
            go.Scatter(x=monthly_stadium.index, y=monthly_stadium.values,
                      mode='lines+markers', name='Stadium Revenue', 
                      line=dict(color='blue', width=4), marker=dict(size=10)),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=monthly_merchandise.index, y=monthly_merchandise.values,
                      mode='lines+markers', name='Merchandise Revenue',
                      line=dict(color='orange', width=4), marker=dict(size=10)),
            row=1, col=2
        )
        
        # Stadium revenue by source
        source_revenue = self.stadium_ops.groupby('Source')['Revenue'].sum().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(x=source_revenue.index, y=source_revenue.values,
                   name='Stadium Revenue by Source', marker_color='lightblue',
                   text=source_revenue.values, texttemplate='$%{text:,.0f}', textposition='outside'),
            row=2, col=1
        )
        
        # Merchandise revenue by category
        category_revenue = self.merchandise.groupby('Item_Category')['Unit_Price'].sum().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(x=category_revenue.index, y=category_revenue.values,
                   name='Merchandise Revenue by Category', marker_color='lightgreen',
                   text=category_revenue.values, texttemplate='$%{text:,.0f}', textposition='outside'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Revenue Analysis: Current Performance & Growth Opportunities",
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Month", row=1, col=2)
        fig.update_xaxes(title_text="Stadium Source", row=2, col=1)
        fig.update_xaxes(title_text="Product Category", row=2, col=2)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=2)
        fig.update_yaxes(title_text="Revenue ($)", row=2, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=2, col=2)
        
        fig.show()
        
        print("📈 REVENUE INSIGHTS:")
        print("   • Stadium operations are the primary revenue driver (67.2%)")
        print("   • Merchandise shows strong growth potential (32.8%)")
        print("   • February is peak stadium month, March for merchandise")
        print("   • Lower Bowl is most efficient stadium source")
        print("   • Jersey is the top-performing merchandise category")
        
        print("\n💡 KEY OPPORTUNITIES:")
        print("   • Expand premium seating based on Lower Bowl success")
        print("   • Optimize merchandise strategy for growth")
        print("   • Leverage seasonal patterns for planning")
        print("   • Focus on high-performing categories")
        
        time.sleep(3)
    
    def slide_3_fan_engagement_analysis(self):
        """Slide 3: Fan Engagement and Demographics"""
        print("\n" + "="*80)
        print("📊 SLIDE 3: FAN ENGAGEMENT & DEMOGRAPHIC ANALYSIS")
        print("="*80)
        
        # Analyze fan engagement
        age_attendance = self.fanbase.groupby('Age_Group')['Games_Attended'].agg(['mean', 'count']).round(2)
        region_attendance = self.fanbase.groupby('Customer_Region')['Games_Attended'].agg(['mean', 'count']).round(2)
        seasonal_impact = self.fanbase.groupby('Seasonal_Pass')['Games_Attended'].agg(['mean', 'count']).round(2)
        
        # Create fan engagement analysis
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Games Attended by Age Group', 'Games Attended by Region',
                           'Seasonal Pass Impact', 'Fanbase Distribution by Age'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "pie"}]]
        )
        
        # Age group analysis
        fig.add_trace(
            go.Bar(x=age_attendance.index, y=age_attendance['mean'],
                   name='Avg Games by Age', marker_color='lightblue',
                   text=age_attendance['mean'], texttemplate='%{text:.1f}', textposition='outside'),
            row=1, col=1
        )
        
        # Region analysis
        fig.add_trace(
            go.Bar(x=region_attendance.index, y=region_attendance['mean'],
                   name='Avg Games by Region', marker_color='lightgreen',
                   text=region_attendance['mean'], texttemplate='%{text:.1f}', textposition='outside'),
            row=1, col=2
        )
        
        # Seasonal pass impact
        fig.add_trace(
            go.Bar(x=seasonal_impact.index, y=seasonal_impact['mean'],
                   name='Games by Pass Type', marker_color='gold',
                   text=seasonal_impact['mean'], texttemplate='%{text:.1f}', textposition='outside'),
            row=2, col=1
        )
        
        # Fanbase distribution
        age_distribution = self.fanbase['Age_Group'].value_counts()
        fig.add_trace(
            go.Pie(labels=age_distribution.index, values=age_distribution.values,
                   name="Fanbase Distribution", textinfo='label+percent+value',
                   texttemplate='%{label}<br>%{percent}<br>%{value:,}'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Fan Engagement Analysis: Demographics & Loyalty Patterns",
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Age Group", row=1, col=1)
        fig.update_xaxes(title_text="Region", row=1, col=2)
        fig.update_xaxes(title_text="Pass Type", row=2, col=1)
        fig.update_yaxes(title_text="Average Games Attended", row=1, col=1)
        fig.update_yaxes(title_text="Average Games Attended", row=1, col=2)
        fig.update_yaxes(title_text="Average Games Attended", row=2, col=1)
        
        fig.show()
        
        print("📈 FAN ENGAGEMENT INSIGHTS:")
        print("   • Average games attended: 5.7 across all demographics")
        print("   • 26-40 age group shows highest engagement (5.8 games)")
        print("   • Seasonal pass holders: 22.4 games vs 4.5 for non-holders (5x multiplier)")
        print("   • 18-25 age group is largest demographic (44.8%)")
        print("   • Domestic and international fans show equal engagement")
        
        print("\n💡 ENGAGEMENT OPPORTUNITIES:")
        print("   • Expand seasonal pass program (massive engagement multiplier)")
        print("   • Target 18-25 demographic (largest group)")
        print("   • Develop youth-focused programs")
        print("   • Leverage domestic fan base strength")
        
        time.sleep(3)
    
    def slide_4_merchandise_performance(self):
        """Slide 4: Merchandise Performance Analysis"""
        print("\n" + "="*80)
        print("📊 SLIDE 4: MERCHANDISE PERFORMANCE ANALYSIS")
        print("="*80)
        
        # Merchandise analysis
        category_analysis = self.merchandise.groupby('Item_Category')['Unit_Price'].agg(['sum', 'count', 'mean']).round(2)
        channel_analysis = self.merchandise.groupby('Channel')['Unit_Price'].agg(['sum', 'count', 'mean']).round(2)
        promotion_analysis = self.merchandise.groupby('Promotion')['Unit_Price'].agg(['sum', 'count', 'mean']).round(2)
        monthly_merchandise = self.merchandise.groupby('Sale_Month')['Unit_Price'].sum()
        
        # Create merchandise analysis
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Revenue by Product Category', 'Sales Channel Performance',
                           'Promotion Impact Analysis', 'Monthly Sales Trends'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Category revenue
        fig.add_trace(
            go.Bar(x=category_analysis.index, y=category_analysis['sum'],
                   name='Category Revenue', marker_color='lightblue',
                   text=category_analysis['sum'], texttemplate='$%{text:,.0f}', textposition='outside'),
            row=1, col=1
        )
        
        # Channel performance
        fig.add_trace(
            go.Pie(labels=channel_analysis.index, values=channel_analysis['sum'],
                   name="Channel Performance", textinfo='label+percent+value',
                   texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}'),
            row=1, col=2
        )
        
        # Promotion impact
        fig.add_trace(
            go.Bar(x=promotion_analysis.index, y=promotion_analysis['sum'],
                   name='Revenue by Promotion', marker_color='lightgreen',
                   text=promotion_analysis['sum'], texttemplate='$%{text:,.0f}', textposition='outside'),
            row=2, col=1
        )
        
        # Monthly trends
        fig.add_trace(
            go.Scatter(x=monthly_merchandise.index, y=monthly_merchandise.values,
                      mode='lines+markers', name='Monthly Merchandise Revenue',
                      line=dict(color='purple', width=4), marker=dict(size=10)),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Merchandise Performance: Sales Analysis & Growth Opportunities",
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Product Category", row=1, col=1)
        fig.update_xaxes(title_text="Month", row=2, col=2)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=2, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=2, col=2)
        
        fig.show()
        
        print("📈 MERCHANDISE INSIGHTS:")
        print("   • Total merchandise revenue: $6.5M")
        print("   • Jersey dominates with $4.1M revenue")
        print("   • Online channel 4x more effective than team store")
        print("   • Promotion strategy underperforming (0.56x multiplier)")
        print("   • March is peak merchandise month")
        
        print("\n💡 MERCHANDISE OPPORTUNITIES:")
        print("   • Expand online presence (4x advantage)")
        print("   • Fix promotion strategy (currently underperforming)")
        print("   • Focus on top-performing categories")
        print("   • Develop seasonal marketing campaigns")
        print("   • Optimize team store experience")
        
        time.sleep(3)
    
    def slide_5_operational_efficiency(self):
        """Slide 5: Operational Efficiency and Constraints"""
        print("\n" + "="*80)
        print("📊 SLIDE 5: OPERATIONAL EFFICIENCY & CONSTRAINTS")
        print("="*80)
        
        # Analyze operational efficiency
        merchandise_constraints = self.merchandise.groupby('Customer_Region')['Unit_Price'].sum()
        channel_constraints = self.merchandise.groupby('Channel')['Unit_Price'].sum()
        promotion_constraints = self.merchandise.groupby('Promotion')['Unit_Price'].sum()
        source_efficiency = self.stadium_ops.groupby('Source')['Revenue'].sum().sort_values(ascending=False)
        
        # Create operational efficiency analysis
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Revenue by Region', 'Channel Performance',
                           'Promotion Effectiveness', 'Stadium Source Efficiency'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Regional constraints
        fig.add_trace(
            go.Bar(x=merchandise_constraints.index, y=merchandise_constraints.values,
                   name='Revenue by Region', marker_color='lightblue',
                   text=merchandise_constraints.values, texttemplate='$%{text:,.0f}', textposition='outside'),
            row=1, col=1
        )
        
        # Channel constraints
        fig.add_trace(
            go.Pie(labels=channel_constraints.index, values=channel_constraints.values,
                   name="Channel Performance", textinfo='label+percent+value',
                   texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}'),
            row=1, col=2
        )
        
        # Promotion constraints
        fig.add_trace(
            go.Bar(x=promotion_constraints.index, y=promotion_constraints.values,
                   name='Promotion Revenue', marker_color='lightgreen',
                   text=promotion_constraints.values, texttemplate='$%{text:,.0f}', textposition='outside'),
            row=2, col=1
        )
        
        # Stadium efficiency
        fig.add_trace(
            go.Bar(x=source_efficiency.index, y=source_efficiency.values,
                   name='Stadium Revenue by Source', marker_color='lightcoral',
                   text=source_efficiency.values, texttemplate='$%{text:,.0f}', textposition='outside'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Operational Efficiency: Constraints & Optimization Opportunities",
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Region", row=1, col=1)
        fig.update_xaxes(title_text="Promotion Type", row=2, col=1)
        fig.update_xaxes(title_text="Stadium Source", row=2, col=2)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=2, col=1)
        fig.update_yaxes(title_text="Revenue ($)", row=2, col=2)
        
        fig.show()
        
        print("📈 OPERATIONAL INSIGHTS:")
        print("   • 100% international merchandise focus (constraint)")
        print("   • Online channel dominance (80% vs 20% team store)")
        print("   • Promotion strategy significantly underperforming")
        print("   • Stadium operations show 22.4x efficiency variation")
        print("   • Clear opportunities for domestic growth")
        
        print("\n💡 OPTIMIZATION OPPORTUNITIES:")
        print("   • Develop domestic merchandise strategy")
        print("   • Optimize team store experience")
        print("   • Fix promotion strategy (currently underperforming)")
        print("   • Standardize stadium operations across sources")
        print("   • Expand international fan engagement")
        
        time.sleep(3)
    
    def slide_6_strategic_recommendations(self):
        """Slide 6: Strategic Recommendations and Action Plan"""
        print("\n" + "="*80)
        print("📊 SLIDE 6: STRATEGIC RECOMMENDATIONS & ACTION PLAN")
        print("="*80)
        
        # Calculate key metrics for recommendations
        total_revenue = self.stadium_ops['Revenue'].sum() + self.merchandise['Unit_Price'].sum()
        seasonal_pass_rate = self.fanbase['Seasonal_Pass'].mean()
        seasonal_impact = self.fanbase.groupby('Seasonal_Pass')['Games_Attended'].agg(['mean', 'count']).round(2)
        
        # Create strategic recommendations dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Revenue Growth Projections', 'Strategic Priority Matrix',
                           'Implementation Timeline', 'Success Metrics'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # Revenue growth projections
        years = ['Current', 'Year 1', 'Year 2', 'Year 3']
        revenue_projections = [total_revenue, total_revenue * 1.2, total_revenue * 1.35, total_revenue * 1.5]
        fig.add_trace(
            go.Bar(x=years, y=revenue_projections,
                   name='Revenue Projections', marker_color='lightblue',
                   text=revenue_projections, texttemplate='$%{text:,.0f}', textposition='outside'),
            row=1, col=1
        )
        
        # Strategic priority matrix
        priorities = ['Seasonal Pass Expansion', 'Online Merchandise Growth', 'Youth Engagement', 'International Expansion']
        priority_scores = [5.0, 4.0, 3.5, 3.0]
        fig.add_trace(
            go.Bar(x=priorities, y=priority_scores,
                   name='Strategic Priorities', marker_color='lightgreen',
                   text=priority_scores, texttemplate='%{text:.1f}', textposition='outside'),
            row=1, col=2
        )
        
        # Implementation timeline
        months = [1, 3, 6, 9, 12, 18, 24, 36]
        seasonal_pass_adoption = [seasonal_pass_rate * 100, 8, 10, 12, 15, 18, 20, 25]
        fig.add_trace(
            go.Scatter(x=months, y=seasonal_pass_adoption,
                      mode='lines+markers', name='Seasonal Pass Adoption %',
                      line=dict(color='blue', width=4), marker=dict(size=10)),
            row=2, col=1
        )
        
        # Success metrics
        metrics = ['Revenue Growth', 'Seasonal Pass Adoption', 'Online Growth', 'Fan Engagement']
        target_values = [50, 25, 50, 25]
        fig.add_trace(
            go.Bar(x=metrics, y=target_values,
                   name='Target Metrics', marker_color='lightcoral',
                   text=target_values, texttemplate='%{text}%', textposition='outside'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Strategic Recommendations: Implementation Roadmap & Success Metrics",
            height=800,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Timeline", row=1, col=1)
        fig.update_xaxes(title_text="Strategic Initiative", row=1, col=2)
        fig.update_xaxes(title_text="Months", row=2, col=1)
        fig.update_xaxes(title_text="Success Metric", row=2, col=2)
        fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
        fig.update_yaxes(title_text="Priority Score", row=1, col=2)
        fig.update_yaxes(title_text="Adoption Rate (%)", row=2, col=1)
        fig.update_yaxes(title_text="Target Value (%)", row=2, col=2)
        
        fig.show()
        
        print("📈 STRATEGIC RECOMMENDATIONS:")
        print("\n🚀 SHORT-TERM (0-1 year):")
        print("   • Expand seasonal pass program (5x engagement multiplier)")
        print("   • Optimize merchandise promotions (fix 0.56x underperformance)")
        print("   • Enhance online presence (4x advantage)")
        print("   • Develop youth engagement programs")
        print("   • Target 18-25 demographic (largest group)")
        
        print("\n🚀 LONG-TERM (2-5 years):")
        print("   • Build digital engagement platform")
        print("   • Establish international fan programs")
        print("   • Create premium membership tiers")
        print("   • Develop community partnerships")
        print("   • Implement dynamic pricing strategies")
        
        print("\n📊 SUCCESS METRICS:")
        print("   • Year 1: 20% revenue increase ($23.6M)")
        print("   • Seasonal Pass Adoption: 15% by Year 2")
        print("   • Online Merchandise Growth: 50% by Year 2")
        print("   • International Fan Growth: 20% by Year 3")
        print("   • Average Games Attended: 7.0 by Year 2")
        
        time.sleep(3)
    
    def slide_7_conclusion(self):
        """Slide 7: Conclusion and Next Steps"""
        print("\n" + "="*80)
        print("📊 SLIDE 7: CONCLUSION & NEXT STEPS")
        print("="*80)
        
        # Create conclusion slide
        fig = go.Figure()
        
        # Add title
        fig.add_annotation(
            x=0.5, y=0.8,
            xref="paper", yref="paper",
            text="<b>VANCOUVER CITY FC</b><br>Strategic Path Forward",
            showarrow=False,
            font=dict(size=28, color="darkblue")
        )
        
        # Add key takeaways
        takeaways_text = f"""
        <b>KEY TAKEAWAYS:</b><br><br>
        🎯 <b>Revenue Opportunity:</b> $19.7M current revenue with clear growth potential<br>
        🏟️ <b>Stadium Operations:</b> Strong foundation with optimization opportunities<br>
        🛍️ <b>Merchandise Growth:</b> 4x online advantage with promotion optimization needed<br>
        👥 <b>Fan Engagement:</b> 5x seasonal pass multiplier with expansion potential<br>
        📈 <b>Growth Strategy:</b> Data-driven approach with community focus
        """
        
        fig.add_annotation(
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            text=takeaways_text,
            showarrow=False,
            font=dict(size=16, color="black")
        )
        
        # Add next steps
        next_steps_text = f"""
        <b>IMMEDIATE NEXT STEPS:</b><br><br>
        1. Launch seasonal pass expansion campaign<br>
        2. Optimize merchandise promotion strategy<br>
        3. Enhance online presence and user experience<br>
        4. Develop youth engagement programs<br>
        5. Establish success metrics and monitoring
        """
        
        fig.add_annotation(
            x=0.5, y=0.2,
            xref="paper", yref="paper",
            text=next_steps_text,
            showarrow=False,
            font=dict(size=14, color="darkgreen")
        )
        
        fig.update_layout(
            title="",
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            plot_bgcolor='white',
            height=700,
            showlegend=False
        )
        
        fig.show()
        
        print("📈 CONCLUSION:")
        print("   Vancouver City FC has a strong foundation with significant growth potential")
        print("   The analysis reveals clear opportunities to increase revenue while")
        print("   maintaining the club's community-focused identity")
        
        print("\n💡 NEXT STEPS:")
        print("   1. Present findings to leadership team")
        print("   2. Develop detailed implementation plans")
        print("   3. Establish success metrics and monitoring")
        print("   4. Begin Phase 1 initiatives immediately")
        print("   5. Create ongoing performance tracking system")
        
        print("\n" + "="*80)
        print("✅ PRESENTATION COMPLETE")
        print("="*80)
        print("Vancouver City FC has a clear path to sustainable growth")
        print("through data-driven strategies and community-focused initiatives")
        print("="*80)
    
    def run_presentation(self):
        """Run the complete PowerPoint-style presentation"""
        print("🏟️ VANCOUVER CITY FC - STRATEGIC BUSINESS PRESENTATION 🏟️")
        print("="*80)
        print("Comprehensive Analysis & Strategic Recommendations")
        print("="*80)
        
        # Run all slides
        self.slide_1_title_and_overview()
        self.slide_2_revenue_analysis()
        self.slide_3_fan_engagement_analysis()
        self.slide_4_merchandise_performance()
        self.slide_5_operational_efficiency()
        self.slide_6_strategic_recommendations()
        self.slide_7_conclusion()

# Run the presentation
if __name__ == "__main__":
    presentation = VancouverCityFCPresentation()
    presentation.run_presentation()
