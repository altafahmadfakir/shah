import streamlit as st
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Ride Booking App", page_icon="🚖", layout="wide")

# ------------------------
# Session State
# ------------------------
if "rides" not in st.session_state:
    st.session_state.rides = []

# ------------------------
# Dummy Drivers
# ------------------------
drivers = [
    {"name": "John", "car": "Toyota Prius", "rating": 4.9},
    {"name": "David", "car": "Honda Civic", "rating": 4.8},
    {"name": "Alex", "car": "Tesla Model 3", "rating": 5.0},
    {"name": "Emma", "car": "Hyundai Elantra", "rating": 4.7},
]

vehicle_prices = {
    "Bike": 8,
    "Mini": 12,
    "Sedan": 18,
    "SUV": 25,
}

# ------------------------
# Sidebar
# ------------------------
st.sidebar.title("🚖 Ride App")

page = st.sidebar.radio(
    "Menu",
    ["Book Ride", "Ride History"]
)

# ------------------------
# Booking Page
# ------------------------
if page == "Book Ride":

    st.title("🚖 Uber Clone (Streamlit Demo)")

    name = st.text_input("Your Name")

    pickup = st.text_input("Pickup Location")

    destination = st.text_input("Destination")

    distance = st.slider(
        "Distance (km)",
        1,
        50,
        10
    )

    vehicle = st.selectbox(
        "Choose Vehicle",
        list(vehicle_prices.keys())
    )

    fare = distance * vehicle_prices[vehicle]

    st.metric("Estimated Fare", f"${fare}")

    if st.button("Book Ride"):

        if not name or not pickup or not destination:
            st.error("Fill all fields.")
        else:

            driver = random.choice(drivers)

            ride = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Passenger": name,
                "Pickup": pickup,
                "Destination": destination,
                "Vehicle": vehicle,
                "Fare": fare,
                "Driver": driver["name"],
                "Car": driver["car"],
                "Rating": driver["rating"],
                "Status": "Driver Assigned"
            }

            st.session_state.rides.append(ride)

            st.success("Ride Booked Successfully!")

            st.subheader("Driver Details")

            st.write(f"👨 Driver: **{driver['name']}**")
            st.write(f"🚗 Vehicle: **{driver['car']}**")
            st.write(f"⭐ Rating: **{driver['rating']}**")

            st.info("Driver is arriving in 5 minutes.")

# ------------------------
# Ride History
# ------------------------
elif page == "Ride History":

    st.title("📜 Ride History")

    if len(st.session_state.rides) == 0:
        st.warning("No rides yet.")
    else:
        df = pd.DataFrame(st.session_state.rides)
        st.dataframe(df, use_container_width=True)