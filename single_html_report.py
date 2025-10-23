#!/usr/bin/env python3
"""
Vancouver City FC - Single HTML Report
Everything in one scrollable webpage
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import warnings
warnings.filterwarnings('ignore')

def create_single_html_report():
    """Create a single HTML file with everything embedded"""
    
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
    total_members = len(fanbase)
    avg_games = fanbase['Games_Attended'].mean()
    seasonal_pass_rate = fanbase['Seasonal_Pass'].mean()
    
    # Create visualizations
    print("Creating visualizations...")
    
    # Revenue composition chart
    revenue_data = {
        'Stadium Operations': stadium_revenue,
        'Merchandise Sales': merchandise_revenue
    }
    
    fig1 = go.Figure(data=[go.Pie(labels=list(revenue_data.keys()), values=list(revenue_data.values()),
                                 textinfo='label+percent+value', texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}',
                                 marker=dict(colors=['#ff7f0e', '#2ca02c']))])
    fig1.update_layout(title="Revenue Composition", height=400)
    
    # Fan engagement charts
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
    
    fig2.update_layout(title="Fan Engagement Analysis", height=400)
    
    # Merchandise analysis
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
    
    fig3.update_layout(title="Merchandise Performance Analysis", height=400)
    
    # Convert figures to HTML strings
    fig1_html = fig1.to_html(full_html=False, include_plotlyjs=False)
    fig2_html = fig2.to_html(full_html=False, include_plotlyjs=False)
    fig3_html = fig3.to_html(full_html=False, include_plotlyjs=False)
    
    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vancouver City FC - Strategic Business Analysis</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #2c3e50;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #2c3e50;
                margin: 0;
                font-size: 2.5em;
            }}
            .header h2 {{
                color: #7f8c8d;
                margin: 10px 0 0 0;
                font-size: 1.2em;
            }}
            .section {{
                margin: 40px 0;
                padding: 20px;
                border-left: 4px solid #3498db;
                background-color: #f8f9fa;
            }}
            .section h2 {{
                color: #2c3e50;
                margin-top: 0;
                font-size: 1.8em;
            }}
            .section h3 {{
                color: #34495e;
                margin-top: 25px;
                font-size: 1.3em;
            }}
            .highlight {{
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .metric {{
                background-color: #e8f4f8;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                border: 2px solid #3498db;
            }}
            .metric-value {{
                font-size: 2em;
                font-weight: bold;
                color: #2c3e50;
            }}
            .metric-label {{
                color: #7f8c8d;
                font-size: 0.9em;
                margin-top: 5px;
            }}
            .recommendation {{
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .constraint {{
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .chart-container {{
                margin: 20px 0;
                text-align: center;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin: 8px 0;
            }}
            .phase {{
                background-color: #e3f2fd;
                border: 1px solid #bbdefb;
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
            }}
            .phase h4 {{
                color: #1976d2;
                margin-top: 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>VANCOUVER CITY FC</h1>
                <h2>Strategic Business Analysis</h2>
                <p>BOLT UBC First Byte 2025 - Case Competition</p>
            </div>
            
            <div class="section">
                <h2>EXECUTIVE SUMMARY</h2>
                <p>Vancouver City FC is a mid-market football club in the BOLT Soccer League with strong 
                foundational performance but significant untapped growth potential.</p>
                
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">${total_revenue:,.0f}</div>
                        <div class="metric-label">Total Revenue</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{total_members:,}</div>
                        <div class="metric-label">Total Members</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{avg_games:.1f}</div>
                        <div class="metric-label">Avg Games Attended</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{seasonal_pass_rate:.1%}</div>
                        <div class="metric-label">Seasonal Pass Rate</div>
                    </div>
                </div>
                
                <div class="highlight">
                    <h3>KEY OPPORTUNITY</h3>
                    <p>The club's greatest opportunity lies in seasonal pass expansion. Current seasonal pass 
                    holders attend 22.4 games compared to 4.5 for non-holders - a <strong>5x engagement multiplier</strong>. 
                    With only 6.8% adoption, this represents massive expansion potential.</p>
                </div>
                
                <div class="recommendation">
                    <h3>STRATEGIC RECOMMENDATION</h3>
                    <p>Focus on three high-impact initiatives:</p>
                    <ul>
                        <li>Expand seasonal pass program (target 15% adoption)</li>
                        <li>Optimize merchandise promotion strategy (fix 0.56x multiplier)</li>
                        <li>Enhance online presence (leverage 4x advantage)</li>
                    </ul>
                </div>
            </div>
            
            <div class="section">
                <h2>SECTION 1: REVENUE ANALYSIS</h2>
                
                <div class="chart-container">
                    {fig1_html}
                </div>
                
                <h3>REVENUE COMPOSITION</h3>
                <p>Vancouver City FC follows a traditional sports club revenue model with stadium operations 
                dominating at 67.2% of total revenue. This reflects strong matchday experience and loyal 
                fan base. The 32.8% merchandise revenue represents significant growth opportunity.</p>
                
                <h3>SEASONAL PATTERNS</h3>
                <ul>
                    <li>February: Peak stadium month ($3.96M)</li>
                    <li>March: Peak merchandise month ($1.09M)</li>
                    <li>Clear seasonal cycles enable targeted marketing and operational planning</li>
                </ul>
                
                <h3>STADIUM EFFICIENCY</h3>
                <p>Lower Bowl emerges as most efficient revenue source, suggesting successful model for 
                premium seating expansion. This supports strategic investment in premium options.</p>
                
                <h3>MERCHANDISE PERFORMANCE</h3>
                <ul>
                    <li>Jersey category dominates with $4.1M revenue</li>
                    <li>Commands premium pricing at $152 average</li>
                    <li>Indicates strong brand value and pricing power</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>SECTION 2: FAN ENGAGEMENT ANALYSIS</h2>
                
                <div class="chart-container">
                    {fig2_html}
                </div>
                
                <h3>DEMOGRAPHIC OVERVIEW</h3>
                <p>Fan engagement shows consistent patterns across demographics with 5.7 games average 
                attendance per member. This consistency suggests strong brand loyalty and community 
                connection.</p>
                
                <h3>AGE GROUP BREAKDOWN</h3>
                <ul>
                    <li>26-40: Highest engagement (5.8 games)</li>
                    <li>18-25: Largest segment (44.8% of fanbase) - key target market</li>
                    <li>Consistent engagement across all age groups</li>
                </ul>
                
                <div class="highlight">
                    <h3>SEASONAL PASS IMPACT - THE GAME CHANGER</h3>
                    <p>This is the most significant finding:</p>
                    <ul>
                        <li>Seasonal pass holders: 22.4 games</li>
                        <li>Non-holders: 4.5 games</li>
                        <li><strong>5x engagement multiplier</strong></li>
                        <li>Only 6.8% current adoption</li>
                        <li>Massive expansion potential</li>
                    </ul>
                </div>
                
                <h3>GEOGRAPHIC ENGAGEMENT</h3>
                <p>Domestic and international fans show equal engagement levels, indicating ability to 
                maintain community focus while building international appeal.</p>
            </div>
            
            <div class="section">
                <h2>SECTION 3: MERCHANDISE PERFORMANCE</h2>
                
                <div class="chart-container">
                    {fig3_html}
                </div>
                
                <h3>REVENUE OVERVIEW</h3>
                <p>Merchandise sales total $6.5M with strong growth potential, representing 32.8% of 
                total revenue.</p>
                
                <h3>CHANNEL PERFORMANCE</h3>
                <ul>
                    <li>Online: 80% of sales (4x advantage over team store)</li>
                    <li>Team Store: 20% of sales</li>
                    <li>Critical importance of digital presence and e-commerce optimization</li>
                </ul>
                
                <div class="constraint">
                    <h3>PROMOTION STRATEGY CRISIS</h3>
                    <p>Current promotions show 0.56x multiplier - actually reducing revenue effectiveness.
                    This represents major optimization opportunity.</p>
                </div>
                
                <h3>PRODUCT CATEGORY BREAKDOWN</h3>
                <ul>
                    <li>Jersey: $4.1M revenue (dominates)</li>
                    <li>Premium pricing: $152 average</li>
                    <li>Strong brand value and pricing power</li>
                    <li>March: Peak merchandise month ($1.09M)</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>SECTION 4: OPERATIONAL CONSTRAINTS</h2>
                
                <div class="constraint">
                    <h3>1. INTERNATIONAL MERCHANDISE FOCUS</h3>
                    <ul>
                        <li>100% international focus limits domestic growth</li>
                        <li>Opportunity: Domestic market expansion</li>
                        <li>Benefit: Local community engagement</li>
                    </ul>
                </div>
                
                <div class="constraint">
                    <h3>2. CHANNEL IMBALANCE</h3>
                    <ul>
                        <li>80% online vs 20% team store</li>
                        <li>Risk: Limited community connection</li>
                        <li>Opportunity: Enhanced online experience</li>
                    </ul>
                </div>
                
                <div class="constraint">
                    <h3>3. STADIUM OPERATIONS VARIATION</h3>
                    <ul>
                        <li>22.4x efficiency variation across sources</li>
                        <li>Opportunity: Standardization using Lower Bowl model</li>
                        <li>Benefit: Improved operational efficiency</li>
                    </ul>
                </div>
                
                <div class="constraint">
                    <h3>4. PROMOTION STRATEGY INEFFICIENCY</h3>
                    <ul>
                        <li>0.56x multiplier (underperforming)</li>
                        <li>Major optimization opportunity</li>
                        <li>Potential for significant revenue improvement</li>
                    </ul>
                </div>
            </div>
            
            <div class="section">
                <h2>SECTION 5: STRATEGIC RECOMMENDATIONS</h2>
                
                <div class="phase">
                    <h4>IMMEDIATE ACTIONS (0-6 months)</h4>
                    
                    <h3>1. SEASONAL PASS EXPANSION</h3>
                    <p><strong>Priority:</strong> HIGHEST<br>
                    <strong>Target:</strong> 15% adoption (double current 6.8%)<br>
                    <strong>Actions:</strong></p>
                    <ul>
                        <li>Targeted marketing to 18-25 demographic</li>
                        <li>Flexible payment options</li>
                        <li>Exclusive member benefits</li>
                        <li>Student discounts and family packages</li>
                    </ul>
                    <p><strong>Impact:</strong> 5x engagement multiplier</p>
                    
                    <h3>2. PROMOTION STRATEGY OVERHAUL</h3>
                    <p><strong>Priority:</strong> HIGH<br>
                    <strong>Target:</strong> 1.5x multiplier (up from 0.56x)<br>
                    <strong>Actions:</strong></p>
                    <ul>
                        <li>Data-driven customer segmentation</li>
                        <li>Value-based offers</li>
                        <li>Seasonal timing optimization</li>
                        <li>A/B testing implementation</li>
                    </ul>
                    <p><strong>Impact:</strong> Significant revenue improvement</p>
                    
                    <h3>3. ONLINE PRESENCE ENHANCEMENT</h3>
                    <p><strong>Priority:</strong> HIGH<br>
                    <strong>Target:</strong> Leverage 4x advantage<br>
                    <strong>Actions:</strong></p>
                    <ul>
                        <li>Improved user experience</li>
                        <li>Mobile optimization</li>
                        <li>Personalized recommendations</li>
                        <li>Virtual try-on features</li>
                    </ul>
                    <p><strong>Impact:</strong> Increased online sales</p>
                </div>
                
                <div class="phase">
                    <h4>MEDIUM-TERM INITIATIVES (6-18 months)</h4>
                    
                    <h3>4. YOUTH ENGAGEMENT PROGRAMS</h3>
                    <p><strong>Target:</strong> 18-25 demographic (44.8% of fanbase)<br>
                    <strong>Actions:</strong></p>
                    <ul>
                        <li>Social media campaigns</li>
                        <li>University partnerships</li>
                        <li>Youth-focused events</li>
                        <li>Community outreach</li>
                    </ul>
                    
                    <h3>5. PREMIUM MERCHANDISE EXPANSION</h3>
                    <p><strong>Focus:</strong> High-performing categories<br>
                    <strong>Actions:</strong></p>
                    <ul>
                        <li>Jersey sales prioritization</li>
                        <li>Limited editions</li>
                        <li>Player collaborations</li>
                        <li>Premium positioning</li>
                    </ul>
                </div>
                
                <div class="phase">
                    <h4>LONG-TERM VISION (18-36 months)</h4>
                    
                    <h3>6. DIGITAL ENGAGEMENT PLATFORM</h3>
                    <ul>
                        <li>Mobile app with social features</li>
                        <li>Personalized content</li>
                        <li>Virtual fan experiences</li>
                        <li>Community features</li>
                    </ul>
                    
                    <h3>7. INTERNATIONAL FAN PROGRAMS</h3>
                    <ul>
                        <li>Localized content</li>
                        <li>Regional merchandise</li>
                        <li>Global community building</li>
                        <li>International partnerships</li>
                    </ul>
                    
                    <h3>8. PREMIUM MEMBERSHIP TIERS</h3>
                    <ul>
                        <li>Escalating benefits</li>
                        <li>VIP experiences</li>
                        <li>Exclusive access</li>
                        <li>Priority privileges</li>
                    </ul>
                </div>
            </div>
            
            <div class="section">
                <h2>SECTION 6: SUCCESS METRICS</h2>
                
                <h3>REVENUE TARGETS</h3>
                <ul>
                    <li>Year 1: 20% increase ($23.6M total)</li>
                    <li>Year 2: 35% increase ($26.6M total)</li>
                    <li>Year 3: 50% increase ($29.5M total)</li>
                </ul>
                
                <h3>FAN ENGAGEMENT TARGETS</h3>
                <ul>
                    <li>Seasonal Pass Adoption: 15% by Year 2</li>
                    <li>Average Games Attended: 7.0 by Year 2</li>
                    <li>Online Merchandise Growth: 50% by Year 2</li>
                    <li>International Fan Growth: 20% by Year 3</li>
                </ul>
                
                <h3>OPERATIONAL EFFICIENCY TARGETS</h3>
                <ul>
                    <li>Promotion Effectiveness: 1.5x multiplier by Year 1</li>
                    <li>Domestic Merchandise: 30% of total by Year 2</li>
                    <li>Stadium Operations: 15% efficiency improvement by Year 2</li>
                    <li>Digital Engagement: 80% of members active by Year 2</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>SECTION 7: IMPLEMENTATION ROADMAP</h2>
                
                <div class="phase">
                    <h4>PHASE 1: FOUNDATION BUILDING (Months 1-6)</h4>
                    <ul>
                        <li>Launch seasonal pass expansion campaign</li>
                        <li>Implement promotion strategy optimization</li>
                        <li>Enhance online user experience</li>
                        <li>Develop youth engagement programs</li>
                        <li>Establish success metrics</li>
                    </ul>
                </div>
                
                <div class="phase">
                    <h4>PHASE 2: GROWTH ACCELERATION (Months 7-18)</h4>
                    <ul>
                        <li>Scale successful Phase 1 initiatives</li>
                        <li>Launch digital platform</li>
                        <li>Implement premium membership tiers</li>
                        <li>Expand international programs</li>
                        <li>Optimize operational efficiency</li>
                    </ul>
                </div>
                
                <div class="phase">
                    <h4>PHASE 3: STRATEGIC EXPANSION (Months 19-36)</h4>
                    <ul>
                        <li>Full digital ecosystem</li>
                        <li>International market expansion</li>
                        <li>Community partnerships</li>
                        <li>Advanced analytics</li>
                        <li>Sustainability initiatives</li>
                    </ul>
                </div>
            </div>
            
            <div class="section">
                <h2>SECTION 8: COMPETITIVE ADVANTAGES</h2>
                
                <h3>1. COMMUNITY FOCUS</h3>
                <ul>
                    <li>Strong domestic fan base</li>
                    <li>Local identity and connection</li>
                    <li>Emotional bonds drive loyalty</li>
                    <li>Difficult for larger clubs to replicate</li>
                </ul>
                
                <h3>2. DATA-DRIVEN APPROACH</h3>
                <ul>
                    <li>Comprehensive analysis</li>
                    <li>Clear growth roadmap</li>
                    <li>Analytical advantage</li>
                    <li>Effective decision-making</li>
                </ul>
                
                <h3>3. FLEXIBILITY & AGILITY</h3>
                <ul>
                    <li>Mid-market club advantages</li>
                    <li>Responsive to fan needs</li>
                    <li>Rapid adaptation capability</li>
                    <li>Less bureaucratic structure</li>
                </ul>
                
                <h3>4. AUTHENTIC LOCAL IDENTITY</h3>
                <ul>
                    <li>Genuine community connection</li>
                    <li>Emotional engagement</li>
                    <li>Sustainable competitive advantage</li>
                    <li>Unique market position</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>SECTION 9: RISK ASSESSMENT</h2>
                
                <h3>RISK 1: MARKET COMPETITION</h3>
                <p><strong>Threat:</strong> Larger clubs with more resources<br>
                <strong>Mitigation:</strong> Focus on community connection and unique experiences</p>
                
                <h3>RISK 2: ECONOMIC DOWNTURN</h3>
                <p><strong>Threat:</strong> Reduced discretionary spending<br>
                <strong>Mitigation:</strong> Flexible pricing and payment options</p>
                
                <h3>RISK 3: TECHNOLOGY DISRUPTION</h3>
                <p><strong>Threat:</strong> Changing fan expectations<br>
                <strong>Mitigation:</strong> Continuous innovation and digital investment</p>
                
                <h3>RISK 4: FAN SATISFACTION</h3>
                <p><strong>Threat:</strong> Alienating existing fans<br>
                <strong>Mitigation:</strong> Gradual implementation and fan feedback integration</p>
            </div>
            
            <div class="section">
                <h2>CONCLUSION</h2>
                
                <p>Vancouver City FC has a clear path to sustainable growth through strategic initiatives 
                that leverage existing strengths while addressing key opportunities.</p>
                
                <div class="highlight">
                    <h3>KEY TAKEAWAYS</h3>
                    <ul>
                        <li>5x engagement multiplier from seasonal pass holders represents massive opportunity</li>
                        <li>Only 6.8% current adoption leaves significant expansion potential</li>
                        <li>4x online advantage provides strong foundation for digital growth</li>
                        <li>Community focus creates sustainable competitive advantage</li>
                    </ul>
                </div>
                
                <div class="recommendation">
                    <h3>STRATEGIC FOCUS</h3>
                    <p>The combination of seasonal pass expansion, merchandise optimization, and digital 
                    enhancement provides a comprehensive framework for achieving 20%+ revenue growth 
                    while maintaining the club's community-focused identity.</p>
                </div>
                
                <h3>NEXT STEPS</h3>
                <ol>
                    <li>Present findings to leadership team</li>
                    <li>Develop detailed implementation plans</li>
                    <li>Establish success metrics and monitoring</li>
                    <li>Begin Phase 1 initiatives immediately</li>
                    <li>Create ongoing performance tracking</li>
                </ol>
                
                <p>Vancouver City FC can position itself as a model for mid-market sports clubs, 
                demonstrating how data-driven decision-making and community focus can drive 
                sustainable growth in the competitive sports entertainment market.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save HTML file
    with open('vancouver_city_fc_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ HTML report created: vancouver_city_fc_report.html")
    print("✓ Open the file in your browser to view the complete report")
    print("✓ All visualizations are embedded and interactive")
    print("✓ Single scrollable document with professional formatting")

if __name__ == "__main__":
    create_single_html_report()
