import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64

# Set page configuration
st.set_page_config(
    page_title="Digital TFI Leap Card",
    page_icon="🚌",
    layout="wide"
)

# Custom CSS with green and white color scheme
st.markdown("""
<style>
    /* Main colors */
    :root {
        --main-green: #2E8B57;
        --light-green: #98FB98;
        --white: #FFFFFF;
        --off-white: #F5F5F5;
        --dark-green: #006400;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: var(--main-green);
        color: white;
    }
    
    /* Main header */
    .main-header {
        color: var(--main-green);
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background-color: var(--white);
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* Section headers */
    .section-header {
        color: var(--main-green);
        font-size: 24px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 2px solid var(--light-green);
        padding-bottom: 10px;
    }
    
    /* Cards */
    .card {
        background-color: var(--white);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Pass card */
    .pass-card {
        background-color: var(--white);
        border: 2px solid var(--main-green);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Pass title */
    .pass-title {
        color: var(--main-green);
        font-size: 18px;
        font-weight: bold;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--main-green);
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: var(--dark-green);
    }
    
    /* Purchase button */
    .purchase-btn {
        background-color: var(--main-green);
        color: white;
        text-align: center;
        padding: 12px;
        border-radius: 20px;
        font-weight: bold;
        cursor: pointer;
        margin-top: 15px;
    }
    
    /* Features list */
    .features-list li {
        margin-bottom: 8px;
    }
    
    /* User card */
    .user-card {
        display: flex;
        align-items: center;
        background-color: var(--off-white);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .user-card img {
        width: 50px;
        height: 50px;
        border-radius: 25px;
        margin-right: 15px;
    }
    
    /* QR Code */
    .qr-container {
        text-align: center;
        margin: 20px 0;
    }
    
    /* Transport mode icons */
    .transport-icon {
        font-size: 24px;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Sample data for the app based on the transport usage CSV file
try:
    # For when the app is deployed on Streamlit Cloud 
    # You'll need to upload your CSV there as well
    transport_data = pd.read_csv("EconometricsTransport_usage_1.csv")
except:
    # Creating sample data if the file doesn't exist
    # This is based on your CSV structure
    data = {
        "Type of Journey": ["Dublin Bus passenger", "DART", "Dublin suburban services", 
                           "Mainline and other services", "All journeys"],
        "Year": [2023, 2023, 2023, 2023, 2023],
        "VALUE": [142500000, 17500000, 12800000, 9400000, 182200000]
    }
    transport_data = pd.DataFrame(data)

# Define the pass tiers
pass_tiers = {
    "TFI Basic": {
        "days": [1, 3, 7],
        "prices": [10, 18, 25],
        "transport": "Unlimited Dublin Bus, Luas, and DART",
        "attractions": "None",
        "perks": "Real-time route planner, transit alerts",
        "color": "#98FB98",  # Light green
        "icon": "🚌"
    },
    "TFI Explorer": {
        "days": [1, 3, 7],
        "prices": [35, 55, 70],
        "transport": "Unlimited transport for the duration",
        "attractions": "3 attractions (e.g., Guinness Storehouse, Dublin Castle, EPIC Museum)",
        "perks": "Discounts on tours & food",
        "color": "#4CBB17",  # Kelly green
        "icon": "🚆"
    },
    "TFI Plus": {
        "days": [1, 3, 7],
        "prices": [70, 100, 130],
        "transport": "Unlimited transport + Express Airport Transfer",
        "attractions": "Unlimited access to top 10 attractions",
        "perks": "VIP fast-track entry, premium dining discounts",
        "color": "#006400",  # Dark green
        "icon": "✈️"
    }
}

# Function to generate a QR code image (simulated)
def get_qr_code():
    # Create a simulation of a QR code using base64
    # In a real app, you'd generate an actual QR code based on pass details
    return "iVBORw0KGgoAAAANSUhEUgAAAHQAAAB0CAYAAABUmhYnAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIlSURBVHhe7dMxAYAwEAAxFEzh3+IEVA6O5J6B3c/M8ofLe97DLUKnCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNIrQKEKjCI0iNMnsBz6KCmYlH9ogAAAAAElFTkSuQmCC"

# Function to create a trip history (simulated)
def generate_trip_history():
    today = datetime.now()
    
    history = []
    for i in range(5):
        day = today - timedelta(days=i)
        mode = ["Dublin Bus", "Luas", "DART"][i % 3]
        if i % 3 == 0:
            route = "Route 16"
            from_to = "O'Connell St to Ballinteer"
            cost = "€2.80"
        elif i % 3 == 1:
            route = "Red Line"
            from_to = "Abbey St to Smithfield"
            cost = "€2.30"
        else:
            route = "DART"
            from_to = "Pearse St to Howth"
            cost = "€3.20"
            
        history.append({
            "date": day.strftime("%d %b"),
            "time": (day.replace(hour=(8 + i) % 24, minute=(10 + i*5) % 60)).strftime("%H:%M"),
            "mode": mode,
            "route": route,
            "journey": from_to,
            "cost": cost
        })
    
    return history

# Main app layout
def main():
    # App Header
    st.markdown('<div class="main-header">Digital TFI Leap Card</div>', unsafe_allow_html=True)
    
    # App tabs
    tab1, tab2, tab3 = st.tabs(["💳 Digital Leap Card", "🎫 Tourist Passes", "📊 Transport Data"])
    
    # Tab 1: Digital Leap Card
    with tab1:
        # User information
        st.markdown('<div class="section-header">My Leap Card</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div class="card">
                <div class="user-card">
                    <img src="https://api.placeholder.com/50x50" alt="Profile">
                    <div>
                        <div style="font-weight: bold;">John Smith</div>
                        <div style="color: gray;">Standard User</div>
                    </div>
                </div>
                <div style="text-align: center; padding: 15px;">
                    <div style="font-size: 36px; font-weight: bold; color: #2E8B57;">€28.50</div>
                    <div style="color: gray;">Available Balance</div>
                </div>
                <div class="purchase-btn">Top Up Balance</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="card">
                <div class="pass-title">Your Digital Leap Card</div>
                <div class="qr-container">
                    <img src="data:image/png;base64,{}" width="150">
                </div>
                <div style="text-align: center; color: gray;">Scan at transport readers</div>
            </div>
            """.format(get_qr_code()), unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Recent Trips")
            
            # Generate trip history
            trips = generate_trip_history()
            
            # Display trips
            for trip in trips:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 8px 0;">
                    <div>
                        <div style="font-weight: bold;">{trip['mode']} - {trip['route']}</div>
                        <div style="color: gray; font-size: 14px;">{trip['journey']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div>{trip['date']} at {trip['time']}</div>
                        <div style="font-weight: bold;">{trip['cost']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Auto top-up settings
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Auto Top-Up Settings")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.toggle("Enable Auto Top-Up", value=True)
            with col_b:
                st.selectbox("Top up when balance falls below:", ["€5", "€10", "€15", "€20"])
            
            st.selectbox("Top up amount:", ["€10", "€20", "€30", "€50"])
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 2: Tourist Passes
    with tab2:
        st.markdown('<div class="section-header">TFI TravelPass+ System for Tourists</div>', unsafe_allow_html=True)
        
        selected_tier = st.radio("Select Pass Tier:", list(pass_tiers.keys()))
        
        # Display tier information
        tier_info = pass_tiers[selected_tier]
        
        st.markdown(f"""
        <div class="card" style="border-left: 5px solid {tier_info['color']};">
            <h3>{tier_info['icon']} {selected_tier}</h3>
            <p><strong>Transport:</strong> {tier_info['transport']}</p>
            <p><strong>Attractions:</strong> {tier_info['attractions']}</p>
            <p><strong>Additional Perks:</strong> {tier_info['perks']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Select duration
        col1, col2 = st.columns([2, 1])
        with col1:
            duration_index = st.select_slider(
                "Select Pass Duration:",
                options=[f"{days} day{'s' if days > 1 else ''}" for days in tier_info['days']],
                value="3 days"
            )
            duration_days = int(duration_index.split()[0])
            
            # Find the index of the selected duration
            duration_idx = tier_info['days'].index(duration_days)
            price = tier_info['prices'][duration_idx]
            
        with col2:
            st.markdown(f"""
            <div style="padding-top: 43px; text-align: center;">
                <div style="font-size: 24px; font-weight: bold;">€{price}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Calculate dates
        start_date = st.date_input("Start Date:", value=datetime.now().date())
        end_date = start_date + timedelta(days=duration_days)
        
        st.info(f"Your pass will be valid from {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}")
        
        # Purchase form
        with st.expander("Proceed to Purchase"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("First Name")
                st.text_input("Email Address")
            with col2:
                st.text_input("Last Name")
                st.text_input("Phone Number")
                
            st.selectbox("Payment Method", ["Credit/Debit Card", "PayPal", "Apple Pay", "Google Pay"])
            
            if st.button("Purchase Pass", type="primary"):
                st.success(f"Your {duration_days}-day {selected_tier} pass has been purchased successfully!")
                
                # Show QR code
                st.markdown(f"""
                <div class="card" style="text-align:center;">
                    <h3>Your TFI TravelPass+ QR Code</h3>
                    <p>Valid: {start_date.strftime('%d %b')} - {end_date.strftime('%d %b %Y')}</p>
                    <div class="qr-container">
                        <img src="data:image/png;base64,{get_qr_code()}" width="200">
                    </div>
                    <p>Scan this QR code to access transport and attractions</p>
                    <div class="purchase-btn">Add to Apple Wallet</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Tab 3: Transport Data
    with tab3:
        st.markdown('<div class="section-header">Transport Usage Data</div>', unsafe_allow_html=True)
        
        # Create a filtered dataframe for visualization
        filtered_data = transport_data[transport_data["Type of Journey"] != "All journeys"].copy()
        
        # Convert VALUE column to numeric if it's not already
        if filtered_data["VALUE"].dtype == "object":
            filtered_data["VALUE"] = pd.to_numeric(filtered_data["VALUE"], errors="coerce")
        
        # Sort by year to ensure proper timeline
        filtered_data = filtered_data.sort_values("Year")
        
        # Create a bar chart of transport usage
        fig = px.bar(
            filtered_data,
            x="Year",
            y="VALUE",
            color="Type of Journey",
            title="Transport Usage by Type (2013-2023)",
            color_discrete_sequence=px.colors.sequential.Greens,
            labels={"VALUE": "Number of Journeys", "Year": "Year"}
        )
        
        fig.update_layout(
            plot_bgcolor="white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show a pie chart of transport distribution for the latest year
        latest_year = filtered_data["Year"].max()
        latest_data = filtered_data[filtered_data["Year"] == latest_year]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_pie = px.pie(
                latest_data, 
                values="VALUE", 
                names="Type of Journey",
                title=f"Transport Distribution ({latest_year})",
                color_discrete_sequence=px.colors.sequential.Greens
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Digital Adoption Forecast")
            
            # Create a simple forecast chart showing projected digital adoption
            years = [2025, 2026, 2027, 2028, 2029]
            adoption = [20, 35, 55, 70, 85]  # percentage adoption projections
            
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(
                x=years, 
                y=adoption,
                mode='lines+markers',
                name='Digital Adoption',
                line=dict(color='#2E8B57')
            ))
            
            fig_forecast.update_layout(
                title="Projected Digital Leap Card Adoption (%)",
                xaxis_title="Year",
                yaxis_title="Adoption Rate (%)",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show data table
        st.markdown('<div class="section-header">Raw Data</div>', unsafe_allow_html=True)
        st.dataframe(transport_data, use_container_width=True)

if __name__ == "__main__":
    main()
