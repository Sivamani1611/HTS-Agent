import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="HTS AI Agent - Working Version",
    page_icon="🌐",
    layout="wide"
)

# Enhanced styling
st.markdown("""
<style>
    /* Import modern fonts */
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
    
    .calculation-result {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
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
    
    .info-box {
        background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌐 HTS AI Agent - Working Version</h1>
        <p>Advanced Trade Intelligence & Duty Calculation Platform</p>
        <p style="font-size: 0.9em; opacity: 0.8;">Fixed all form and table display issues!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.header("🛠️ Navigation")
        page = st.selectbox("Choose a feature:", [
            "🏠 Dashboard", 
            "📊 Duty Calculator", 
            "💬 Simple Chat",
            "📈 Sample Data",
            "📊 Analytics"
        ])
    
    # Route to different pages
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "📊 Duty Calculator":
        render_calculator()
    elif page == "💬 Simple Chat":
        render_simple_chat()
    elif page == "📈 Sample Data":
        render_sample_data()
    else:
        render_analytics()

def render_dashboard():
    st.header("📊 Executive Dashboard")
    
    # Enhanced metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>125</h3>
            <p>Total Queries</p>
            <small>↗️ +12 this week</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>87</h3>
            <p>Duty Calculations</p>
            <small>↗️ +8 this week</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>8.5%</h3>
            <p>Avg Duty Rate</p>
            <small>↘️ -0.2% this month</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>$12.5K</h3>
            <p>Est. Savings</p>
            <small>↗️ +$2.1K this month</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent activity with working table display
    st.subheader("📋 Recent Activity")
    
    activity_data = [
        {"Time": "2 minutes ago", "Action": "Duty calculation", "Details": "HTS: 0101.30.00.00", "Result": "$10,600"},
        {"Time": "15 minutes ago", "Action": "Policy question", "Details": "What is GSP?", "Result": "Answered"},
        {"Time": "1 hour ago", "Action": "Duty calculation", "Details": "HTS: 0201.10.00.00", "Result": "$8,240"},
        {"Time": "2 hours ago", "Action": "Batch processing", "Details": "25 HTS codes", "Result": "Completed"},
    ]
    
    df_activity = pd.DataFrame(activity_data)
    st.dataframe(df_activity, use_container_width=True, hide_index=True)

def render_calculator():
    st.header("📊 Advanced Duty Calculator")
    
    st.markdown("""
    <div class="info-box">
        💡 <strong>Professional Duty Calculator</strong><br>
        Enter your shipment details below for accurate duty calculations with comprehensive breakdown.
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for calculation results
    if 'calculation_done' not in st.session_state:
        st.session_state.calculation_done = False
    
    # Input form (WITHOUT download buttons inside!)
    st.subheader("📝 Enter Calculation Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📦 Product Information")
        hts_code = st.text_input("HTS Code", value="0101.30.00.00", placeholder="XXXX.XX.XX.XX")
        product_cost = st.number_input("Product Cost ($)", value=10000.0, min_value=0.0, step=100.0)
        freight = st.number_input("Freight ($)", value=500.0, min_value=0.0, step=50.0)
        insurance = st.number_input("Insurance ($)", value=100.0, min_value=0.0, step=10.0)
    
    with col2:
        st.markdown("#### 📏 Shipment Details")
        weight = st.number_input("Weight (kg)", value=500.0, min_value=0.0, step=10.0)
        quantity = st.number_input("Quantity", value=1, min_value=1, step=1)
        country_origin = st.selectbox("Country of Origin", ["China", "Germany", "Japan", "Mexico", "Canada", "Other"])
        
        st.markdown("#### 💰 Additional Costs")
        handling_fee = st.number_input("Handling Fee ($)", value=50.0, min_value=0.0)
        broker_fee = st.number_input("Broker Fee ($)", value=150.0, min_value=0.0)
    
    # Calculate button (outside form!)
    if st.button("🔄 Calculate Total Landed Cost", type="primary", key="calc_button"):
        # Enhanced calculation with more details
        cif_value = product_cost + freight + insurance
        
        # Sample duty rates database
        duty_rates = {
            "0101.30.00.00": {"rate": 0.0, "description": "Live asses - Free", "category": "Live Animals"},
            "0102.21.00.00": {"rate": 0.025, "description": "Live cattle, purebred - 2.5%", "category": "Live Animals"},
            "0201.10.00.00": {"rate": 0.044, "description": "Beef carcasses - 4.4¢/kg", "category": "Meat Products"},
            "0301.11.00.00": {"rate": 0.0, "description": "Ornamental fish - Free", "category": "Fish"},
            "0401.10.00.00": {"rate": 0.038, "description": "Milk ≤1% fat - 3.8¢/liter", "category": "Dairy"},
            "default": {"rate": 0.05, "description": "General rate - 5%", "category": "General"}
        }
        
        duty_info = duty_rates.get(hts_code, duty_rates["default"])
        duty_rate = duty_info["rate"]
        duty_amount = cif_value * duty_rate
        total_additional = handling_fee + broker_fee
        landed_cost = cif_value + duty_amount + total_additional
        
        # Store results in session state
        st.session_state.calc_results = {
            "hts_code": hts_code,
            "duty_info": duty_info,
            "product_cost": product_cost,
            "freight": freight,
            "insurance": insurance,
            "cif_value": cif_value,
            "duty_rate": duty_rate,
            "duty_amount": duty_amount,
            "handling_fee": handling_fee,
            "broker_fee": broker_fee,
            "total_additional": total_additional,
            "landed_cost": landed_cost,
            "calculation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.calculation_done = True
    
    # Display results if calculation is done
    if st.session_state.calculation_done and 'calc_results' in st.session_state:
        results = st.session_state.calc_results
        
        # Display enhanced results
        st.markdown("""
        <div class="calculation-result">
            <h3>✅ Calculation Complete!</h3>
            <p>Your comprehensive duty calculation is ready with detailed breakdown.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("CIF Value", f"${results['cif_value']:,.2f}")
        with col2:
            st.metric("Duty Amount", f"${results['duty_amount']:,.2f}", f"{results['duty_rate']*100:.1f}%")
        with col3:
            st.metric("Additional Fees", f"${results['total_additional']:,.2f}")
        with col4:
            st.metric("Landed Cost", f"${results['landed_cost']:,.2f}")
        
        # Detailed breakdown table
        st.subheader("📋 Detailed Cost Breakdown")
        
        # Create breakdown data with proper formatting
        breakdown_data = {
            "Cost Component": [
                "Product Cost", 
                "Freight", 
                "Insurance", 
                "CIF Value", 
                "Import Duties", 
                "Handling Fee", 
                "Broker Fee", 
                "TOTAL LANDED COST"
            ],
            "Amount (USD)": [
                f"${results['product_cost']:,.2f}",
                f"${results['freight']:,.2f}",
                f"${results['insurance']:,.2f}",
                f"${results['cif_value']:,.2f}",
                f"${results['duty_amount']:,.2f}",
                f"${results['handling_fee']:,.2f}",
                f"${results['broker_fee']:,.2f}",
                f"${results['landed_cost']:,.2f}"
            ],
            "Percentage of Total": [
                f"{(results['product_cost']/results['landed_cost'])*100:.1f}%",
                f"{(results['freight']/results['landed_cost'])*100:.1f}%",
                f"{(results['insurance']/results['landed_cost'])*100:.1f}%",
                f"{(results['cif_value']/results['landed_cost'])*100:.1f}%",
                f"{(results['duty_amount']/results['landed_cost'])*100:.1f}%",
                f"{(results['handling_fee']/results['landed_cost'])*100:.1f}%",
                f"{(results['broker_fee']/results['landed_cost'])*100:.1f}%",
                "100.0%"
            ],
            "Notes": [
                "Base product value",
                "Shipping costs",
                "Insurance coverage",
                "Cost + Insurance + Freight",
                f"Rate: {results['duty_rate']*100:.1f}%",
                "Port handling",
                "Customs broker",
                "Final import cost"
            ]
        }
        
        df_breakdown = pd.DataFrame(breakdown_data)
        
        # Display with enhanced styling and proper column configuration
        st.dataframe(
            df_breakdown,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Cost Component": st.column_config.TextColumn("Cost Component", width="medium"),
                "Amount (USD)": st.column_config.TextColumn("Amount (USD)", width="small"),
                "Percentage of Total": st.column_config.TextColumn("% of Total", width="small"),
                "Notes": st.column_config.TextColumn("Notes", width="medium")
            }
        )
        
        # Store for downloads
        st.session_state.breakdown_df = df_breakdown
        
        # Visualization
        if st.checkbox("📊 Show Cost Visualization"):
            # Create pie chart
            labels = ['Product Cost', 'Freight', 'Insurance', 'Duties', 'Additional Fees']
            values = [results['product_cost'], results['freight'], results['insurance'], 
                     results['duty_amount'], results['total_additional']]
            colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            fig.update_traces(hoverinfo='label+percent', textinfo='value', 
                            textfont_size=12, marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))
            fig.update_layout(title="Cost Distribution", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)
        
        # Additional information
        st.subheader("ℹ️ HTS Code Information")
        st.info(f"**{results['hts_code']}**: {results['duty_info']['description']} | Category: {results['duty_info']['category']}")
        
        # DOWNLOAD BUTTONS - OUTSIDE ANY FORM!
        st.subheader("💾 Export Results")
        
        # Prepare export data
        export_data = {
            "calculation_date": results['calculation_date'],
            "hts_code": results['hts_code'],
            "product_cost": results['product_cost'],
            "freight": results['freight'],
            "insurance": results['insurance'],
            "cif_value": results['cif_value'],
            "duty_rate": results['duty_rate'],
            "duty_amount": results['duty_amount'],
            "handling_fee": results['handling_fee'],
            "broker_fee": results['broker_fee'],
            "total_additional": results['total_additional'],
            "landed_cost": results['landed_cost'],
            "breakdown": breakdown_data
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"duty_calculation_{results['hts_code'].replace('.', '')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                key="download_json_working"
            )
        with col2:
            csv_data = df_breakdown.to_csv(index=False)
            st.download_button(
                "📥 Download CSV", 
                data=csv_data,
                file_name=f"duty_calculation_{results['hts_code'].replace('.', '')}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_csv_working"
            )
    
    # Clear results button
    if st.session_state.calculation_done:
        if st.button("🗑️ Clear Results", key="clear_results"):
            st.session_state.calculation_done = False
            if 'calc_results' in st.session_state:
                del st.session_state.calc_results
            if 'breakdown_df' in st.session_state:
                del st.session_state.breakdown_df
            st.rerun()

def render_simple_chat():
    st.header("💬 Simple Trade Assistant")
    
    st.markdown("""
    <div class="info-box">
        🤖 <strong>Trade Policy Assistant</strong><br>
        Ask questions about trade policies, HTS codes, or get quick calculations.
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Sample knowledge base
    knowledge_base = {
        "gsp": "The Generalized System of Preferences (GSP) is a U.S. trade preference program designed to promote economic development by allowing duty-free entry for thousands of products from designated developing countries.",
        "generalized system of preferences": "The Generalized System of Preferences (GSP) is a U.S. trade preference program designed to promote economic development by allowing duty-free entry for thousands of products from designated developing countries.",
        "hts": "The Harmonized Tariff Schedule (HTS) is a standardized numerical method of classifying traded products used by customs authorities around the world.",
        "duty": "Import duties are taxes imposed by customs authorities on goods when they are transported across international borders.",
        "cif": "CIF (Cost, Insurance, and Freight) is the total cost of goods including the cost of the goods, insurance, and freight charges.",
        "nafta": "NAFTA (now USMCA) provides preferential tariff treatment for qualifying goods originating in Canada, Mexico, and the United States.",
        "usmca": "The United States-Mexico-Canada Agreement (USMCA) replaced NAFTA and provides preferential tariff treatment for qualifying goods.",
        "fta": "Free Trade Agreements (FTAs) are treaties between countries that reduce or eliminate trade barriers between participating nations."
    }
    
    # Chat interface
    user_input = st.text_input("Ask a question about trade policies or HTS codes:", 
                               placeholder="e.g., What is GSP? or Tell me about HTS code 0101.30.00.00")
    
    if st.button("💬 Send", type="primary") and user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        
        # Simple response logic
        user_input_lower = user_input.lower()
        response = "I'm sorry, I don't have specific information about that. Please try asking about GSP, HTS codes, duties, CIF, NAFTA/USMCA, or FTA."
        
        # Check knowledge base
        for key, value in knowledge_base.items():
            if key in user_input_lower:
                response = value
                break
        
        # HTS code specific responses
        if "0101.30.00.00" in user_input:
            response = "HTS Code 0101.30.00.00 refers to 'Live asses' and has a duty rate of 'Free' under the general rate."
        elif "0102.21.00.00" in user_input:
            response = "HTS Code 0102.21.00.00 refers to 'Live cattle, purebred breeding animals' with a duty rate of 2.5%."
        elif "calculate" in user_input_lower and any(char.isdigit() for char in user_input):
            response = "To calculate duties, please use the Duty Calculator page where you can enter all the required details for accurate calculations."
        
        # Add bot response to history
        st.session_state.chat_history.append({"role": "assistant", "message": response})
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("💬 Conversation History")
        
        for i, chat in enumerate(st.session_state.chat_history):
            if chat["role"] == "user":
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <strong>You:</strong> {chat["message"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #667eea;">
                    <strong>🤖 Assistant:</strong> {chat["message"]}
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

def render_sample_data():
    st.header("📈 Sample HTS Database")
    
    # Enhanced sample data
    sample_data = [
        {"HTS Code": "0101.30.00.00", "Description": "Live asses", "Duty Rate": "Free", "Category": "Live Animals", "Units": "Number", "Special Program": "GSP Eligible"},
        {"HTS Code": "0102.21.00.00", "Description": "Live cattle, purebred breeding", "Duty Rate": "2.5%", "Category": "Live Animals", "Units": "Number", "Special Program": "USMCA Eligible"},
        {"HTS Code": "0201.10.00.00", "Description": "Beef carcasses and half-carcasses, fresh or chilled", "Duty Rate": "4.4¢/kg", "Category": "Meat", "Units": "kg", "Special Program": "Subject to TRQ"},
        {"HTS Code": "0301.11.00.00", "Description": "Ornamental fish", "Duty Rate": "Free", "Category": "Fish", "Units": "Number", "Special Program": "GSP Eligible"},
        {"HTS Code": "0401.10.00.00", "Description": "Milk, not concentrated, not sweetened, fat ≤ 1%", "Duty Rate": "3.8¢/liter", "Category": "Dairy", "Units": "Liter", "Special Program": "USMCA Eligible"}
    ]
    
    df = pd.DataFrame(sample_data)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox("Filter by Category:", ["All"] + list(df["Category"].unique()))
    with col2:
        duty_filter = st.selectbox("Filter by Duty Type:", ["All", "Free", "Percentage", "Weight-based", "Unit-based"])
    with col3:
        program_filter = st.selectbox("Filter by Special Program:", ["All"] + list(df["Special Program"].unique()))
    
    # Apply filters
    filtered_df = df.copy()
    
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]
    
    if duty_filter != "All":
        if duty_filter == "Free":
            filtered_df = filtered_df[filtered_df["Duty Rate"] == "Free"]
        elif duty_filter == "Percentage":
            filtered_df = filtered_df[filtered_df["Duty Rate"].str.contains("%", na=False)]
        elif duty_filter == "Weight-based":
            filtered_df = filtered_df[filtered_df["Duty Rate"].str.contains("¢/kg", na=False)]
        elif duty_filter == "Unit-based":
            filtered_df = filtered_df[filtered_df["Duty Rate"].str.contains("¢/liter", na=False)]
    
    if program_filter != "All":
        filtered_df = filtered_df[filtered_df["Special Program"] == program_filter]
    
    st.subheader("🎯 HTS Code Database")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

def render_analytics():
    st.header("📊 Trade Analytics Dashboard")
    
    # Sample analytics data
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    query_data = {
        'Date': dates,
        'Queries': [15, 18, 22, 19, 25, 30, 28, 32, 29, 35, 38, 33, 40, 42, 38, 45, 48, 44, 50, 52, 49, 55, 58, 53, 60, 62, 58, 65, 68, 63],
        'Calculations': [8, 10, 12, 11, 14, 16, 15, 18, 16, 19, 21, 18, 22, 24, 21, 25, 27, 24, 28, 29, 27, 31, 33, 30, 34, 35, 33, 37, 39, 36]
    }
    
    df_analytics = pd.DataFrame(query_data)
    
    # Usage trends
    st.subheader("📈 Usage Trends")
    
    fig_line = px.line(df_analytics, x='Date', y=['Queries', 'Calculations'], 
                       title="Daily Platform Usage",
                       labels={'value': 'Count', 'variable': 'Type'})
    fig_line.update_layout(title_x=0.5)
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Category distribution
    st.subheader("📊 Popular Categories")
    
    category_data = {
        'Category': ['Live Animals', 'Meat Products', 'Dairy', 'Vegetables', 'Fish', 'Coffee', 'Nuts'],
        'Queries': [25, 18, 15, 12, 10, 8, 6]
    }
    
    fig_bar = px.bar(category_data, x='Category', y='Queries', 
                     title="Queries by Product Category",
                     color='Queries', color_continuous_scale="Viridis")
    fig_bar.update_layout(title_x=0.5)
    st.plotly_chart(fig_bar, use_container_width=True)

if __name__ == "__main__":
    main() 