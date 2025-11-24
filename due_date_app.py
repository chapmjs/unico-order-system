import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(page_title="UniCo Plant - Order Promise System", layout="wide")

# Initialize session state for orders if not exists
if 'orders' not in st.session_state:
    st.session_state.orders = pd.DataFrame({
        'Order_ID': ['ORD-001', 'ORD-002', 'ORD-003', 'ORD-004', 'ORD-005'],
        'Customer': ['Burnside', 'ABC Corp', 'Johnson Inc', 'Burnside', 'XYZ Ltd'],
        'Product': ['Model 12', 'Model 15', 'Model 12', 'Model 18', 'Model 15'],
        'Quantity': [100, 250, 75, 150, 200],
        'Bottleneck_Hours': [12.0, 30.0, 9.0, 22.0, 24.0],
        'Order_Date': [datetime.now() - timedelta(days=10), 
                       datetime.now() - timedelta(days=8),
                       datetime.now() - timedelta(days=5),
                       datetime.now() - timedelta(days=3),
                       datetime.now() - timedelta(days=1)],
        'Promised_Date': [datetime.now() + timedelta(days=5),
                          datetime.now() + timedelta(days=12),
                          datetime.now() + timedelta(days=8),
                          datetime.now() + timedelta(days=15),
                          datetime.now() + timedelta(days=18)],
        'Status': ['In Production', 'In Production', 'In Queue', 'In Queue', 'In Queue'],
        'Progress': [60, 35, 0, 0, 0]
    })

# Bottleneck capacity parameters
BOTTLENECK_HOURS_PER_DAY = 16  # Two shifts, accounting for setup/breaks
BOTTLENECK_HOURS_PER_WEEK = BOTTLENECK_HOURS_PER_DAY * 5  # 5 day work week

# Header
st.title("🏭 UniCo Manufacturing - Order Promise System")
st.markdown("### Based on Theory of Constraints - Managing the Bottleneck")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "➕ New Order Calculator", "📋 Order Details", "📈 Analytics"])

with tab1:
    # Dashboard
    st.header("Current Order Status")
    
    # Calculate metrics
    orders_df = st.session_state.orders.copy()
    total_orders = len(orders_df)
    orders_on_time = len(orders_df[orders_df['Promised_Date'] >= datetime.now()])
    total_bottleneck_hours = orders_df['Bottleneck_Hours'].sum()
    
    # Calculate bottleneck utilization for next 2 weeks
    weeks_of_work = total_bottleneck_hours / BOTTLENECK_HOURS_PER_WEEK
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Orders", total_orders)
    
    with col2:
        on_time_pct = (orders_on_time / total_orders * 100) if total_orders > 0 else 0
        st.metric("On-Time Status", f"{on_time_pct:.0f}%")
    
    with col3:
        st.metric("Bottleneck Queue", f"{total_bottleneck_hours:.1f} hrs")
    
    with col4:
        st.metric("Weeks of Work", f"{weeks_of_work:.1f} weeks")
    
    st.markdown("---")
    
    # Order status visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Order Timeline")
        
        # Create timeline chart
        orders_display = orders_df.copy()
        orders_display['Days_Until_Due'] = (orders_display['Promised_Date'] - datetime.now()).dt.days
        orders_display['Status_Color'] = orders_display['Days_Until_Due'].apply(
            lambda x: 'red' if x < 0 else ('orange' if x < 7 else 'green')
        )
        
        fig = go.Figure()
        
        for idx, row in orders_display.iterrows():
            fig.add_trace(go.Bar(
                y=[row['Order_ID']],
                x=[row['Progress']],
                orientation='h',
                name=row['Order_ID'],
                marker=dict(color=row['Status_Color']),
                text=f"{row['Progress']}%",
                textposition='inside',
                hovertemplate=f"<b>{row['Order_ID']}</b><br>" +
                             f"Customer: {row['Customer']}<br>" +
                             f"Product: {row['Product']}<br>" +
                             f"Progress: {row['Progress']}%<br>" +
                             f"Due: {row['Promised_Date'].strftime('%Y-%m-%d')}<br>" +
                             f"Days Until Due: {row['Days_Until_Due']}<extra></extra>"
            ))
        
        fig.update_layout(
            showlegend=False,
            xaxis_title="Progress (%)",
            yaxis_title="Order ID",
            height=400,
            xaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Order Health")
        
        # Status distribution
        status_counts = orders_df['Status'].value_counts()
        
        fig2 = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            marker=dict(colors=['#FFA500', '#90EE90', '#FFB6C1'])
        )])
        
        fig2.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Risk summary
        orders_display = orders_df.copy()
        orders_display['Days_Until_Due'] = (orders_display['Promised_Date'] - datetime.now()).dt.days
        
        at_risk = len(orders_display[orders_display['Days_Until_Due'] < 7])
        st.metric("⚠️ Orders at Risk (< 7 days)", at_risk)

with tab2:
    # New order calculator
    st.header("New Order Promise Calculator")
    st.markdown("Calculate realistic delivery dates based on bottleneck capacity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Order Details")
        
        new_customer = st.text_input("Customer Name", "New Customer")
        new_product = st.selectbox("Product", ["Model 12", "Model 15", "Model 18", "Model 20"])
        new_quantity = st.number_input("Quantity", min_value=1, value=100, step=10)
        
        # Bottleneck hours per unit (simplified)
        hours_per_unit = {
            "Model 12": 0.12,
            "Model 15": 0.15,
            "Model 18": 0.18,
            "Model 20": 0.20
        }
        
        new_bottleneck_hours = new_quantity * hours_per_unit[new_product]
        
        st.info(f"**Bottleneck Time Required:** {new_bottleneck_hours:.1f} hours")
        
        st.subheader("Customer Request")
        requested_date = st.date_input("Customer Requested Date", 
                                       value=datetime.now() + timedelta(days=14))
    
    with col2:
        st.subheader("Capacity Analysis")
        
        # Calculate current queue
        current_queue = orders_df['Bottleneck_Hours'].sum()
        total_with_new = current_queue + new_bottleneck_hours
        
        # Calculate when this order can realistically be done
        days_in_queue = current_queue / BOTTLENECK_HOURS_PER_DAY
        days_for_new_order = new_bottleneck_hours / BOTTLENECK_HOURS_PER_DAY
        total_days_needed = days_in_queue + days_for_new_order
        
        # Add buffer (20% safety margin - referenced in The Goal)
        buffered_days = total_days_needed * 1.2
        
        earliest_date = datetime.now() + timedelta(days=buffered_days)
        
        st.metric("Current Queue", f"{current_queue:.1f} hrs")
        st.metric("New Order Time", f"{new_bottleneck_hours:.1f} hrs")
        st.metric("Total Days Needed", f"{buffered_days:.1f} days")
        
        st.markdown("---")
        
        st.subheader("Recommended Promise Date")
        st.success(f"**{earliest_date.strftime('%Y-%m-%d')}**")
        
        # Check if customer request is feasible
        requested_datetime = datetime.combine(requested_date, datetime.min.time())
        days_difference = (requested_datetime - earliest_date).days
        
        if requested_datetime < earliest_date:
            st.error(f"⚠️ Customer request is {abs(days_difference)} days too aggressive!")
            st.warning("**RECOMMENDATION:** Negotiate a later date or escalate to management for expediting")
        else:
            st.success(f"✅ Customer request is feasible with {days_difference} days of buffer!")
    
    st.markdown("---")
    
    # Add order button
    if st.button("Add Order to System", type="primary"):
        new_order = pd.DataFrame({
            'Order_ID': [f'ORD-{len(orders_df) + 1:03d}'],
            'Customer': [new_customer],
            'Product': [new_product],
            'Quantity': [new_quantity],
            'Bottleneck_Hours': [new_bottleneck_hours],
            'Order_Date': [datetime.now()],
            'Promised_Date': [earliest_date],
            'Status': ['In Queue'],
            'Progress': [0]
        })
        
        st.session_state.orders = pd.concat([st.session_state.orders, new_order], ignore_index=True)
        st.success(f"✅ Order {new_order['Order_ID'].values[0]} added successfully!")
        st.rerun()

with tab3:
    # Order details table
    st.header("All Orders")
    
    orders_display = st.session_state.orders.copy()
    orders_display['Days_Until_Due'] = (orders_display['Promised_Date'] - datetime.now()).dt.days
    orders_display['Risk_Level'] = orders_display['Days_Until_Due'].apply(
        lambda x: '🔴 LATE' if x < 0 else ('🟠 AT RISK' if x < 7 else '🟢 ON TRACK')
    )
    
    # Format for display
    display_df = orders_display[['Order_ID', 'Customer', 'Product', 'Quantity', 
                                  'Bottleneck_Hours', 'Promised_Date', 'Status', 
                                  'Progress', 'Days_Until_Due', 'Risk_Level']]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Update order status
    st.subheader("Update Order")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        order_to_update = st.selectbox("Select Order", orders_df['Order_ID'].tolist())
    
    with col2:
        new_status = st.selectbox("New Status", ["In Queue", "In Production", "Completed", "Shipped"])
    
    with col3:
        new_progress = st.slider("Progress (%)", 0, 100, 0)
    
    if st.button("Update Order"):
        idx = st.session_state.orders[st.session_state.orders['Order_ID'] == order_to_update].index[0]
        st.session_state.orders.at[idx, 'Status'] = new_status
        st.session_state.orders.at[idx, 'Progress'] = new_progress
        st.success(f"✅ Order {order_to_update} updated!")
        st.rerun()

with tab4:
    # Analytics
    st.header("Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bottleneck Utilization Forecast")
        
        # Create weekly forecast
        weeks = []
        hours = []
        cumulative_hours = 0
        
        for week in range(1, 5):
            week_orders = orders_df[
                (orders_df['Promised_Date'] >= datetime.now() + timedelta(weeks=week-1)) &
                (orders_df['Promised_Date'] < datetime.now() + timedelta(weeks=week))
            ]
            week_hours = week_orders['Bottleneck_Hours'].sum()
            cumulative_hours += week_hours
            
            weeks.append(f"Week {week}")
            hours.append(week_hours)
        
        forecast_df = pd.DataFrame({
            'Week': weeks,
            'Hours': hours,
            'Capacity': [BOTTLENECK_HOURS_PER_WEEK] * 4,
            'Utilization_%': [(h / BOTTLENECK_HOURS_PER_WEEK * 100) for h in hours]
        })
        
        fig3 = go.Figure()
        
        fig3.add_trace(go.Bar(
            x=forecast_df['Week'],
            y=forecast_df['Hours'],
            name='Planned Hours',
            marker_color='lightblue'
        ))
        
        fig3.add_trace(go.Scatter(
            x=forecast_df['Week'],
            y=forecast_df['Capacity'],
            name='Capacity',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig3.update_layout(
            yaxis_title="Hours",
            height=400
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.subheader("Customer Order Distribution")
        
        customer_orders = orders_df['Customer'].value_counts()
        
        fig4 = px.bar(
            x=customer_orders.index,
            y=customer_orders.values,
            labels={'x': 'Customer', 'y': 'Number of Orders'},
            color=customer_orders.values,
            color_continuous_scale='Blues'
        )
        
        fig4.update_layout(height=400, showlegend=False)
        
        st.plotly_chart(fig4, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**💡 Theory of Constraints Principle:** 
*"An hour lost at the bottleneck is an hour lost for the entire system. An hour saved at a non-bottleneck is a mirage."* - The Goal

This system helps protect bottleneck capacity and make realistic promises based on constraint capacity.
""")
