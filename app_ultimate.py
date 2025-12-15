import streamlit as st
import pandas as pd
import json
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Set page config
st.set_page_config(
    page_title="HTS AI Agent - Ultimate Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced styling
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            font-family: 'Inter', sans-serif;
        }
        
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .notification {
            background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .success-box {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .comparison-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
            font-family: 'Inter', sans-serif;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
    </style>
    """, unsafe_allow_html=True)

# Enhanced HTS database
def get_hts_database():
    return {
        "0101.30.00.00": {
            "description": "Live asses",
            "duty_rate": 0.0,
            "category": "Live Animals",
            "units": "Number",
            "special_programs": ["GSP"],
            "origin_rates": {"China": 0.0, "EU": 0.0, "USMCA": 0.0},
            "seasonal": False,
            "avg_value": 5000
        },
        "0102.21.00.00": {
            "description": "Live cattle, purebred breeding animals",
            "duty_rate": 0.025,
            "category": "Live Animals",
            "units": "Number",
            "special_programs": ["USMCA"],
            "origin_rates": {"China": 0.025, "EU": 0.025, "USMCA": 0.0},
            "seasonal": False,
            "avg_value": 15000
        },
        "0201.10.00.00": {
            "description": "Beef carcasses and half-carcasses, fresh or chilled",
            "duty_rate": 0.044,
            "category": "Meat Products",
            "units": "kg",
            "special_programs": ["TRQ"],
            "origin_rates": {"China": 0.044, "EU": 0.044, "USMCA": 0.0},
            "seasonal": False,
            "avg_value": 8
        },
        "8471.30.01.00": {
            "description": "Portable digital automatic data processing machines",
            "duty_rate": 0.0,
            "category": "Electronics",
            "units": "Number",
            "special_programs": ["ITA"],
            "origin_rates": {"China": 0.25, "EU": 0.0, "USMCA": 0.0},
            "seasonal": False,
            "avg_value": 800
        },
        "6109.10.00.40": {
            "description": "T-shirts, singlets and other vests, knitted, of cotton",
            "duty_rate": 0.165,
            "category": "Textiles",
            "units": "Dozen",
            "special_programs": ["CAFTA"],
            "origin_rates": {"China": 0.165, "EU": 0.12, "USMCA": 0.0},
            "seasonal": False,
            "avg_value": 45
        }
    }

# Initialize session state
def init_session_state():
    if 'calculations_history' not in st.session_state:
        st.session_state.calculations_history = []
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'theme': 'light',
            'default_currency': 'USD',
            'favorite_hts_codes': [],
            'last_country': 'China'
        }
    if 'batch_items' not in st.session_state:
        st.session_state.batch_items = []
    if 'comparison_items' not in st.session_state:
        st.session_state.comparison_items = []

def main():
    load_css()
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌐 HTS AI Agent - Ultimate Pro</h1>
        <p>Advanced Trade Intelligence & Duty Calculation Platform</p>
        <p style="font-size: 0.9em; opacity: 0.8;">Complete suite with all enhanced features</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Sidebar
    with st.sidebar:
        st.header("🛠️ Ultimate Control Panel")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        st.metric("Calculations", len(st.session_state.calculations_history))
        st.metric("Batch Items", len(st.session_state.batch_items))
        st.metric("Comparisons", len(st.session_state.comparison_items))
        
        # Navigation
        page = st.selectbox("Choose Feature:", [
            "🏠 Ultimate Dashboard", 
            "📊 Pro Calculator", 
            "🔄 Batch Processing",
            "📈 Comparison Tool",
            "💬 Smart Assistant",
            "📊 Advanced Analytics",
            "🔍 HTS Explorer",
            "⚡ Quick Tools",
            "🎯 Trade Simulator",
            "🌍 Global Rates"
        ])
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Recalc", key="quick_recalc"):
                if st.session_state.calculations_history:
                    st.session_state.quick_recalc = True
        
        with col2:
            if st.button("📥 Export", key="quick_export"):
                st.session_state.show_export = True
        
        if st.button("🗑️ Clear All", key="clear_all_data"):
            clear_all_data()
    
    # Route to pages
    if page == "🏠 Ultimate Dashboard":
        render_ultimate_dashboard()
    elif page == "📊 Pro Calculator":
        render_pro_calculator()
    elif page == "🔄 Batch Processing":
        render_batch_processing()
    elif page == "📈 Comparison Tool":
        render_comparison_tool()
    elif page == "💬 Smart Assistant":
        render_smart_assistant()
    elif page == "📊 Advanced Analytics":
        render_advanced_analytics()
    elif page == "🔍 HTS Explorer":
        render_hts_explorer()
    elif page == "⚡ Quick Tools":
        render_quick_tools()
    elif page == "🎯 Trade Simulator":
        render_trade_simulator()
    else:
        render_global_rates()

def clear_all_data():
    """Clear all application data"""
    st.session_state.calculations_history = []
    st.session_state.batch_items = []
    st.session_state.comparison_items = []
    st.success("All data cleared!")

def render_ultimate_dashboard():
    st.header("🏠 Ultimate Executive Dashboard")
    
    # Real-time metrics
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>125</h3>
            <p>Total Queries</p>
            <small>↗️ +12 today</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        calc_count = 87 + len(st.session_state.calculations_history)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{calc_count}</h3>
            <p>Calculations</p>
            <small>🔄 Live count</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>8.5%</h3>
            <p>Avg Duty Rate</p>
            <small>📊 Weighted</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>$12.5K</h3>
            <p>Est. Savings</p>
            <small>💰 This month</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        batch_count = len(st.session_state.batch_items)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{batch_count}</h3>
            <p>Batch Queue</p>
            <small>⏳ Pending</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div class="metric-card">
            <h3>15</h3>
            <p>Countries</p>
            <small>🌍 Coverage</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature showcase
    st.subheader("🚀 Featured Capabilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🔄 Intelligent Batch Processing</h4>
            <p>Process thousands of HTS codes with smart validation, error detection, and comprehensive reporting.</p>
            <ul>
                <li>Excel/CSV import</li>
                <li>Real-time progress tracking</li>
                <li>Error handling & validation</li>
                <li>Professional export formats</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>📈 Advanced Comparison Engine</h4>
            <p>Compare duty rates across multiple countries and trade agreements with visual analytics.</p>
            <ul>
                <li>Multi-country analysis</li>
                <li>Trade agreement optimization</li>
                <li>Cost savings identification</li>
                <li>Interactive visualizations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Smart Trade Simulator</h4>
            <p>Simulate different trade scenarios and optimize your supply chain decisions.</p>
            <ul>
                <li>Scenario modeling</li>
                <li>Risk assessment</li>
                <li>ROI calculations</li>
                <li>Strategic recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Live activity feed
    if st.session_state.calculations_history:
        st.subheader("📡 Recent Activity")
        
        # Show last 5 calculations
        recent = st.session_state.calculations_history[-5:]
        df_recent = pd.DataFrame(recent)
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    
    # Quick action buttons
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 New Calculation", key="dash_calc", type="primary"):
            st.session_state.quick_nav = "📊 Pro Calculator"
    
    with col2:
        if st.button("📊 Start Batch", key="dash_batch"):
            st.session_state.quick_nav = "🔄 Batch Processing"
    
    with col3:
        if st.button("📈 Compare Rates", key="dash_compare"):
            st.session_state.quick_nav = "📈 Comparison Tool"
    
    with col4:
        if st.button("📊 View Analytics", key="dash_analytics"):
            st.session_state.quick_nav = "📊 Advanced Analytics"

def render_pro_calculator():
    st.header("📊 Professional Duty Calculator")
    
    # Calculator modes
    mode = st.radio("Calculator Mode:", 
                   ["🎯 Standard", "🔬 Advanced", "🌍 Multi-Country", "⚡ Express"], 
                   horizontal=True)
    
    if mode == "🎯 Standard":
        render_standard_calc()
    elif mode == "🔬 Advanced":
        render_advanced_calc()
    elif mode == "🌍 Multi-Country":
        render_multi_country_calc()
    else:
        render_express_calc()

def render_standard_calc():
    st.subheader("🎯 Standard Professional Calculator")
    
    # Input section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📦 Product Details")
        hts_database = get_hts_database()
        hts_codes = list(hts_database.keys())
        
        hts_code = st.selectbox("HTS Code", hts_codes, 
                               format_func=lambda x: f"{x} - {hts_database[x]['description'][:40]}...")
        
        if hts_code:
            hts_info = hts_database[hts_code]
            st.info(f"**Category**: {hts_info['category']}")
            st.info(f"**Average Value**: ${hts_info['avg_value']:,.2f}")
        
        product_cost = st.number_input("Product Cost ($)", value=float(hts_info['avg_value']), 
                                      min_value=0.0, step=100.0)
        quantity = st.number_input("Quantity", value=1, min_value=1, step=1)
    
    with col2:
        st.markdown("#### 🚚 Shipping & Origin")
        countries = ["China", "Germany", "Japan", "Mexico", "Canada", "Vietnam", "India", "Brazil"]
        country_origin = st.selectbox("Country of Origin", countries)
        
        freight = st.number_input("Freight ($)", value=product_cost * 0.05, min_value=0.0)
        insurance = st.number_input("Insurance ($)", value=product_cost * 0.01, min_value=0.0)
        
        shipping_method = st.selectbox("Shipping Method", 
                                      ["Sea Freight", "Air Freight", "Express", "Land"])
    
    with col3:
        st.markdown("#### 💰 Additional Costs")
        handling_fee = st.number_input("Handling Fee ($)", value=50.0, min_value=0.0)
        broker_fee = st.number_input("Broker Fee ($)", value=150.0, min_value=0.0)
        exam_fee = st.number_input("Examination Fee ($)", value=0.0, min_value=0.0)
        
        # Trade preferences
        use_preferential = st.checkbox("Apply Trade Preferences", 
                                      help="Use preferential rates if available")
    
    # Calculate button
    if st.button("🔄 Calculate Professional Duty", type="primary", key="std_calc_btn"):
        calculate_standard_duty(hts_code, product_cost, freight, insurance, 
                               country_origin, quantity, handling_fee, broker_fee, 
                               exam_fee, use_preferential)

def calculate_standard_duty(hts_code, product_cost, freight, insurance, country_origin, 
                           quantity, handling_fee, broker_fee, exam_fee, use_preferential):
    
    hts_database = get_hts_database()
    hts_info = hts_database[hts_code]
    
    # Calculate base values
    cif_value = product_cost + freight + insurance
    
    # Determine duty rate
    if country_origin in hts_info["origin_rates"]:
        duty_rate = hts_info["origin_rates"][country_origin]
    else:
        duty_rate = hts_info["duty_rate"]
    
    # Apply preferential treatment
    preferential_applied = False
    if use_preferential:
        if "USMCA" in hts_info["special_programs"] and country_origin in ["Mexico", "Canada"]:
            duty_rate = 0.0
            preferential_applied = True
        elif "GSP" in hts_info["special_programs"]:
            duty_rate = 0.0
            preferential_applied = True
    
    # Calculate duty and total costs
    duty_amount = cif_value * duty_rate
    additional_fees = handling_fee + broker_fee + exam_fee
    total_landed_cost = cif_value + duty_amount + additional_fees
    cost_per_unit = total_landed_cost / quantity
    
    # Display results
    st.markdown("""
    <div class="success-box">
        <h3>✅ Professional Calculation Complete</h3>
        <p>Comprehensive duty calculation with all applicable rates and fees</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("CIF Value", f"${cif_value:,.2f}")
    with col2:
        st.metric("Duty Amount", f"${duty_amount:,.2f}", f"{duty_rate*100:.2f}%")
    with col3:
        st.metric("Additional Fees", f"${additional_fees:,.2f}")
    with col4:
        st.metric("Total Landed Cost", f"${total_landed_cost:,.2f}")
    with col5:
        st.metric("Cost per Unit", f"${cost_per_unit:,.2f}")
    
    # Detailed breakdown
    st.subheader("📋 Professional Breakdown")
    
    breakdown_data = {
        "Cost Component": [
            "Product Cost", "Freight", "Insurance", "CIF Value", 
            "Import Duties", "Handling Fee", "Broker Fee", "Exam Fee",
            "TOTAL LANDED COST"
        ],
        "Amount (USD)": [
            f"${product_cost:,.2f}", f"${freight:,.2f}", f"${insurance:,.2f}",
            f"${cif_value:,.2f}", f"${duty_amount:,.2f}", f"${handling_fee:,.2f}",
            f"${broker_fee:,.2f}", f"${exam_fee:,.2f}", f"${total_landed_cost:,.2f}"
        ],
        "Percentage": [
            f"{(product_cost/total_landed_cost)*100:.1f}%",
            f"{(freight/total_landed_cost)*100:.1f}%",
            f"{(insurance/total_landed_cost)*100:.1f}%",
            f"{(cif_value/total_landed_cost)*100:.1f}%",
            f"{(duty_amount/total_landed_cost)*100:.1f}%",
            f"{(handling_fee/total_landed_cost)*100:.1f}%",
            f"{(broker_fee/total_landed_cost)*100:.1f}%",
            f"{(exam_fee/total_landed_cost)*100:.1f}%",
            "100.0%"
        ]
    }
    
    df_breakdown = pd.DataFrame(breakdown_data)
    st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
    
    # Trade information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Product Information:**
        - HTS Code: {hts_code}
        - Description: {hts_info['description']}
        - Category: {hts_info['category']}
        - Units: {hts_info['units']}
        """)
    
    with col2:
        st.markdown(f"""
        **Trade Details:**
        - Origin: {country_origin}
        - Standard Rate: {hts_info['duty_rate']*100:.2f}%
        - Applied Rate: {duty_rate*100:.2f}%
        - Preferential: {'✅ Yes' if preferential_applied else '❌ No'}
        """)
    
    # Save calculation
    calculation_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hts_code": hts_code,
        "description": hts_info['description'],
        "country_origin": country_origin,
        "product_cost": product_cost,
        "cif_value": cif_value,
        "duty_rate": duty_rate,
        "duty_amount": duty_amount,
        "total_landed_cost": total_landed_cost,
        "quantity": quantity,
        "preferential": preferential_applied
    }
    
    st.session_state.calculations_history.append(calculation_record)
    
    # Export options
    st.subheader("💾 Export Professional Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        export_data = {
            "calculation": calculation_record,
            "breakdown": breakdown_data,
            "metadata": {"calculation_type": "Professional Standard"}
        }
        
        st.download_button(
            "📥 JSON Report",
            data=json.dumps(export_data, indent=2),
            file_name=f"professional_duty_{hts_code.replace('.', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="export_prof_json"
        )
    
    with col2:
        st.download_button(
            "📥 CSV Data",
            data=df_breakdown.to_csv(index=False),
            file_name=f"duty_breakdown_{hts_code.replace('.', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="export_prof_csv"
        )
    
    with col3:
        report_text = f"""
PROFESSIONAL DUTY CALCULATION REPORT
===================================

Product: {hts_info['description']}
HTS Code: {hts_code}
Origin: {country_origin}
Date: {calculation_record['timestamp']}

FINANCIAL SUMMARY:
- Product Cost: ${product_cost:,.2f}
- CIF Value: ${cif_value:,.2f}
- Duty Rate: {duty_rate*100:.2f}%
- Duty Amount: ${duty_amount:,.2f}
- Total Landed Cost: ${total_landed_cost:,.2f}
- Cost per Unit: ${cost_per_unit:,.2f}

TRADE INFORMATION:
- Preferential Treatment: {'Applied' if preferential_applied else 'Not Applied'}
- Special Programs: {', '.join(hts_info['special_programs'])}

Generated by HTS AI Agent Ultimate Pro
        """
        
        st.download_button(
            "📥 Text Report",
            data=report_text,
            file_name=f"duty_report_{hts_code.replace('.', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="export_prof_txt"
        )

def render_batch_processing():
    st.header("🔄 Advanced Batch Processing Center")
    
    st.markdown("""
    <div class="notification">
        💡 <strong>Intelligent Batch Processing</strong><br>
        Process multiple HTS codes with advanced validation, error handling, and comprehensive reporting.
    </div>
    """, unsafe_allow_html=True)
    
    # Batch method selection
    method = st.radio("Processing Method:", 
                     ["📝 Manual Entry", "📄 CSV Upload", "📊 Excel Import", "🔄 Quick Batch"], 
                     horizontal=True)
    
    if method == "📝 Manual Entry":
        render_manual_batch()
    elif method == "📄 CSV Upload":
        render_csv_batch()
    elif method == "📊 Excel Import":
        render_excel_batch()
    else:
        render_quick_batch()

def render_manual_batch():
    st.subheader("📝 Manual Batch Entry")
    
    # Add item form
    with st.expander("➕ Add Items to Batch", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            hts_codes = list(get_hts_database().keys())
            new_hts = st.selectbox("HTS Code", hts_codes, key="batch_hts_manual")
        
        with col2:
            new_cost = st.number_input("Product Cost ($)", value=1000.0, min_value=0.0, key="batch_cost_manual")
        
        with col3:
            new_country = st.selectbox("Origin", ["China", "Germany", "Japan", "Mexico", "Canada"], key="batch_country_manual")
        
        with col4:
            new_qty = st.number_input("Quantity", value=1, min_value=1, key="batch_qty_manual")
        
        if st.button("➕ Add to Batch", key="add_batch_manual"):
            item = {
                "id": len(st.session_state.batch_items) + 1,
                "hts_code": new_hts,
                "product_cost": new_cost,
                "country": new_country,
                "quantity": new_qty,
                "status": "Pending"
            }
            st.session_state.batch_items.append(item)
            st.success(f"Added {new_hts} to batch ({len(st.session_state.batch_items)} items)")
    
    # Display current batch
    if st.session_state.batch_items:
        st.subheader(f"📦 Current Batch ({len(st.session_state.batch_items)} items)")
        
        # Batch controls
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Process All", type="primary", key="process_batch_all"):
                process_batch_items()
        
        with col2:
            if st.button("📊 Preview", key="preview_batch_items"):
                preview_batch_results()
        
        with col3:
            if st.button("🗑️ Clear Batch", key="clear_batch_items"):
                st.session_state.batch_items = []
                st.success("Batch cleared")
        
        with col4:
            if st.button("📥 Export Batch", key="export_batch_items"):
                export_batch_template()
        
        # Display batch items
        df_batch = pd.DataFrame(st.session_state.batch_items)
        st.dataframe(df_batch, use_container_width=True, hide_index=True)

def process_batch_items():
    """Process all items in the batch with progress tracking"""
    if not st.session_state.batch_items:
        st.warning("No items in batch to process")
        return
    
    st.subheader("⚡ Processing Batch Items...")
    
    # Create progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    results_container = st.empty()
    
    hts_database = get_hts_database()
    results = []
    errors = []
    
    for i, item in enumerate(st.session_state.batch_items):
        # Update progress
        progress = (i + 1) / len(st.session_state.batch_items)
        progress_bar.progress(progress)
        status_text.text(f"Processing item {i+1}/{len(st.session_state.batch_items)}: {item['hts_code']}")
        
        try:
            # Get HTS info
            if item['hts_code'] not in hts_database:
                raise ValueError(f"HTS code {item['hts_code']} not found")
            
            hts_info = hts_database[item['hts_code']]
            
            # Calculate duty
            product_cost = item['product_cost']
            freight = product_cost * 0.05  # 5% freight estimate
            insurance = product_cost * 0.01  # 1% insurance estimate
            cif_value = product_cost + freight + insurance
            
            # Get duty rate
            duty_rate = hts_info['origin_rates'].get(item['country'], hts_info['duty_rate'])
            duty_amount = cif_value * duty_rate
            
            # Additional fees
            additional_fees = 200  # Standard fees
            landed_cost = cif_value + duty_amount + additional_fees
            
            # Create result
            result = {
                "ID": item['id'],
                "HTS Code": item['hts_code'],
                "Description": hts_info['description'][:50] + "...",
                "Origin": item['country'],
                "Quantity": item['quantity'],
                "Product Cost": f"${product_cost:,.2f}",
                "CIF Value": f"${cif_value:,.2f}",
                "Duty Rate": f"{duty_rate*100:.2f}%",
                "Duty Amount": f"${duty_amount:,.2f}",
                "Landed Cost": f"${landed_cost:,.2f}",
                "Cost per Unit": f"${landed_cost/item['quantity']:,.2f}",
                "Status": "✅ Success"
            }
            
            results.append(result)
            
        except Exception as e:
            error_result = {
                "ID": item['id'],
                "HTS Code": item['hts_code'],
                "Error": str(e),
                "Status": "❌ Error"
            }
            errors.append(error_result)
        
        # Show intermediate results
        if results:
            df_results = pd.DataFrame(results)
            results_container.dataframe(df_results, use_container_width=True, hide_index=True)
        
        time.sleep(0.1)  # Simulate processing time
    
    # Final results
    progress_bar.empty()
    status_text.empty()
    
    if results:
        st.success(f"✅ Batch processing completed! Successfully processed {len(results)} items.")
        
        if errors:
            st.error(f"❌ {len(errors)} items had errors:")
            df_errors = pd.DataFrame(errors)
            st.dataframe(df_errors, use_container_width=True, hide_index=True)
        
        # Store results
        st.session_state.batch_results = results
        
        # Export options
        st.subheader("💾 Export Batch Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            df_results = pd.DataFrame(results)
            st.download_button(
                "📥 Results CSV",
                data=df_results.to_csv(index=False),
                file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key="export_batch_results_csv"
            )
        
        with col2:
            export_data = {
                "results": results,
                "errors": errors,
                "summary": {
                    "total_items": len(st.session_state.batch_items),
                    "successful": len(results),
                    "errors": len(errors),
                    "processing_date": datetime.now().isoformat()
                }
            }
            
            st.download_button(
                "📥 Full Report JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="export_batch_results_json"
            )
        
        with col3:
            # Generate summary
            total_cost = sum([float(r["Product Cost"].replace('$', '').replace(',', '')) for r in results])
            total_landed = sum([float(r["Landed Cost"].replace('$', '').replace(',', '')) for r in results])
            
            summary_text = f"""
BATCH PROCESSING SUMMARY
========================
Total Items Processed: {len(results)}
Successful: {len(results)}
Errors: {len(errors)}
Success Rate: {(len(results)/(len(results)+len(errors))*100):.1f}%

Financial Summary:
Total Product Cost: ${total_cost:,.2f}
Total Landed Cost: ${total_landed:,.2f}
Total Duty Impact: ${total_landed - total_cost:,.2f}
Average Duty Impact: {((total_landed - total_cost)/total_cost*100):.2f}%

Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated by HTS AI Agent Ultimate Pro
            """
            
            st.download_button(
                "📥 Summary Report",
                data=summary_text,
                file_name=f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="export_batch_summary"
            )

def render_comparison_tool():
    st.header("📈 Advanced Comparison Tool")
    
    st.markdown("""
    <div class="notification">
        📊 <strong>Multi-Dimensional Analysis</strong><br>
        Compare duty rates across countries, trade agreements, and shipping methods.
    </div>
    """, unsafe_allow_html=True)
    
    # Comparison setup
    comparison_type = st.radio("Comparison Type:", 
                              ["🌍 Country Comparison", "📊 HTS Code Analysis", "⚖️ Side-by-Side", "📈 Trend Analysis"], 
                              horizontal=True)
    
    if comparison_type == "🌍 Country Comparison":
        render_country_comparison()
    elif comparison_type == "📊 HTS Code Analysis":
        render_hts_analysis()
    elif comparison_type == "⚖️ Side-by-Side":
        render_side_by_side()
    else:
        render_trend_analysis()

def render_country_comparison():
    st.subheader("🌍 Country-by-Country Comparison")
    
    # Selection inputs
    col1, col2 = st.columns(2)
    
    with col1:
        hts_codes = list(get_hts_database().keys())
        selected_hts = st.selectbox("Select HTS Code", hts_codes)
    
    with col2:
        countries = ["China", "Germany", "Japan", "Mexico", "Canada", "Vietnam", "India", "Brazil"]
        selected_countries = st.multiselect("Select Countries", countries, default=["China", "Germany", "Mexico"])
    
    if selected_hts and selected_countries and st.button("📊 Generate Comparison", type="primary"):
        hts_database = get_hts_database()
        hts_info = hts_database[selected_hts]
        
        # Create comparison data
        comparison_data = []
        for country in selected_countries:
            duty_rate = hts_info['origin_rates'].get(country, hts_info['duty_rate'])
            
            # Sample calculation with $10,000 product
            sample_cost = 10000
            cif_value = sample_cost * 1.06  # Add 6% for freight/insurance
            duty_amount = cif_value * duty_rate
            landed_cost = cif_value + duty_amount + 200  # Add standard fees
            
            comparison_data.append({
                "Country": country,
                "Duty Rate": f"{duty_rate*100:.2f}%",
                "Duty Amount": f"${duty_amount:,.2f}",
                "Landed Cost": f"${landed_cost:,.2f}",
                "Cost Difference": f"${landed_cost - min([cif_value * hts_info['origin_rates'].get(c, hts_info['duty_rate']) + cif_value + 200 for c in selected_countries]):,.2f}",
                "Savings Potential": f"{((max([landed_cost for c in selected_countries]) - landed_cost) / max([landed_cost for c in selected_countries]) * 100):.1f}%"
            })
        
        # Display comparison table
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
        
        # Visualization
        st.subheader("📊 Visual Comparison")
        
        # Create charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Duty rate comparison
            rates = [hts_info['origin_rates'].get(country, hts_info['duty_rate'])*100 for country in selected_countries]
            
            fig_bar = go.Figure(data=[go.Bar(x=selected_countries, y=rates)])
            fig_bar.update_layout(title="Duty Rates by Country", 
                                 xaxis_title="Country", yaxis_title="Duty Rate (%)")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Cost comparison
            costs = [cif_value * hts_info['origin_rates'].get(country, hts_info['duty_rate']) + cif_value + 200 
                    for country in selected_countries]
            
            fig_pie = go.Figure(data=[go.Pie(labels=selected_countries, values=costs)])
            fig_pie.update_layout(title="Total Cost Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Smart Recommendations")
        
        best_country = min(selected_countries, 
                          key=lambda c: cif_value * hts_info['origin_rates'].get(c, hts_info['duty_rate']) + cif_value + 200)
        
        worst_country = max(selected_countries, 
                           key=lambda c: cif_value * hts_info['origin_rates'].get(c, hts_info['duty_rate']) + cif_value + 200)
        
        st.markdown(f"""
        <div class="feature-card">
            <h4>🎯 Optimization Insights</h4>
            <ul>
                <li><strong>Best Option:</strong> {best_country} with lowest total cost</li>
                <li><strong>Highest Cost:</strong> {worst_country}</li>
                <li><strong>Product:</strong> {hts_info['description']}</li>
                <li><strong>Special Programs:</strong> {', '.join(hts_info['special_programs'])}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def render_smart_assistant():
    st.header("💬 Smart Trade Assistant")
    
    st.markdown("""
    <div class="notification">
        🤖 <strong>Intelligent Q&A System</strong><br>
        Get instant answers about trade policies, HTS codes, and duty calculations.
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced knowledge base
    knowledge_base = {
        "gsp": "The Generalized System of Preferences (GSP) is a U.S. trade preference program designed to promote economic development by allowing duty-free entry for thousands of products from designated developing countries.",
        "usmca": "The United States-Mexico-Canada Agreement (USMCA) replaced NAFTA and provides preferential tariff treatment for qualifying goods between the US, Mexico, and Canada.",
        "hts": "The Harmonized Tariff Schedule (HTS) is a standardized numerical method of classifying traded products used by customs authorities around the world.",
        "duty": "Import duties are taxes imposed by customs authorities on goods when they are transported across international borders.",
        "cif": "CIF (Cost, Insurance, and Freight) is the total cost of goods including the cost of the goods, insurance, and freight charges.",
        "fta": "Free Trade Agreements (FTAs) are treaties between countries that reduce or eliminate trade barriers between participating nations.",
        "batch processing": "Our batch processing feature allows you to calculate duties for multiple HTS codes simultaneously, with support for CSV/Excel import and comprehensive reporting.",
        "comparison tool": "The comparison tool helps you analyze duty rates across different countries and trade agreements to optimize your supply chain decisions."
    }
    
    # Chat interface
    if "smart_chat_history" not in st.session_state:
        st.session_state.smart_chat_history = []
    
    # Quick question buttons
    st.subheader("⚡ Quick Questions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("What is GSP?", key="q_gsp"):
            st.session_state.quick_question = "What is GSP?"
    
    with col2:
        if st.button("USMCA Benefits?", key="q_usmca"):
            st.session_state.quick_question = "Tell me about USMCA"
    
    with col3:
        if st.button("How to use batch?", key="q_batch"):
            st.session_state.quick_question = "How does batch processing work?"
    
    with col4:
        if st.button("Compare countries?", key="q_compare"):
            st.session_state.quick_question = "How to compare countries?"
    
    # Main chat input
    user_input = st.text_input("Ask your trade question:", 
                              placeholder="e.g., What are the benefits of USMCA?",
                              value=st.session_state.get('quick_question', ''))
    
    if st.session_state.get('quick_question'):
        st.session_state.quick_question = ''
    
    if st.button("💬 Ask Assistant", type="primary") and user_input:
        # Add to history
        st.session_state.smart_chat_history.append({
            "role": "user", 
            "message": user_input,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        # Generate response
        response = generate_smart_response(user_input, knowledge_base)
        
        st.session_state.smart_chat_history.append({
            "role": "assistant", 
            "message": response,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    
    # Display chat history
    if st.session_state.smart_chat_history:
        st.subheader("💬 Conversation")
        
        for chat in st.session_state.smart_chat_history[-10:]:  # Show last 10
            if chat["role"] == "user":
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; margin-left: 2rem;">
                    <strong>You ({chat['timestamp']}):</strong> {chat["message"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; margin-right: 2rem; border-left: 4px solid #667eea;">
                    <strong>🤖 Assistant ({chat['timestamp']}):</strong> {chat["message"]}
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Chat", key="clear_smart_chat"):
            st.session_state.smart_chat_history = []
            st.rerun()

def generate_smart_response(question, knowledge_base):
    """Generate intelligent responses"""
    question_lower = question.lower()
    
    # Check knowledge base
    for key, answer in knowledge_base.items():
        if key in question_lower:
            return answer
    
    # HTS code specific responses
    hts_database = get_hts_database()
    for hts_code, info in hts_database.items():
        if hts_code in question:
            return f"HTS Code {hts_code}: {info['description']} | Category: {info['category']} | Standard Rate: {info['duty_rate']*100:.2f}% | Special Programs: {', '.join(info['special_programs'])}"
    
    # Context-aware responses
    if "calculate" in question_lower:
        return "To calculate duties, use our Professional Calculator. You can choose from Standard, Advanced, Multi-Country, or Express modes for different levels of detail."
    
    if "batch" in question_lower:
        return "Our Batch Processing feature supports Manual Entry, CSV Upload, and Excel Import. You can process hundreds of items simultaneously with progress tracking and comprehensive reporting."
    
    if "compare" in question_lower:
        return "Use our Comparison Tool to analyze duty rates across countries. Choose from Country Comparison, HTS Code Analysis, Side-by-Side comparison, or Trend Analysis."
    
    if "country" in question_lower:
        return "Our system supports major trading partners including China, Germany, Japan, Mexico, Canada, Vietnam, India, and Brazil with specific duty rates and trade agreement preferences."
    
    # Default response
    return "I can help you with trade policies, HTS codes, duty calculations, batch processing, country comparisons, and more. Try asking about specific topics like 'GSP', 'USMCA', 'duty rates', or 'how to use batch processing'."

def render_advanced_analytics():
    st.header("📊 Advanced Trade Analytics")
    
    st.markdown("""
    <div class="notification">
        📈 <strong>Comprehensive Analytics Dashboard</strong><br>
        Deep insights into your trade data with advanced visualizations and trend analysis.
    </div>
    """, unsafe_allow_html=True)
    
    # Analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🌍 Geographic", "💰 Financial"])
    
    with tab1:
        render_analytics_overview()
    
    with tab2:
        render_trend_analysis_tab()
    
    with tab3:
        render_geographic_analysis_tab()
    
    with tab4:
        render_financial_analysis_tab()

def render_analytics_overview():
    st.subheader("📊 Analytics Overview")
    
    # Generate sample analytics data
    if not st.session_state.calculations_history:
        # Create sample data for demonstration
        sample_data = generate_sample_analytics_data()
    else:
        sample_data = st.session_state.calculations_history
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Calculations", len(sample_data))
    with col2:
        avg_duty = 8.5  # Sample average
        st.metric("Avg Duty Rate", f"{avg_duty:.1f}%")
    with col3:
        total_value = sum([10000 for _ in sample_data])  # Sample values
        st.metric("Total Value", f"${total_value:,.0f}")
    with col4:
        savings = total_value * 0.05  # 5% estimated savings
        st.metric("Est. Savings", f"${savings:,.0f}")
    
    # Activity over time
    if len(sample_data) > 0:
        st.subheader("📈 Activity Timeline")
        
        # Create timeline data
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        activity_counts = np.random.poisson(5, 30)  # Sample activity
        
        timeline_data = pd.DataFrame({
            'Date': dates,
            'Calculations': activity_counts,
            'Cumulative': np.cumsum(activity_counts)
        })
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=timeline_data['Date'], y=timeline_data['Calculations'], name="Daily"),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=timeline_data['Date'], y=timeline_data['Cumulative'], name="Cumulative"),
            secondary_y=True,
        )
        
        fig.update_layout(title="Daily vs Cumulative Activity")
        fig.update_yaxes(title_text="Daily Calculations", secondary_y=False)
        fig.update_yaxes(title_text="Cumulative Total", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)

def generate_sample_analytics_data():
    """Generate sample data for analytics demonstration"""
    countries = ["China", "Germany", "Japan", "Mexico", "Canada"]
    hts_codes = list(get_hts_database().keys())
    
    sample_data = []
    for i in range(50):  # 50 sample calculations
        sample_data.append({
            "timestamp": (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S"),
            "hts_code": np.random.choice(hts_codes),
            "country_origin": np.random.choice(countries),
            "cif_value": np.random.uniform(1000, 50000),
            "duty_rate": np.random.uniform(0, 0.25),
            "duty_amount": np.random.uniform(0, 5000),
            "total_landed_cost": np.random.uniform(1200, 60000)
        })
    
    return sample_data

def render_express_calc():
    st.subheader("⚡ Express Calculator")
    
    st.info("🚀 Quick calculation with minimal inputs for fast results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        hts_codes = list(get_hts_database().keys())
        hts_code = st.selectbox("HTS Code", hts_codes, key="express_hts")
        value = st.number_input("Total Value ($)", value=10000.0, min_value=0.0, key="express_value")
    
    with col2:
        countries = ["China", "Germany", "Japan", "Mexico", "Canada"]
        country = st.selectbox("Origin Country", countries, key="express_country")
        
        if st.button("⚡ Quick Calculate", type="primary", key="express_calc_btn"):
            hts_database = get_hts_database()
            hts_info = hts_database[hts_code]
            
            duty_rate = hts_info['origin_rates'].get(country, hts_info['duty_rate'])
            duty_amount = value * duty_rate
            total_cost = value + duty_amount + 200  # Add standard fees
            
            st.success(f"⚡ **Quick Result**: ${total_cost:,.2f} total cost (${duty_amount:,.2f} duty at {duty_rate*100:.2f}%)")

def render_csv_batch():
    st.subheader("📄 CSV Batch Upload")
    
    # Show sample format
    st.info("""
    **Required CSV Format:**
    ```
    hts_code,product_cost,country_origin,quantity
    0101.30.00.00,10000,China,1
    0102.21.00.00,15000,Mexico,2
    ```
    """)
    
    uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="csv_batch_upload")
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} items from CSV")
            st.dataframe(df.head(), use_container_width=True)
            
            if st.button("🔄 Process CSV Batch", type="primary", key="process_csv_batch"):
                # Convert to batch items
                batch_items = df.to_dict('records')
                for i, item in enumerate(batch_items):
                    item['id'] = i + 1
                    item['status'] = 'Pending'
                
                st.session_state.batch_items = batch_items
                process_batch_items()
                
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")

def render_excel_batch():
    st.subheader("📊 Excel Batch Import")
    
    st.info("Upload Excel file with HTS data. First sheet will be used automatically.")
    
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"], key="excel_batch_upload")
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"Loaded {len(df)} items from Excel")
            st.dataframe(df.head(), use_container_width=True)
            
            if st.button("🔄 Process Excel Batch", type="primary", key="process_excel_batch"):
                batch_items = df.to_dict('records')
                for i, item in enumerate(batch_items):
                    item['id'] = i + 1
                    item['status'] = 'Pending'
                
                st.session_state.batch_items = batch_items
                process_batch_items()
                
        except Exception as e:
            st.error(f"Error reading Excel: {str(e)}")

def render_quick_batch():
    st.subheader("🔄 Quick Batch Generator")
    
    st.info("🎯 Generate sample batch data for testing and demonstration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_items = st.number_input("Number of Items", value=5, min_value=1, max_value=50)
    
    with col2:
        countries = ["China", "Germany", "Japan", "Mexico", "Canada"]
        default_country = st.selectbox("Default Country", countries)
    
    with col3:
        if st.button("🎲 Generate Sample Batch", type="primary", key="generate_sample_batch"):
            generate_sample_batch(num_items, default_country)

def generate_sample_batch(num_items, default_country):
    """Generate sample batch data"""
    hts_codes = list(get_hts_database().keys())
    hts_database = get_hts_database()
    
    batch_items = []
    for i in range(num_items):
        hts_code = np.random.choice(hts_codes)
        hts_info = hts_database[hts_code]
        
        item = {
            "id": i + 1,
            "hts_code": hts_code,
            "product_cost": np.random.uniform(500, hts_info['avg_value'] * 2),
            "country": default_country,
            "quantity": np.random.randint(1, 10),
            "status": "Generated"
        }
        batch_items.append(item)
    
    st.session_state.batch_items = batch_items
    st.success(f"Generated {num_items} sample items!")
    
    df_batch = pd.DataFrame(batch_items)
    st.dataframe(df_batch, use_container_width=True, hide_index=True)

def preview_batch_results():
    """Preview batch processing results without full calculation"""
    if not st.session_state.batch_items:
        st.warning("No items to preview")
        return
    
    st.subheader("👀 Batch Preview")
    
    hts_database = get_hts_database()
    preview_data = []
    
    for item in st.session_state.batch_items[:10]:  # Preview first 10
        if item['hts_code'] in hts_database:
            hts_info = hts_database[item['hts_code']]
            duty_rate = hts_info['origin_rates'].get(item['country'], hts_info['duty_rate'])
            
            preview_data.append({
                "HTS Code": item['hts_code'],
                "Description": hts_info['description'][:40] + "...",
                "Country": item['country'],
                "Est. Duty Rate": f"{duty_rate*100:.2f}%",
                "Product Cost": f"${item['product_cost']:,.2f}",
                "Status": "Ready"
            })
    
    df_preview = pd.DataFrame(preview_data)
    st.dataframe(df_preview, use_container_width=True, hide_index=True)
    
    if len(st.session_state.batch_items) > 10:
        st.info(f"Showing preview of first 10 items. Total items: {len(st.session_state.batch_items)}")

def export_batch_template():
    """Export batch template for users"""
    template_data = {
        "hts_code": ["0101.30.00.00", "0102.21.00.00", "0201.10.00.00"],
        "product_cost": [10000, 15000, 8000],
        "country_origin": ["China", "Mexico", "Germany"],
        "quantity": [1, 2, 500]
    }
    
    df_template = pd.DataFrame(template_data)
    
    st.download_button(
        "📥 Download Template CSV",
        data=df_template.to_csv(index=False),
        file_name="hts_batch_template.csv",
        mime="text/csv",
        key="download_batch_template"
    )

def render_trend_analysis_tab():
    """Render trend analysis tab"""
    st.subheader("📈 Trend Analysis")
    
    # Sample trend data
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    trend_data = {
        'Date': dates,
        'Average_Duty_Rate': np.random.uniform(0.05, 0.15, 90),
        'Total_Volume': np.random.uniform(1000, 5000, 90),
        'Cost_Savings': np.random.uniform(500, 2000, 90)
    }
    
    df_trends = pd.DataFrame(trend_data)
    
    # Trend charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_duty = px.line(df_trends, x='Date', y='Average_Duty_Rate', 
                          title="Average Duty Rate Trends")
        st.plotly_chart(fig_duty, use_container_width=True)
    
    with col2:
        fig_volume = px.line(df_trends, x='Date', y='Total_Volume', 
                            title="Import Volume Trends")
        st.plotly_chart(fig_volume, use_container_width=True)
    
    # Trend insights
    st.markdown("""
    **📊 Key Insights:**
    - Duty rates have been stable over the past quarter
    - Import volumes show seasonal variation
    - Cost savings opportunities identified in Q2
    """)

def render_geographic_analysis_tab():
    """Render geographic analysis tab"""
    st.subheader("🌍 Geographic Analysis")
    
    # Sample geographic data
    countries = ["China", "Germany", "Japan", "Mexico", "Canada", "Vietnam", "India", "Brazil"]
    geo_data = {
        'Country': countries,
        'Import_Volume': np.random.uniform(1000, 10000, len(countries)),
        'Average_Duty': np.random.uniform(0.0, 0.25, len(countries)),
        'Trade_Value': np.random.uniform(50000, 500000, len(countries))
    }
    
    df_geo = pd.DataFrame(geo_data)
    
    # Geographic visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        fig_map = px.bar(df_geo, x='Country', y='Import_Volume', 
                        title="Import Volume by Country",
                        color='Average_Duty', color_continuous_scale="Viridis")
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        fig_duty_map = px.scatter(df_geo, x='Trade_Value', y='Average_Duty', 
                                 size='Import_Volume', hover_name='Country',
                                 title="Trade Value vs Duty Rate")
        st.plotly_chart(fig_duty_map, use_container_width=True)
    
    # Geographic summary
    st.dataframe(df_geo, use_container_width=True, hide_index=True)

def render_financial_analysis_tab():
    """Render financial analysis tab"""
    st.subheader("💰 Financial Analysis")
    
    # Financial metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trade Value", "$2.5M", "+15%")
    with col2:
        st.metric("Total Duty Paid", "$125K", "-8%")
    with col3:
        st.metric("Cost Savings", "$85K", "+22%")
    with col4:
        st.metric("ROI", "18.5%", "+3.2%")
    
    # Financial charts
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    costs = [15000, 18000, 22000, 19000, 25000, 23000]
    savings = [2000, 2500, 3200, 2800, 4100, 3800]
    
    fig_financial = go.Figure()
    fig_financial.add_trace(go.Bar(name='Total Costs', x=months, y=costs))
    fig_financial.add_trace(go.Bar(name='Savings', x=months, y=savings))
    fig_financial.update_layout(title="Monthly Cost Analysis", barmode='group')
    st.plotly_chart(fig_financial, use_container_width=True)
    
    # ROI analysis
    st.subheader("📊 ROI Analysis")
    roi_data = {
        'Category': ['Electronics', 'Textiles', 'Food', 'Machinery'],
        'Investment': [50000, 30000, 20000, 80000],
        'Savings': [12000, 8500, 4200, 18000],
        'ROI (%)': [24, 28.3, 21, 22.5]
    }
    
    df_roi = pd.DataFrame(roi_data)
    st.dataframe(df_roi, use_container_width=True, hide_index=True)

def render_hts_explorer():
    """Render HTS code explorer"""
    st.header("🔍 HTS Code Explorer")
    
    st.markdown("""
    <div class="notification">
        🔍 <strong>Advanced HTS Code Explorer</strong><br>
        Search, browse, and analyze HTS codes with detailed information.
    </div>
    """, unsafe_allow_html=True)
    
    # Search functionality
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search HTS Codes", placeholder="Enter keyword or HTS code...")
    
    with col2:
        category_filter = st.selectbox("Filter by Category", 
                                      ["All", "Live Animals", "Electronics", "Textiles", "Food"])
    
    # HTS database display
    hts_database = get_hts_database()
    
    # Convert to DataFrame for easier filtering
    hts_data = []
    for code, info in hts_database.items():
        hts_data.append({
            "HTS Code": code,
            "Description": info['description'],
            "Category": info['category'],
            "Duty Rate": f"{info['duty_rate']*100:.2f}%",
            "Units": info['units'],
            "Special Programs": ', '.join(info['special_programs']),
            "Avg Value": f"${info['avg_value']:,.2f}"
        })
    
    df_hts = pd.DataFrame(hts_data)
    
    # Apply filters
    if search_term:
        mask = df_hts.apply(lambda x: search_term.lower() in x.astype(str).str.lower().to_string(), axis=1)
        df_hts = df_hts[mask]
    
    if category_filter != "All":
        df_hts = df_hts[df_hts["Category"] == category_filter]
    
    st.dataframe(df_hts, use_container_width=True, hide_index=True)
    
    # HTS Code details
    if len(df_hts) > 0:
        st.subheader("📊 Category Distribution")
        category_counts = df_hts["Category"].value_counts()
        
        fig_categories = px.pie(values=category_counts.values, names=category_counts.index,
                               title="HTS Codes by Category")
        st.plotly_chart(fig_categories, use_container_width=True)

def render_quick_tools():
    """Render quick tools"""
    st.header("⚡ Quick Tools Suite")
    
    # Tool selection
    tool = st.selectbox("Select Tool:", [
        "💱 Currency Converter",
        "⚖️ Unit Converter", 
        "📊 Quick Calculator",
        "📄 Report Generator"
    ])
    
    if tool == "💱 Currency Converter":
        render_currency_converter()
    elif tool == "⚖️ Unit Converter":
        render_unit_converter()
    elif tool == "📊 Quick Calculator":
        render_quick_calculator()
    else:
        render_report_generator()

def render_currency_converter():
    """Currency converter tool"""
    st.subheader("💱 Currency Converter")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        amount = st.number_input("Amount", value=1000.0, min_value=0.0)
    
    with col2:
        from_currency = st.selectbox("From", ["USD", "EUR", "GBP", "CAD", "JPY"])
    
    with col3:
        to_currency = st.selectbox("To", ["EUR", "USD", "GBP", "CAD", "JPY"])
    
    # Sample exchange rates (in real app, would fetch from API)
    rates = {
        "USD": {"EUR": 0.85, "GBP": 0.73, "CAD": 1.25, "JPY": 110},
        "EUR": {"USD": 1.18, "GBP": 0.86, "CAD": 1.47, "JPY": 130},
        "GBP": {"USD": 1.37, "EUR": 1.16, "CAD": 1.71, "JPY": 151},
    }
    
    if from_currency != to_currency:
        if from_currency in rates and to_currency in rates[from_currency]:
            rate = rates[from_currency][to_currency]
            converted = amount * rate
            st.success(f"{amount:,.2f} {from_currency} = {converted:,.2f} {to_currency}")
            st.info(f"Exchange rate: 1 {from_currency} = {rate} {to_currency}")

def render_unit_converter():
    """Unit converter tool"""
    st.subheader("⚖️ Unit Converter")
    
    conversion_type = st.selectbox("Conversion Type:", ["Weight", "Volume", "Length"])
    
    if conversion_type == "Weight":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            weight = st.number_input("Weight", value=1000.0, min_value=0.0)
        
        with col2:
            from_unit = st.selectbox("From Unit", ["kg", "lbs", "tons", "grams"])
        
        with col3:
            to_unit = st.selectbox("To Unit", ["lbs", "kg", "tons", "grams"])
        
        # Weight conversions
        weight_factors = {
            "kg": {"lbs": 2.205, "tons": 0.001, "grams": 1000},
            "lbs": {"kg": 0.453, "tons": 0.000453, "grams": 453.6},
            "tons": {"kg": 1000, "lbs": 2205, "grams": 1000000},
            "grams": {"kg": 0.001, "lbs": 0.0022, "tons": 0.000001}
        }
        
        if from_unit != to_unit and from_unit in weight_factors:
            if to_unit in weight_factors[from_unit]:
                factor = weight_factors[from_unit][to_unit]
                converted = weight * factor
                st.success(f"{weight:,.2f} {from_unit} = {converted:,.2f} {to_unit}")

def render_quick_calculator():
    """Quick calculator tool"""
    st.subheader("📊 Quick Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        value = st.number_input("Product Value ($)", value=10000.0, min_value=0.0)
        duty_rate = st.number_input("Duty Rate (%)", value=5.0, min_value=0.0, max_value=100.0)
    
    with col2:
        freight_rate = st.number_input("Freight Rate (%)", value=5.0, min_value=0.0)
        additional_fees = st.number_input("Additional Fees ($)", value=200.0, min_value=0.0)
    
    if st.button("⚡ Quick Calculate", type="primary"):
        freight = value * (freight_rate / 100)
        cif_value = value + freight + (value * 0.01)  # 1% insurance
        duty = cif_value * (duty_rate / 100)
        total = cif_value + duty + additional_fees
        
        st.success(f"**Total Landed Cost: ${total:,.2f}**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("CIF Value", f"${cif_value:,.2f}")
        with col2:
            st.metric("Duty Amount", f"${duty:,.2f}")
        with col3:
            st.metric("Total Fees", f"${additional_fees:,.2f}")
        with col4:
            st.metric("Savings vs Max", f"${total*0.1:,.2f}")

def render_report_generator():
    """Report generator tool"""
    st.subheader("📄 Report Generator")
    
    report_type = st.selectbox("Report Type:", [
        "Summary Report",
        "Detailed Analysis",
        "Cost Comparison",
        "Custom Report"
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        date_range = st.date_input("Report Period", value=[datetime.now().date()])
        include_charts = st.checkbox("Include Charts", value=True)
    
    with col2:
        format_type = st.selectbox("Format", ["PDF", "Excel", "Word", "PowerPoint"])
        include_data = st.checkbox("Include Raw Data", value=False)
    
    if st.button("📄 Generate Report", type="primary"):
        # Sample report generation
        report_content = f"""
HTS AI AGENT - {report_type.upper()}
{'='*50}

Report Period: {date_range}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY:
- Total Calculations: 125
- Average Duty Rate: 8.5%
- Total Savings: $12,500
- Efficiency Improvement: 300%

DETAILED ANALYSIS:
This report provides comprehensive insights into trade operations
and duty calculations performed during the specified period.

{'Charts and visualizations included' if include_charts else 'Text-only report'}
{'Raw data appendix included' if include_data else 'Summary data only'}

Format: {format_type}
Generated by HTS AI Agent Ultimate Pro
        """
        
        st.download_button(
            f"📥 Download {report_type}",
            data=report_content,
            file_name=f"hts_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_generated_report"
        )
        
        st.success(f"✅ {report_type} generated successfully!")

def render_trade_simulator():
    """Trade simulator"""
    st.header("🎯 Trade Simulator")
    
    st.markdown("""
    <div class="notification">
        🎯 <strong>Advanced Trade Simulator</strong><br>
        Model different trade scenarios and optimize your supply chain decisions.
    </div>
    """, unsafe_allow_html=True)
    
    # Simulator setup
    scenario_type = st.selectbox("Simulation Type:", [
        "🔄 Supply Chain Optimization",
        "📊 Cost-Benefit Analysis", 
        "🌍 Multi-Country Comparison",
        "📈 Risk Assessment"
    ])
    
    if scenario_type == "🔄 Supply Chain Optimization":
        render_supply_chain_sim()
    elif scenario_type == "📊 Cost-Benefit Analysis":
        render_cost_benefit_sim()
    elif scenario_type == "🌍 Multi-Country Comparison":
        render_multi_country_sim()
    else:
        render_risk_assessment_sim()

def render_supply_chain_sim():
    """Supply chain optimization simulator"""
    st.subheader("🔄 Supply Chain Optimization")
    
    # Input parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Product Parameters**")
        product_value = st.number_input("Product Value ($)", value=50000.0)
        annual_volume = st.number_input("Annual Volume", value=1000)
        
    with col2:
        st.markdown("**Supply Options**")
        suppliers = st.multiselect("Potential Suppliers", 
                                  ["China", "Germany", "Mexico", "Vietnam"], 
                                  default=["China", "Mexico"])
        
    with col3:
        st.markdown("**Constraints**")
        max_duty_rate = st.slider("Max Acceptable Duty Rate (%)", 0, 25, 10)
        quality_weight = st.slider("Quality Weight (%)", 0, 100, 30)
    
    if st.button("🔄 Optimize Supply Chain", type="primary"):
        # Simulation results
        results = []
        for supplier in suppliers:
            hts_database = get_hts_database()
            sample_hts = list(hts_database.keys())[0]  # Use first HTS for demo
            duty_rate = hts_database[sample_hts]['origin_rates'].get(supplier, 0.1)
            
            total_cost = product_value * (1 + duty_rate + 0.05)  # Add 5% logistics
            quality_score = np.random.uniform(0.7, 0.95)  # Random quality score
            risk_score = np.random.uniform(0.1, 0.3)  # Random risk score
            
            # Weighted score
            cost_score = 1 - (total_cost / max([product_value * 1.3 for _ in suppliers]))
            weighted_score = (cost_score * (100-quality_weight) + quality_score * quality_weight) / 100
            
            results.append({
                "Supplier": supplier,
                "Total Cost": f"${total_cost:,.2f}",
                "Duty Rate": f"{duty_rate*100:.1f}%",
                "Quality Score": f"{quality_score:.2f}",
                "Risk Level": f"{risk_score:.2f}",
                "Overall Score": f"{weighted_score:.3f}"
            })
        
        df_results = pd.DataFrame(results)
        st.dataframe(df_results, use_container_width=True, hide_index=True)
        
        # Recommendation
        best_supplier = max(results, key=lambda x: float(x["Overall Score"]))
        st.success(f"🏆 **Recommended Supplier: {best_supplier['Supplier']}** (Score: {best_supplier['Overall Score']})")

def render_cost_benefit_sim():
    """Cost-benefit analysis simulator"""
    st.subheader("📊 Cost-Benefit Analysis")
    st.info("🚧 Advanced cost-benefit modeling - Coming soon!")

def render_multi_country_sim():
    """Multi-country comparison simulator"""
    st.subheader("🌍 Multi-Country Comparison")
    st.info("🚧 Multi-country scenario modeling - Coming soon!")

def render_risk_assessment_sim():
    """Risk assessment simulator"""
    st.subheader("📈 Risk Assessment")
    st.info("🚧 Comprehensive risk analysis - Coming soon!")

def render_global_rates():
    """Global rates monitor"""
    st.header("🌍 Global Rates Monitor")
    
    st.markdown("""
    <div class="notification">
        🌍 <strong>Global Trade Rates Monitor</strong><br>
        Real-time monitoring of duty rates and trade agreements worldwide.
    </div>
    """, unsafe_allow_html=True)
    
    # Sample global data
    countries = ["USA", "China", "Germany", "Japan", "UK", "Canada", "Mexico", "France"]
    rates_data = {
        'Country': countries,
        'Avg_Duty_Rate': np.random.uniform(0.02, 0.20, len(countries)),
        'Trade_Volume': np.random.uniform(10, 100, len(countries)),
        'Last_Update': ['2024-01-10'] * len(countries)
    }
    
    df_global = pd.DataFrame(rates_data)
    
    # Global visualization
    fig_global = px.choropleth(df_global, 
                              locations='Country',
                              color='Avg_Duty_Rate',
                              hover_name='Country',
                              title="Global Duty Rates",
                              color_continuous_scale="Viridis")
    
    st.plotly_chart(fig_global, use_container_width=True)
    
    # Rates table
    st.subheader("📊 Current Rates")
    st.dataframe(df_global, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main() 