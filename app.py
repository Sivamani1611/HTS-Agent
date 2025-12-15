import streamlit as st
import pandas as pd
import sys
import os
import json
from datetime import datetime
import pdfkit
from io import BytesIO
import base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.tariff_bot import TariffBot
from tools.invoice_parser import InvoiceParser
from tools.export_handler import ExportHandler
from tools.memory_handler import MemoryHandler

st.set_page_config(
    page_title="HTS AI Agent",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'memory' not in st.session_state:
    st.session_state.memory = MemoryHandler()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

@st.cache_resource
def load_bot():
    return TariffBot()

def main():
    st.title("🌐 HTS AI Agent - Advanced Trade Assistant")
    st.markdown("### Your Comprehensive Tool for Trade Policies and Duty Calculations")
    
    bot = load_bot()
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Tools & Features")
        
        # File Upload Section
        st.subheader("📄 Document Upload")
        uploaded_file = st.file_uploader(
            "Upload Invoice/Product Details",
            type=['csv', 'xlsx', 'pdf', 'json'],
            help="Upload invoice or product details for automated parsing"
        )
        
        if uploaded_file:
            with st.spinner("Parsing document..."):
                parser = InvoiceParser()
                parsed_data = parser.parse_file(uploaded_file)
                if parsed_data:
                    st.success("✅ Document parsed successfully!")
                    st.json(parsed_data)
                    if st.button("Use for Calculation"):
                        st.session_state.parsed_data = parsed_data
        
        st.divider()
        
        # Query History
        st.subheader("📝 Query History")
        history = st.session_state.memory.get_recent_queries(5)
        for i, query in enumerate(history):
            if st.button(f"🕐 {query['timestamp'][:16]}: {query['query'][:30]}...", key=f"hist_{i}"):
                st.session_state.rerun_query = query['query']
        
        st.divider()
        
        # Settings
        st.subheader("⚙️ Settings")
        include_vat = st.checkbox("Include VAT Calculation", value=True)
        vat_rate = st.number_input("VAT Rate (%)", value=20.0, min_value=0.0, max_value=30.0)
        include_shipping = st.checkbox("Include Additional Shipping Fees", value=True)
        st.session_state.settings = {
            'include_vat': include_vat,
            'vat_rate': vat_rate,
            'include_shipping': include_shipping
        }
    
    # Main Interface Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📊 Duty Calculator", "📈 Batch Processing", "📑 Reports"])
    
    with tab1:
        render_chat_interface(bot)
    
    with tab2:
        render_duty_calculator(bot)
    
    with tab3:
        render_batch_processing(bot)
    
    with tab4:
        render_reports()

def render_chat_interface(bot):
    st.header("Interactive Chat")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and isinstance(message["content"], dict):
                if "duties" in message["content"]:
                    display_duty_result(message["content"])
                else:
                    st.markdown(message["content"].get("answer", str(message["content"])))
            else:
                st.markdown(message["content"])
    
    # Check for rerun query
    if hasattr(st.session_state, 'rerun_query'):
        query = st.session_state.rerun_query
        del st.session_state.rerun_query
    else:
        query = st.chat_input("Ask about trade policies or calculate duties...")
    
    if query:
        # Add to chat history
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        with st.chat_message("user"):
            st.markdown(query)
        
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                # Save to memory
                st.session_state.memory.add_query(query)
                
                # Process query
                response = bot.process_query(query)
                
                # Display response
                if isinstance(response, dict):
                    if "duties" in response:
                        display_duty_result(response)
                        # Add export buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            excel_data = ExportHandler.to_excel(response)
                            st.download_button(
                                "📥 Download Excel",
                                data=excel_data,
                                file_name=f"duty_calculation_{response['HTS Code'].replace('.', '')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        with col2:
                            pdf_data = ExportHandler.to_pdf(response)
                            st.download_button(
                                "📥 Download PDF",
                                data=pdf_data,
                                file_name=f"duty_calculation_{response['HTS Code'].replace('.', '')}.pdf",
                                mime="application/pdf"
                            )
                    else:
                        st.markdown(response.get("answer", str(response)))
                else:
                    st.markdown(str(response))
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})

def render_duty_calculator(bot):
    st.header("Advanced Duty Calculator")
    
    # Check if we have parsed data
    if hasattr(st.session_state, 'parsed_data'):
        st.info("Using data from uploaded document")
        data = st.session_state.parsed_data
    else:
        data = {}
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hts_code = st.text_input("HTS Code", value=data.get('hts_code', "0101.30.00.00"))
        product_cost = st.number_input("Product Cost ($)", value=float(data.get('product_cost', 10000)), min_value=0.0)
        freight = st.number_input("Freight ($)", value=float(data.get('freight', 500)), min_value=0.0)
    
    with col2:
        insurance = st.number_input("Insurance ($)", value=float(data.get('insurance', 100)), min_value=0.0)
        unit_weight = st.number_input("Unit Weight (kg)", value=float(data.get('unit_weight', 500)), min_value=0.0)
        quantity = st.number_input("Quantity", value=int(data.get('quantity', 5)), min_value=1)
    
    with col3:
        st.subheader("Additional Costs")
        handling_fee = st.number_input("Handling Fee ($)", value=50.0, min_value=0.0)
        customs_broker_fee = st.number_input("Customs Broker Fee ($)", value=150.0, min_value=0.0)
        
    if st.button("Calculate Total Costs", type="primary"):
        with st.spinner("Calculating..."):
            # Basic duty calculation
            result = bot.tariff_calculator.calculate_duty(
                hts_code=hts_code,
                product_cost=product_cost,
                freight=freight,
                insurance=insurance,
                unit_weight=unit_weight,
                quantity=quantity
            )
            
            if "error" not in result:
                # Add additional calculations
                result = add_comprehensive_calculations(
                    result, 
                    handling_fee, 
                    customs_broker_fee,
                    st.session_state.settings
                )
                
                # Display comprehensive results
                display_comprehensive_result(result)
                
                # Export options
                st.divider()
                col1, col2, col3 = st.columns(3)
                with col1:
                    excel_data = ExportHandler.to_excel(result)
                    st.download_button(
                        "📥 Export to Excel",
                        data=excel_data,
                        file_name=f"comprehensive_duty_{hts_code.replace('.', '')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                with col2:
                    pdf_data = ExportHandler.to_pdf(result)
                    st.download_button(
                        "📥 Export to PDF",
                        data=pdf_data,
                        file_name=f"comprehensive_duty_{hts_code.replace('.', '')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                with col3:
                    json_data = json.dumps(result, indent=2)
                    st.download_button(
                        "📥 Export to JSON",
                        data=json_data,
                        file_name=f"comprehensive_duty_{hts_code.replace('.', '')}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
            else:
                st.error(result["error"])

def render_batch_processing(bot):
    st.header("Batch HTS Processing")
    st.markdown("Process multiple HTS codes at once")
    
    # Template download
    template_df = pd.DataFrame({
        'HTS Code': ['0101.30.00.00', '0102.21.00.00'],
        'Product Cost': [10000, 5000],
        'Freight': [500, 250],
        'Insurance': [100, 50],
        'Unit Weight': [500, 300],
        'Quantity': [5, 2]
    })
    
    csv_template = template_df.to_csv(index=False)
    st.download_button(
        "📥 Download CSV Template",
        data=csv_template,
        file_name="hts_batch_template.csv",
        mime="text/csv"
    )
    
    # File upload for batch processing
    uploaded_batch = st.file_uploader("Upload CSV with multiple HTS codes", type=['csv'])
    
    if uploaded_batch:
        df = pd.read_csv(uploaded_batch)
        st.dataframe(df)
        
        if st.button("Process Batch", type="primary"):
            progress_bar = st.progress(0)
            results = []
            
            for idx, row in df.iterrows():
                progress_bar.progress((idx + 1) / len(df))
                
                result = bot.tariff_calculator.calculate_duty(
                    hts_code=row['HTS Code'],
                    product_cost=row['Product Cost'],
                    freight=row['Freight'],
                    insurance=row['Insurance'],
                    unit_weight=row['Unit Weight'],
                    quantity=row['Quantity']
                )
                
                if "error" not in result:
                    results.append({
                        'HTS Code': result['HTS Code'],
                        'Description': result['Description'],
                        'CIF Value': result['CIF Value'],
                        'Total Duty': result['Total Duty'],
                        'Landed Cost': result['Landed Cost']
                    })
                else:
                    results.append({
                        'HTS Code': row['HTS Code'],
                        'Error': result['error']
                    })
            
            # Display results
            results_df = pd.DataFrame(results)
            st.dataframe(results_df)
            
            # Export batch results
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Input Data', index=False)
                results_df.to_excel(writer, sheet_name='Results', index=False)
            
            excel_buffer.seek(0)
            
            st.download_button(
                "📥 Download Batch Results",
                data=excel_buffer,
                file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

def render_reports():
    st.header("Reports & Analytics")
    
    # Query statistics
    stats = st.session_state.memory.get_statistics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Queries", stats['total_queries'])
    with col2:
        st.metric("Policy Questions", stats['policy_queries'])
    with col3:
        st.metric("Duty Calculations", stats['duty_calculations'])
    
    # Recent calculations summary
    st.subheader("Recent Calculations Summary")
    recent_calcs = st.session_state.memory.get_recent_calculations(10)
    if recent_calcs:
        df = pd.DataFrame(recent_calcs)
        st.dataframe(df)
        
        # Generate summary report
        if st.button("Generate Summary Report"):
            report = generate_summary_report(recent_calcs)
            st.download_button(
                "📥 Download Summary Report",
                data=report,
                file_name=f"hts_summary_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )

def display_duty_result(result):
    """Display duty calculation results in a formatted way"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CIF Value", result.get("CIF Value", "N/A"))
    with col2:
        st.metric("Total Duty", result.get("Total Duty", "N/A"))
    with col3:
        st.metric("Landed Cost", result.get("Landed Cost", "N/A"))
    
    # Duty breakdown
    if "duties" in result:
        st.subheader("Duty Breakdown")
        for duty_type, duty_info in result["duties"].items():
            st.write(f"**{duty_type}**: {duty_info['rate']} = {duty_info['amount']}")

def display_comprehensive_result(result):
    """Display comprehensive calculation results"""
    st.success("✅ Calculation Complete")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CIF Value", result.get("CIF Value", "N/A"))
    with col2:
        st.metric("Total Duty", result.get("Total Duty", "N/A"))
    with col3:
        st.metric("VAT", result.get("VAT Amount", "$0.00"))
    with col4:
        st.metric("Final Total", result.get("Final Total Cost", "N/A"))
    
    # Detailed breakdown
    with st.expander("View Detailed Breakdown"):
        st.json(result)

def add_comprehensive_calculations(result, handling_fee, customs_broker_fee, settings):
    """Add VAT, shipping, and other calculations"""
    # Parse monetary values
    cif_value = float(result['CIF Value'].replace('$', '').replace(',', ''))
    total_duty = float(result['Total Duty'].replace('$', '').replace(',', ''))
    
    # Additional fees
    result['Handling Fee'] = f"${handling_fee:,.2f}"
    result['Customs Broker Fee'] = f"${customs_broker_fee:,.2f}"
    
    # Calculate VAT if enabled
    if settings['include_vat']:
        vat_base = cif_value + total_duty
        vat_amount = vat_base * (settings['vat_rate'] / 100)
        result['VAT Rate'] = f"{settings['vat_rate']}%"
        result['VAT Amount'] = f"${vat_amount:,.2f}"
    else:
        vat_amount = 0
    
    # Calculate final total
    final_total = cif_value + total_duty + handling_fee + customs_broker_fee + vat_amount
    result['Final Total Cost'] = f"${final_total:,.2f}"
    
    return result

def generate_summary_report(calculations):
    """Generate PDF summary report"""
    # This is a placeholder - you'd implement actual PDF generation
    return b"PDF Report Content"

if __name__ == "__main__":
    main()