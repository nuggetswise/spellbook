"""
Results display component for extracted obligations.
Shows obligations in an interactive table with filtering and sorting.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import plotly.express as px
import plotly.graph_objects as go

def render_obligations_table(obligations: List[Dict[str, Any]]) -> None:
    """
    Render obligations in an interactive table.
    
    Args:
        obligations: List of extracted obligations
    """
    if not obligations:
        st.warning("No obligations found in the contract.")
        return
    
    st.header("📋 Extracted Obligations")
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(obligations)
    
    # Add row numbers
    df.insert(0, 'ID', range(1, len(df) + 1))
    
    # Display summary metrics
    render_summary_metrics(df)
    
    # Display risk distribution chart
    render_risk_chart(df)
    
    # Filtering options
    filtered_df = render_filters(df)
    
    # Display the table
    render_interactive_table(filtered_df)
    
    # Export options
    render_export_options(filtered_df)

def render_summary_metrics(df: pd.DataFrame) -> None:
    """
    Render summary metrics for obligations.
    
    Args:
        df: Obligations DataFrame
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Obligations", len(df))
    
    with col2:
        high_risk = len(df[df['riskLevel'] == 'High'])
        st.metric("High Risk", high_risk, delta=f"{high_risk/len(df)*100:.1f}%" if len(df) > 0 else "0%")
    
    with col3:
        medium_risk = len(df[df['riskLevel'] == 'Medium'])
        st.metric("Medium Risk", medium_risk, delta=f"{medium_risk/len(df)*100:.1f}%" if len(df) > 0 else "0%")
    
    with col4:
        low_risk = len(df[df['riskLevel'] == 'Low'])
        st.metric("Low Risk", low_risk, delta=f"{low_risk/len(df)*100:.1f}%" if len(df) > 0 else "0%")

def render_risk_chart(df: pd.DataFrame) -> None:
    """
    Render risk distribution chart.
    
    Args:
        df: Obligations DataFrame
    """
    # Count risk levels
    risk_counts = df['riskLevel'].value_counts()
    
    # Create pie chart
    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Risk Level Distribution",
        color_discrete_map={
            'High': '#ff4444',
            'Medium': '#ffaa00',
            'Low': '#44ff44'
        }
    )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Render filtering options for the table.
    
    Args:
        df: Original DataFrame
        
    Returns:
        Filtered DataFrame
    """
    st.subheader("🔍 Filter Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Risk level filter
        risk_filter = st.multiselect(
            "Risk Level",
            options=['Low', 'Medium', 'High'],
            default=['Low', 'Medium', 'High']
        )
    
    with col2:
        # Party filter
        parties = sorted(df['responsibleParty'].unique())
        party_filter = st.multiselect(
            "Responsible Party",
            options=parties,
            default=parties
        )
    
    with col3:
        # Date filter
        date_options = ['All', 'Has Due Date', 'Ongoing']
        date_filter = st.selectbox("Due Date", date_options)
    
    # Apply filters
    filtered_df = df.copy()
    
    if risk_filter:
        filtered_df = filtered_df[filtered_df['riskLevel'].isin(risk_filter)]
    
    if party_filter:
        filtered_df = filtered_df[filtered_df['responsibleParty'].isin(party_filter)]
    
    if date_filter == 'Has Due Date':
        filtered_df = filtered_df[filtered_df['dueDate'] != 'Ongoing']
    elif date_filter == 'Ongoing':
        filtered_df = filtered_df[filtered_df['dueDate'] == 'Ongoing']
    
    # Ensure ID column exists (in case it was lost during filtering)
    if 'ID' not in filtered_df.columns:
        filtered_df.insert(0, 'ID', range(1, len(filtered_df) + 1))
    
    # Show filter results
    if len(filtered_df) != len(df):
        st.info(f"Showing {len(filtered_df)} of {len(df)} obligations")
    
    return filtered_df

def render_interactive_table(df: pd.DataFrame) -> None:
    """
    Render the interactive obligations table.
    
    Args:
        df: Filtered DataFrame
    """
    st.subheader("📊 Obligations Table")
    
    # Ensure ID column exists
    if 'ID' not in df.columns:
        df = df.copy()
        df.insert(0, 'ID', range(1, len(df) + 1))
    
    # Prepare table data
    display_df = df[['ID', 'obligation', 'responsibleParty', 'dueDate', 'riskLevel', 'summary']].copy()
    
    # Rename columns for display
    display_df.columns = ['ID', 'Obligation', 'Responsible Party', 'Due Date', 'Risk Level', 'Summary']
    
    # Color code risk levels using the new pandas styling method
    def color_risk(val):
        if val == 'High':
            return 'background-color: #ffebee'
        elif val == 'Medium':
            return 'background-color: #fff3e0'
        else:
            return 'background-color: #e8f5e8'
    
    # Apply styling using the new map method
    styled_df = display_df.style.map(color_risk, subset=['Risk Level'])
    
    # Display table
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=400
    )
    
    # Add expandable details for each obligation
    with st.expander("📝 Detailed View"):
        for _, row in df.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.write(f"**ID:** {row.get('ID', 'N/A')}")
                    st.write(f"**Risk:** {row['riskLevel']}")
                    st.write(f"**Party:** {row['responsibleParty']}")
                    st.write(f"**Due:** {row['dueDate']}")
                
                with col2:
                    st.write(f"**Obligation:** {row['obligation']}")
                    st.write(f"**Summary:** {row['summary']}")
                
                st.divider()

def render_export_options(df: pd.DataFrame) -> None:
    """
    Render export options for the obligations data.
    
    Args:
        df: Obligations DataFrame
    """
    st.subheader("💾 Export Options")
    
    # Ensure ID column exists before export
    export_df = df.copy()
    if 'ID' not in export_df.columns:
        export_df.insert(0, 'ID', range(1, len(export_df) + 1))
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV export
        csv_data = export_df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name="contract_obligations.csv",
            mime="text/csv"
        )
    
    with col2:
        # Summary export
        summary_text = generate_summary_text(export_df)
        st.download_button(
            label="📝 Download Summary",
            data=summary_text,
            file_name="obligations_summary.txt",
            mime="text/plain"
        )

def generate_summary_text(df: pd.DataFrame) -> str:
    """
    Generate a text summary of obligations.
    
    Args:
        df: Obligations DataFrame
        
    Returns:
        Summary text
    """
    summary = f"CONTRACT OBLIGATIONS SUMMARY\n"
    summary += f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary += f"Total Obligations: {len(df)}\n\n"
    
    # Risk breakdown
    risk_counts = df['riskLevel'].value_counts()
    summary += "RISK BREAKDOWN:\n"
    for risk, count in risk_counts.items():
        percentage = (count / len(df)) * 100
        summary += f"- {risk}: {count} ({percentage:.1f}%)\n"
    
    summary += "\nPARTY BREAKDOWN:\n"
    party_counts = df['responsibleParty'].value_counts()
    for party, count in party_counts.items():
        summary += f"- {party}: {count} obligations\n"
    
    summary += "\nDETAILED OBLIGATIONS:\n"
    summary += "=" * 50 + "\n"
    
    for idx, row in df.iterrows():
        # Use index + 1 as ID if ID column doesn't exist
        obligation_id = row.get('ID', idx + 1)
        summary += f"\nID: {obligation_id}\n"
        summary += f"Risk Level: {row['riskLevel']}\n"
        summary += f"Responsible Party: {row['responsibleParty']}\n"
        summary += f"Due Date: {row['dueDate']}\n"
        summary += f"Obligation: {row['obligation']}\n"
        summary += f"Summary: {row['summary']}\n"
        summary += "-" * 30 + "\n"
    
    return summary 