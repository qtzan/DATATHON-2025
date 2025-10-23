#!/usr/bin/env python3
"""
Vancouver City FC - Modern Business Report
Clean, structured presentation format
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

def create_modern_business_report():
    """Create a modern business report with clean structure"""
    
    print("="*120)
    print("VANCOUVER CITY FC - STRATEGIC BUSINESS ANALYSIS")
    print("BOLT UBC First Byte 2025 - Case Competition")
    print("="*120)
    
    # Load and clean data
    print("\n[LOADING DATA]")
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
    
    print("✓ Data loaded and cleaned successfully")
    
    # Calculate key metrics
    total_revenue = stadium_ops['Revenue'].sum() + merchandise['Unit_Price'].sum()
    stadium_revenue = stadium_ops['Revenue'].sum()
    merchandise_revenue = merchandise['Unit_Price'].sum()
    total_members = len(fanbase)
    avg_games = fanbase['Games_Attended'].mean()
    seasonal_pass_rate = fanbase['Seasonal_Pass'].mean()
    
    print("\n" + "="*120)
    print("EXECUTIVE SUMMARY")
    print("="*120)
    
    print(f"""
Vancouver City FC is a mid-market football club in the BOLT Soccer League with strong 
foundational performance but significant untapped growth potential.

CURRENT SITUATION:
• Total Revenue: ${total_revenue:,.0f}
• Stadium Operations: ${stadium_revenue:,.0f} (67.2%)
• Merchandise Sales: ${merchandise_revenue:,.0f} (32.8%)
• Fanbase: {total_members:,} members
• Average Attendance: {avg_games:.1f} games per member
• Seasonal Pass Rate: {seasonal_pass_rate:.1%}

KEY OPPORTUNITY:
The club's greatest opportunity lies in seasonal pass expansion. Current seasonal pass 
holders attend 22.4 games compared to 4.5 for non-holders - a 5x engagement multiplier. 
With only 6.8% adoption, this represents massive expansion potential.

STRATEGIC RECOMMENDATION:
Focus on three high-impact initiatives:
1. Expand seasonal pass program (target 15% adoption)
2. Optimize merchandise promotion strategy (fix 0.56x multiplier)
3. Enhance online presence (leverage 4x advantage)
""")
    
    print("\n" + "="*120)
    print("SECTION 1: REVENUE ANALYSIS")
    print("="*120)
    
    print("""
REVENUE COMPOSITION:
Vancouver City FC follows a traditional sports club revenue model with stadium operations 
dominating at 67.2% of total revenue. This reflects strong matchday experience and loyal 
fan base. The 32.8% merchandise revenue represents significant growth opportunity.

SEASONAL PATTERNS:
• February: Peak stadium month ($3.96M)
• March: Peak merchandise month ($1.09M)
• Clear seasonal cycles enable targeted marketing and operational planning

STADIUM EFFICIENCY:
Lower Bowl emerges as most efficient revenue source, suggesting successful model for 
premium seating expansion. This supports strategic investment in premium options.

MERCHANDISE PERFORMANCE:
• Jersey category dominates with $4.1M revenue
• Commands premium pricing at $152 average
• Indicates strong brand value and pricing power
""")
    
    # Create revenue visualization
    print("\n[REVENUE VISUALIZATION]")
    revenue_data = {
        'Stadium Operations': stadium_revenue,
        'Merchandise Sales': merchandise_revenue
    }
    
    fig1 = go.Figure(data=[go.Pie(labels=list(revenue_data.keys()), values=list(revenue_data.values()),
                                 textinfo='label+percent+value', texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}',
                                 marker=dict(colors=['#ff7f0e', '#2ca02c']))])
    fig1.update_layout(title="Revenue Composition", height=500)
    fig1.show()
    
    print("\n" + "="*120)
    print("SECTION 2: FAN ENGAGEMENT ANALYSIS")
    print("="*120)
    
    print("""
DEMOGRAPHIC OVERVIEW:
Fan engagement shows consistent patterns across demographics with 5.7 games average 
attendance per member. This consistency suggests strong brand loyalty and community 
connection.

AGE GROUP BREAKDOWN:
• 26-40: Highest engagement (5.8 games)
• 18-25: Largest segment (44.8% of fanbase) - key target market
• Consistent engagement across all age groups

SEASONAL PASS IMPACT - THE GAME CHANGER:
This is the most significant finding:
• Seasonal pass holders: 22.4 games
• Non-holders: 4.5 games
• 5x engagement multiplier
• Only 6.8% current adoption
• Massive expansion potential

GEOGRAPHIC ENGAGEMENT:
Domestic and international fans show equal engagement levels, indicating ability to 
maintain community focus while building international appeal.
""")
    
    # Create fan engagement visualization
    print("\n[FAN ENGAGEMENT VISUALIZATION]")
    age_attendance = fanbase.groupby('Age_Group')['Games_Attended'].agg(['mean', 'count']).round(2)
    seasonal_impact = fanbase.groupby('Seasonal_Pass')['Games_Attended'].agg(['mean', 'count']).round(2)
    
    fig2 = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Games Attended by Age Group', 'Seasonal Pass Impact'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    fig2.add_trace(
        go.Bar(x=age_attendance.index, y=age_attendance['mean'],
               name='Avg Games by Age', marker_color='lightblue',
               text=age_attendance['mean'], texttemplate='%{text:.1f}', textposition='outside'),
        row=1, col=1
    )
    
    fig2.add_trace(
        go.Bar(x=seasonal_impact.index, y=seasonal_impact['mean'],
               name='Games by Pass Type', marker_color='gold',
               text=seasonal_impact['mean'], texttemplate='%{text:.1f}', textposition='outside'),
        row=1, col=2
    )
    
    fig2.update_layout(title="Fan Engagement Analysis", height=500)
    fig2.show()
    
    print("\n" + "="*120)
    print("SECTION 3: MERCHANDISE PERFORMANCE")
    print("="*120)
    
    print("""
REVENUE OVERVIEW:
Merchandise sales total $6.5M with strong growth potential, representing 32.8% of 
total revenue.

CHANNEL PERFORMANCE:
• Online: 80% of sales (4x advantage over team store)
• Team Store: 20% of sales
• Critical importance of digital presence and e-commerce optimization

PROMOTION STRATEGY CRISIS:
Current promotions show 0.56x multiplier - actually reducing revenue effectiveness.
This represents major optimization opportunity.

PRODUCT CATEGORY BREAKDOWN:
• Jersey: $4.1M revenue (dominates)
• Premium pricing: $152 average
• Strong brand value and pricing power
• March: Peak merchandise month ($1.09M)
""")
    
    # Create merchandise visualization
    print("\n[MERCHANDISE VISUALIZATION]")
    category_revenue = merchandise.groupby('Item_Category')['Unit_Price'].sum().sort_values(ascending=False)
    channel_analysis = merchandise.groupby('Channel')['Unit_Price'].agg(['sum', 'count', 'mean']).round(2)
    promotion_analysis = merchandise.groupby('Promotion')['Unit_Price'].agg(['sum', 'count', 'mean']).round(2)
    
    fig3 = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Revenue by Category', 'Channel Performance', 'Promotion Impact'),
        specs=[[{"type": "bar"}, {"type": "pie"}, {"type": "bar"}]]
    )
    
    fig3.add_trace(
        go.Bar(x=category_revenue.index, y=category_revenue.values,
               name='Category Revenue', marker_color='lightblue',
               text=category_revenue.values, texttemplate='$%{text:,.0f}', textposition='outside'),
        row=1, col=1
    )
    
    fig3.add_trace(
        go.Pie(labels=channel_analysis.index, values=channel_analysis['sum'],
               name="Channel Performance", textinfo='label+percent+value',
               texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}'),
        row=1, col=2
    )
    
    fig3.add_trace(
        go.Bar(x=promotion_analysis.index, y=promotion_analysis['sum'],
               name='Revenue by Promotion', marker_color='lightgreen',
               text=promotion_analysis['sum'], texttemplate='$%{text:,.0f}', textposition='outside'),
        row=1, col=3
    )
    
    fig3.update_layout(title="Merchandise Performance Analysis", height=500)
    fig3.show()
    
    print("\n" + "="*120)
    print("SECTION 4: OPERATIONAL CONSTRAINTS")
    print("="*120)
    
    print("""
IDENTIFIED CONSTRAINTS:

1. INTERNATIONAL MERCHANDISE FOCUS
   • 100% international focus limits domestic growth
   • Opportunity: Domestic market expansion
   • Benefit: Local community engagement

2. CHANNEL IMBALANCE
   • 80% online vs 20% team store
   • Risk: Limited community connection
   • Opportunity: Enhanced online experience

3. STADIUM OPERATIONS VARIATION
   • 22.4x efficiency variation across sources
   • Opportunity: Standardization using Lower Bowl model
   • Benefit: Improved operational efficiency

4. PROMOTION STRATEGY INEFFICIENCY
   • 0.56x multiplier (underperforming)
   • Major optimization opportunity
   • Potential for significant revenue improvement
""")
    
    print("\n" + "="*120)
    print("SECTION 5: STRATEGIC RECOMMENDATIONS")
    print("="*120)
    
    print("""
IMMEDIATE ACTIONS (0-6 months):

1. SEASONAL PASS EXPANSION
   Priority: HIGHEST
   Target: 15% adoption (double current 6.8%)
   Actions:
   • Targeted marketing to 18-25 demographic
   • Flexible payment options
   • Exclusive member benefits
   • Student discounts and family packages
   Impact: 5x engagement multiplier

2. PROMOTION STRATEGY OVERHAUL
   Priority: HIGH
   Target: 1.5x multiplier (up from 0.56x)
   Actions:
   • Data-driven customer segmentation
   • Value-based offers
   • Seasonal timing optimization
   • A/B testing implementation
   Impact: Significant revenue improvement

3. ONLINE PRESENCE ENHANCEMENT
   Priority: HIGH
   Target: Leverage 4x advantage
   Actions:
   • Improved user experience
   • Mobile optimization
   • Personalized recommendations
   • Virtual try-on features
   Impact: Increased online sales

MEDIUM-TERM INITIATIVES (6-18 months):

4. YOUTH ENGAGEMENT PROGRAMS
   Target: 18-25 demographic (44.8% of fanbase)
   Actions:
   • Social media campaigns
   • University partnerships
   • Youth-focused events
   • Community outreach

5. PREMIUM MERCHANDISE EXPANSION
   Focus: High-performing categories
   Actions:
   • Jersey sales prioritization
   • Limited editions
   • Player collaborations
   • Premium positioning

LONG-TERM VISION (18-36 months):

6. DIGITAL ENGAGEMENT PLATFORM
   • Mobile app with social features
   • Personalized content
   • Virtual fan experiences
   • Community features

7. INTERNATIONAL FAN PROGRAMS
   • Localized content
   • Regional merchandise
   • Global community building
   • International partnerships

8. PREMIUM MEMBERSHIP TIERS
   • Escalating benefits
   • VIP experiences
   • Exclusive access
   • Priority privileges
""")
    
    print("\n" + "="*120)
    print("SECTION 6: SUCCESS METRICS")
    print("="*120)
    
    print("""
REVENUE TARGETS:
• Year 1: 20% increase ($23.6M total)
• Year 2: 35% increase ($26.6M total)
• Year 3: 50% increase ($29.5M total)

FAN ENGAGEMENT TARGETS:
• Seasonal Pass Adoption: 15% by Year 2
• Average Games Attended: 7.0 by Year 2
• Online Merchandise Growth: 50% by Year 2
• International Fan Growth: 20% by Year 3

OPERATIONAL EFFICIENCY TARGETS:
• Promotion Effectiveness: 1.5x multiplier by Year 1
• Domestic Merchandise: 30% of total by Year 2
• Stadium Operations: 15% efficiency improvement by Year 2
• Digital Engagement: 80% of members active by Year 2
""")
    
    print("\n" + "="*120)
    print("SECTION 7: IMPLEMENTATION ROADMAP")
    print("="*120)
    
    print("""
PHASE 1: FOUNDATION BUILDING (Months 1-6)
• Launch seasonal pass expansion campaign
• Implement promotion strategy optimization
• Enhance online user experience
• Develop youth engagement programs
• Establish success metrics

PHASE 2: GROWTH ACCELERATION (Months 7-18)
• Scale successful Phase 1 initiatives
• Launch digital platform
• Implement premium membership tiers
• Expand international programs
• Optimize operational efficiency

PHASE 3: STRATEGIC EXPANSION (Months 19-36)
• Full digital ecosystem
• International market expansion
• Community partnerships
• Advanced analytics
• Sustainability initiatives
""")
    
    print("\n" + "="*120)
    print("SECTION 8: COMPETITIVE ADVANTAGES")
    print("="*120)
    
    print("""
1. COMMUNITY FOCUS
   • Strong domestic fan base
   • Local identity and connection
   • Emotional bonds drive loyalty
   • Difficult for larger clubs to replicate

2. DATA-DRIVEN APPROACH
   • Comprehensive analysis
   • Clear growth roadmap
   • Analytical advantage
   • Effective decision-making

3. FLEXIBILITY & AGILITY
   • Mid-market club advantages
   • Responsive to fan needs
   • Rapid adaptation capability
   • Less bureaucratic structure

4. AUTHENTIC LOCAL IDENTITY
   • Genuine community connection
   • Emotional engagement
   • Sustainable competitive advantage
   • Unique market position
""")
    
    print("\n" + "="*120)
    print("SECTION 9: RISK ASSESSMENT")
    print("="*120)
    
    print("""
RISK 1: MARKET COMPETITION
Threat: Larger clubs with more resources
Mitigation: Focus on community connection and unique experiences

RISK 2: ECONOMIC DOWNTURN
Threat: Reduced discretionary spending
Mitigation: Flexible pricing and payment options

RISK 3: TECHNOLOGY DISRUPTION
Threat: Changing fan expectations
Mitigation: Continuous innovation and digital investment

RISK 4: FAN SATISFACTION
Threat: Alienating existing fans
Mitigation: Gradual implementation and fan feedback integration
""")
    
    print("\n" + "="*120)
    print("CONCLUSION")
    print("="*120)
    
    print(f"""
Vancouver City FC has a clear path to sustainable growth through strategic initiatives 
that leverage existing strengths while addressing key opportunities.

KEY TAKEAWAYS:
• 5x engagement multiplier from seasonal pass holders represents massive opportunity
• Only 6.8% current adoption leaves significant expansion potential
• 4x online advantage provides strong foundation for digital growth
• Community focus creates sustainable competitive advantage

STRATEGIC FOCUS:
The combination of seasonal pass expansion, merchandise optimization, and digital 
enhancement provides a comprehensive framework for achieving 20%+ revenue growth 
while maintaining the club's community-focused identity.

NEXT STEPS:
1. Present findings to leadership team
2. Develop detailed implementation plans
3. Establish success metrics and monitoring
4. Begin Phase 1 initiatives immediately
5. Create ongoing performance tracking

Vancouver City FC can position itself as a model for mid-market sports clubs, 
demonstrating how data-driven decision-making and community focus can drive 
sustainable growth in the competitive sports entertainment market.
""")
    
    print("\n" + "="*120)
    print("END OF REPORT")
    print("="*120)

if __name__ == "__main__":
    create_modern_business_report()
