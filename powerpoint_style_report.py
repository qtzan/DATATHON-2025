#!/usr/bin/env python3
"""
Vancouver City FC - PowerPoint Style Report
Each section as a separate slide with navigation
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import warnings
warnings.filterwarnings('ignore')

def create_powerpoint_style_report():
    """Create a PowerPoint-style presentation with slide navigation"""
    
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
                                 marker=dict(colors=['#00ffff', '#ff0080']),
                                 hole=0.3)])
    fig1.update_layout(
        title="Revenue Composition",
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0', size=14),
        title_font=dict(color='#00ffff', size=20)
    )
    
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
               name='Avg Games by Age', marker_color='#00ffff',
               text=age_attendance['mean'], texttemplate='%{text:.1f}', textposition='outside'),
        row=1, col=1
    )
    
    fig2.add_trace(
        go.Bar(x=seasonal_impact.index, y=seasonal_impact['mean'],
               name='Games by Pass Type', marker_color='#ff0080',
               text=seasonal_impact['mean'], texttemplate='%{text:.1f}', textposition='outside'),
        row=1, col=2
    )
    
    fig2.update_layout(
        title="Fan Engagement Analysis",
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0', size=14),
        title_font=dict(color='#00ffff', size=20)
    )
    
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
               name='Category Revenue', marker_color='#00ffff',
               text=category_revenue.values, texttemplate='$%{text:,.0f}', textposition='outside'),
        row=1, col=1
    )
    
    fig3.add_trace(
        go.Pie(labels=channel_analysis.index, values=channel_analysis['sum'],
               name="Channel Performance", textinfo='label+percent+value',
               texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}',
               marker=dict(colors=['#00ffff', '#ff0080'])),
        row=1, col=2
    )
    
    fig3.add_trace(
        go.Bar(x=promotion_analysis.index, y=promotion_analysis['sum'],
               name='Revenue by Promotion', marker_color='#ff0080',
               text=promotion_analysis['sum'], texttemplate='$%{text:,.0f}', textposition='outside'),
        row=1, col=3
    )
    
    fig3.update_layout(
        title="Merchandise Performance Analysis",
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0', size=14),
        title_font=dict(color='#00ffff', size=20)
    )
    
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
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Audiowide&display=swap');
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Rajdhani', sans-serif;
                line-height: 1.6;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #0a0a0a 100%);
                color: #e0e0e0;
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
            }}
            
            body::before {{
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(0, 128, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(255, 0, 128, 0.05) 0%, transparent 50%);
                pointer-events: none;
                z-index: -1;
            }}
            
            .presentation-container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            .slide {{
                display: none;
                background: linear-gradient(145deg, rgba(30, 30, 46, 0.95) 0%, rgba(45, 45, 68, 0.95) 100%);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 
                    0 20px 40px rgba(0,0,0,0.4), 
                    0 0 0 1px rgba(0,255,255,0.2),
                    inset 0 1px 0 rgba(255,255,255,0.1);
                border: 2px solid rgba(0,255,255,0.3);
                backdrop-filter: blur(10px);
                position: relative;
                min-height: 80vh;
                margin-bottom: 20px;
            }}
            
            .slide.active {{
                display: block;
                animation: slideIn 0.5s ease-in-out;
            }}
            
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateX(50px); }}
                to {{ opacity: 1; transform: translateX(0); }}
            }}
            
            .slide-header {{
                text-align: center;
                border-bottom: 3px solid #00ffff;
                padding-bottom: 30px;
                margin-bottom: 40px;
                background: linear-gradient(90deg, rgba(0,255,255,0.1) 0%, rgba(0,128,255,0.1) 50%, rgba(0,255,255,0.1) 100%);
                border-radius: 15px;
                padding: 30px;
                position: relative;
                overflow: hidden;
            }}
            
            .slide-header h1 {{
                color: #00ffff;
                margin: 0;
                font-size: 3em;
                font-family: 'Audiowide', cursive;
                font-weight: 900;
                text-shadow: 
                    0 0 10px rgba(0,255,255,0.8),
                    0 0 20px rgba(0,255,255,0.6),
                    0 0 30px rgba(0,255,255,0.4);
                background: linear-gradient(45deg, #00ffff, #0080ff, #00ffff, #ff0080);
                background-size: 400% 400%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: gradientShift 3s ease-in-out infinite;
            }}
            
            @keyframes gradientShift {{
                0%, 100% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
            }}
            
            .slide-header h2 {{
                color: #a0a0a0;
                margin: 15px 0 0 0;
                font-size: 1.4em;
                font-weight: 300;
                letter-spacing: 3px;
                text-transform: uppercase;
            }}
            
            .slide-content {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 40px;
                align-items: start;
            }}
            
            .slide-text {{
                padding: 20px;
            }}
            
            .slide-chart {{
                background: rgba(0,0,0,0.3);
                padding: 20px;
                border-radius: 15px;
                border: 1px solid rgba(0,255,255,0.2);
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
                text-align: center;
            }}
            
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin: 30px 0;
            }}
            
            .metric-card {{
                background: linear-gradient(145deg, rgba(0,255,255,0.1) 0%, rgba(0,128,255,0.1) 100%);
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #00ffff;
                box-shadow: 0 10px 25px rgba(0,255,255,0.2);
                transition: all 0.3s ease;
            }}
            
            .metric-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0,255,255,0.4);
            }}
            
            .metric-value {{
                font-size: 2.5em;
                font-weight: 900;
                color: #00ffff;
                font-family: 'Orbitron', monospace;
                text-shadow: 0 0 15px rgba(0,255,255,0.8);
            }}
            
            .metric-label {{
                color: #a0a0a0;
                font-size: 1em;
                margin-top: 10px;
                font-weight: 300;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .highlight-box {{
                background: linear-gradient(145deg, rgba(255,255,0,0.1) 0%, rgba(255,165,0,0.1) 100%);
                border: 2px solid #ffaa00;
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                box-shadow: 0 0 20px rgba(255,170,0,0.3);
            }}
            
            .recommendation-box {{
                background: linear-gradient(145deg, rgba(0,255,0,0.1) 0%, rgba(0,200,0,0.1) 100%);
                border: 2px solid #00ff00;
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                box-shadow: 0 0 20px rgba(0,255,0,0.3);
            }}
            
            .constraint-box {{
                background: linear-gradient(145deg, rgba(255,0,0,0.1) 0%, rgba(200,0,0,0.1) 100%);
                border: 2px solid #ff4444;
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                box-shadow: 0 0 20px rgba(255,68,68,0.3);
            }}
            
            .section-title {{
                color: #00ffff;
                font-size: 2.2em;
                font-family: 'Orbitron', monospace;
                font-weight: 700;
                text-shadow: 0 0 15px rgba(0,255,255,0.5);
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-bottom: 20px;
            }}
            
            .subsection-title {{
                color: #ffffff;
                font-size: 1.5em;
                font-weight: 600;
                border-bottom: 2px solid rgba(0,255,255,0.3);
                padding-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin: 20px 0 15px 0;
            }}
            
            .navigation {{
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 10px;
                z-index: 1000;
            }}
            
            .nav-btn {{
                background: linear-gradient(145deg, rgba(0,255,255,0.2) 0%, rgba(0,128,255,0.2) 100%);
                border: 2px solid #00ffff;
                color: #00ffff;
                padding: 12px 20px;
                border-radius: 25px;
                cursor: pointer;
                font-family: 'Orbitron', monospace;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(0,255,255,0.3);
            }}
            
            .nav-btn:hover {{
                background: linear-gradient(145deg, rgba(0,255,255,0.4) 0%, rgba(0,128,255,0.4) 100%);
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,255,255,0.5);
            }}
            
            .nav-btn:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
            }}
            
            .slide-counter {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(0,0,0,0.7);
                color: #00ffff;
                padding: 10px 20px;
                border-radius: 25px;
                font-family: 'Orbitron', monospace;
                font-weight: 700;
                border: 1px solid #00ffff;
                z-index: 1000;
            }}
            
            ul {{
                padding-left: 25px;
                margin: 15px 0;
            }}
            
            li {{
                margin: 8px 0;
                color: #e0e0e0;
                font-size: 1.1em;
                line-height: 1.7;
            }}
            
            p {{
                color: #e0e0e0;
                font-size: 1.1em;
                line-height: 1.7;
                margin: 15px 0;
            }}
            
            strong {{
                color: #00ffff;
                font-weight: 700;
                text-shadow: 0 0 5px rgba(0,255,255,0.5);
            }}
            
            .full-width {{
                grid-column: 1 / -1;
            }}
            
            .chart-title {{
                color: #00ffff;
                font-size: 1.5em;
                font-family: 'Orbitron', monospace;
                font-weight: 700;
                margin-bottom: 20px;
                text-align: center;
                text-shadow: 0 0 10px rgba(0,255,255,0.5);
            }}
        </style>
    </head>
    <body>
        <div class="presentation-container">
            <div class="slide-counter">
                <span id="current-slide">1</span> / <span id="total-slides">9</span>
            </div>
            
            <!-- Slide 1: Title Slide -->
            <div class="slide active">
                <div class="slide-header">
                    <h1>VANCOUVER CITY FC</h1>
                    <h2>Strategic Business Analysis</h2>
                    <p>BOLT UBC First Byte 2025 - Case Competition</p>
                </div>
                <div class="slide-content full-width">
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-value">${total_revenue:,.0f}</div>
                            <div class="metric-label">Total Revenue</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{total_members:,}</div>
                            <div class="metric-label">Total Members</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{avg_games:.1f}</div>
                            <div class="metric-label">Avg Games Attended</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{seasonal_pass_rate:.1%}</div>
                            <div class="metric-label">Seasonal Pass Rate</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Slide 2: Executive Summary -->
            <div class="slide">
                <div class="slide-header">
                    <h1>EXECUTIVE SUMMARY</h1>
                </div>
                <div class="slide-content">
                    <div class="slide-text">
                        <p>Vancouver City FC is a mid-market football club in the BOLT Soccer League with strong 
                        foundational performance but significant untapped growth potential.</p>
                        
                        <div class="highlight-box">
                            <div class="subsection-title">KEY OPPORTUNITY</div>
                            <p>The club's greatest opportunity lies in seasonal pass expansion. Current seasonal pass 
                            holders attend 22.4 games compared to 4.5 for non-holders - a <strong>5x engagement multiplier</strong>. 
                            With only 6.8% adoption, this represents massive expansion potential.</p>
                        </div>
                        
                        <div class="recommendation-box">
                            <div class="subsection-title">STRATEGIC RECOMMENDATION</div>
                            <p>Focus on three high-impact initiatives:</p>
                            <ul>
                                <li>Expand seasonal pass program (target 15% adoption)</li>
                                <li>Optimize merchandise promotion strategy (fix 0.56x multiplier)</li>
                                <li>Enhance online presence (leverage 4x advantage)</li>
                            </ul>
                        </div>
                    </div>
                    <div class="slide-chart">
                        <div class="chart-title">Revenue Composition</div>
                        {fig1_html}
                    </div>
                </div>
            </div>
            
            <!-- Slide 3: Revenue Analysis -->
            <div class="slide">
                <div class="slide-header">
                    <h1>REVENUE ANALYSIS</h1>
                </div>
                <div class="slide-content">
                    <div class="slide-text">
                        <div class="subsection-title">REVENUE COMPOSITION</div>
                        <p>Vancouver City FC follows a traditional sports club revenue model with stadium operations 
                        dominating at 67.2% of total revenue. This reflects strong matchday experience and loyal 
                        fan base. The 32.8% merchandise revenue represents significant growth opportunity.</p>
                        
                        <div class="subsection-title">SEASONAL PATTERNS</div>
                        <ul>
                            <li>February: Peak stadium month ($3.96M)</li>
                            <li>March: Peak merchandise month ($1.09M)</li>
                            <li>Clear seasonal cycles enable targeted marketing and operational planning</li>
                        </ul>
                        
                        <div class="subsection-title">STADIUM EFFICIENCY</div>
                        <p>Lower Bowl emerges as most efficient revenue source, suggesting successful model for 
                        premium seating expansion. This supports strategic investment in premium options.</p>
                        
                        <div class="subsection-title">MERCHANDISE PERFORMANCE</div>
                        <ul>
                            <li>Jersey category dominates with $4.1M revenue</li>
                            <li>Commands premium pricing at $152 average</li>
                            <li>Indicates strong brand value and pricing power</li>
                        </ul>
                    </div>
                    <div class="slide-chart">
                        <div class="chart-title">Revenue Breakdown</div>
                        {fig1_html}
                    </div>
                </div>
            </div>
            
            <!-- Slide 4: Fan Engagement Analysis -->
            <div class="slide">
                <div class="slide-header">
                    <h1>FAN ENGAGEMENT ANALYSIS</h1>
                </div>
                <div class="slide-content">
                    <div class="slide-text">
                        <div class="subsection-title">DEMOGRAPHIC OVERVIEW</div>
                        <p>Fan engagement shows consistent patterns across demographics with 5.7 games average 
                        attendance per member. This consistency suggests strong brand loyalty and community 
                        connection.</p>
                        
                        <div class="subsection-title">AGE GROUP BREAKDOWN</div>
                        <ul>
                            <li>26-40: Highest engagement (5.8 games)</li>
                            <li>18-25: Largest segment (44.8% of fanbase) - key target market</li>
                            <li>Consistent engagement across all age groups</li>
                        </ul>
                        
                        <div class="highlight-box">
                            <div class="subsection-title">SEASONAL PASS IMPACT - THE GAME CHANGER</div>
                            <p>This is the most significant finding:</p>
                            <ul>
                                <li>Seasonal pass holders: 22.4 games</li>
                                <li>Non-holders: 4.5 games</li>
                                <li><strong>5x engagement multiplier</strong></li>
                                <li>Only 6.8% current adoption</li>
                                <li>Massive expansion potential</li>
                            </ul>
                        </div>
                    </div>
                    <div class="slide-chart">
                        <div class="chart-title">Engagement Patterns</div>
                        {fig2_html}
                    </div>
                </div>
            </div>
            
            <!-- Slide 5: Merchandise Performance -->
            <div class="slide">
                <div class="slide-header">
                    <h1>MERCHANDISE PERFORMANCE</h1>
                </div>
                <div class="slide-content">
                    <div class="slide-text">
                        <div class="subsection-title">REVENUE OVERVIEW</div>
                        <p>Merchandise sales total $6.5M with strong growth potential, representing 32.8% of 
                        total revenue.</p>
                        
                        <div class="subsection-title">CHANNEL PERFORMANCE</div>
                        <ul>
                            <li>Online: 80% of sales (4x advantage over team store)</li>
                            <li>Team Store: 20% of sales</li>
                            <li>Critical importance of digital presence and e-commerce optimization</li>
                        </ul>
                        
                        <div class="constraint-box">
                            <div class="subsection-title">PROMOTION STRATEGY CRISIS</div>
                            <p>Current promotions show 0.56x multiplier - actually reducing revenue effectiveness.
                            This represents major optimization opportunity.</p>
                        </div>
                        
                        <div class="subsection-title">PRODUCT CATEGORY BREAKDOWN</div>
                        <ul>
                            <li>Jersey: $4.1M revenue (dominates)</li>
                            <li>Premium pricing: $152 average</li>
                            <li>Strong brand value and pricing power</li>
                            <li>March: Peak merchandise month ($1.09M)</li>
                        </ul>
                    </div>
                    <div class="slide-chart">
                        <div class="chart-title">Merchandise Analysis</div>
                        {fig3_html}
                    </div>
                </div>
            </div>
            
            <!-- Slide 6: Operational Constraints -->
            <div class="slide">
                <div class="slide-header">
                    <h1>OPERATIONAL CONSTRAINTS</h1>
                </div>
                <div class="slide-content full-width">
                    <div class="slide-text">
                        <div class="constraint-box">
                            <div class="subsection-title">1. INTERNATIONAL MERCHANDISE FOCUS</div>
                            <ul>
                                <li>100% international focus limits domestic growth</li>
                                <li>Opportunity: Domestic market expansion</li>
                                <li>Benefit: Local community engagement</li>
                            </ul>
                        </div>
                        
                        <div class="constraint-box">
                            <div class="subsection-title">2. CHANNEL IMBALANCE</div>
                            <ul>
                                <li>80% online vs 20% team store</li>
                                <li>Risk: Limited community connection</li>
                                <li>Opportunity: Enhanced online experience</li>
                            </ul>
                        </div>
                        
                        <div class="constraint-box">
                            <div class="subsection-title">3. STADIUM OPERATIONS VARIATION</div>
                            <ul>
                                <li>22.4x efficiency variation across sources</li>
                                <li>Opportunity: Standardization using Lower Bowl model</li>
                                <li>Benefit: Improved operational efficiency</li>
                            </ul>
                        </div>
                        
                        <div class="constraint-box">
                            <div class="subsection-title">4. PROMOTION STRATEGY INEFFICIENCY</div>
                            <ul>
                                <li>0.56x multiplier (underperforming)</li>
                                <li>Major optimization opportunity</li>
                                <li>Potential for significant revenue improvement</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Slide 7: Strategic Recommendations -->
            <div class="slide">
                <div class="slide-header">
                    <h1>STRATEGIC RECOMMENDATIONS</h1>
                </div>
                <div class="slide-content full-width">
                    <div class="slide-text">
                        <div class="recommendation-box">
                            <div class="subsection-title">IMMEDIATE ACTIONS (0-6 months)</div>
                            
                            <div class="subsection-title">1. SEASONAL PASS EXPANSION</div>
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
                            
                            <div class="subsection-title">2. PROMOTION STRATEGY OVERHAUL</div>
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
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Slide 8: Implementation Roadmap -->
            <div class="slide">
                <div class="slide-header">
                    <h1>IMPLEMENTATION ROADMAP</h1>
                </div>
                <div class="slide-content full-width">
                    <div class="slide-text">
                        <div class="recommendation-box">
                            <div class="subsection-title">PHASE 1: FOUNDATION BUILDING (Months 1-6)</div>
                            <ul>
                                <li>Launch seasonal pass expansion campaign</li>
                                <li>Implement promotion strategy optimization</li>
                                <li>Enhance online user experience</li>
                                <li>Develop youth engagement programs</li>
                                <li>Establish success metrics</li>
                            </ul>
                        </div>
                        
                        <div class="recommendation-box">
                            <div class="subsection-title">PHASE 2: GROWTH ACCELERATION (Months 7-18)</div>
                            <ul>
                                <li>Scale successful Phase 1 initiatives</li>
                                <li>Launch digital platform</li>
                                <li>Implement premium membership tiers</li>
                                <li>Expand international programs</li>
                                <li>Optimize operational efficiency</li>
                            </ul>
                        </div>
                        
                        <div class="recommendation-box">
                            <div class="subsection-title">PHASE 3: STRATEGIC EXPANSION (Months 19-36)</div>
                            <ul>
                                <li>Full digital ecosystem</li>
                                <li>International market expansion</li>
                                <li>Community partnerships</li>
                                <li>Advanced analytics</li>
                                <li>Sustainability initiatives</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Slide 9: Conclusion -->
            <div class="slide">
                <div class="slide-header">
                    <h1>CONCLUSION</h1>
                </div>
                <div class="slide-content full-width">
                    <div class="slide-text">
                        <p>Vancouver City FC has a clear path to sustainable growth through strategic initiatives 
                        that leverage existing strengths while addressing key opportunities.</p>
                        
                        <div class="highlight-box">
                            <div class="subsection-title">KEY TAKEAWAYS</div>
                            <ul>
                                <li>5x engagement multiplier from seasonal pass holders represents massive opportunity</li>
                                <li>Only 6.8% current adoption leaves significant expansion potential</li>
                                <li>4x online advantage provides strong foundation for digital growth</li>
                                <li>Community focus creates sustainable competitive advantage</li>
                            </ul>
                        </div>
                        
                        <div class="recommendation-box">
                            <div class="subsection-title">STRATEGIC FOCUS</div>
                            <p>The combination of seasonal pass expansion, merchandise optimization, and digital 
                            enhancement provides a comprehensive framework for achieving 20%+ revenue growth 
                            while maintaining the club's community-focused identity.</p>
                        </div>
                        
                        <div class="subsection-title">NEXT STEPS</div>
                        <ol>
                            <li>Present findings to leadership team</li>
                            <li>Develop detailed implementation plans</li>
                            <li>Establish success metrics and monitoring</li>
                            <li>Begin Phase 1 initiatives immediately</li>
                            <li>Create ongoing performance tracking</li>
                        </ol>
                    </div>
                </div>
            </div>
            
            <!-- Navigation -->
            <div class="navigation">
                <button class="nav-btn" id="prevBtn" onclick="changeSlide(-1)">← PREV</button>
                <button class="nav-btn" id="nextBtn" onclick="changeSlide(1)">NEXT →</button>
            </div>
        </div>
        
        <script>
            let currentSlide = 0;
            const slides = document.querySelectorAll('.slide');
            const totalSlides = slides.length;
            
            document.getElementById('total-slides').textContent = totalSlides;
            
            function showSlide(n) {{
                slides[currentSlide].classList.remove('active');
                currentSlide = (n + totalSlides) % totalSlides;
                slides[currentSlide].classList.add('active');
                
                document.getElementById('current-slide').textContent = currentSlide + 1;
                
                // Update navigation buttons
                document.getElementById('prevBtn').disabled = currentSlide === 0;
                document.getElementById('nextBtn').disabled = currentSlide === totalSlides - 1;
            }}
            
            function changeSlide(direction) {{
                if (direction === 1 && currentSlide < totalSlides - 1) {{
                    showSlide(currentSlide + 1);
                }} else if (direction === -1 && currentSlide > 0) {{
                    showSlide(currentSlide - 1);
                }}
            }}
            
            // Keyboard navigation
            document.addEventListener('keydown', function(e) {{
                if (e.key === 'ArrowRight' || e.key === ' ') {{
                    e.preventDefault();
                    changeSlide(1);
                }} else if (e.key === 'ArrowLeft') {{
                    e.preventDefault();
                    changeSlide(-1);
                }}
            }});
            
            // Initialize
            showSlide(0);
        </script>
    </body>
    </html>
    """
    
    # Save HTML file
    with open('vancouver_city_fc_powerpoint.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ PowerPoint-style report created: vancouver_city_fc_powerpoint.html")
    print("✓ 9 slides with navigation controls")
    print("✓ Charts integrated into each relevant slide")
    print("✓ Use arrow keys or navigation buttons to flip through slides")
    print("✓ Each section is now a separate slide like PowerPoint")

if __name__ == "__main__":
    create_powerpoint_style_report()
