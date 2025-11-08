import streamlit as st
import searoute as sr
import folium
from streamlit_folium import st_folium
import json

# Page configuration
st.set_page_config(
    page_title="Ship Route Generator",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
    }
    .route-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🚢 Ship Route Generator & Visualizer")
st.markdown("""
This service uses AI-powered routing to generate optimal maritime routes between any two points on Earth.
The routes consider real maritime passages, canals, and avoid land masses.
""")

# Sidebar for inputs
st.sidebar.header("📍 Route Configuration")

# Example locations
example_locations = {
    "Custom": {"lat": None, "lon": None},
    "Le Havre, France": {"lat": 49.4859, "lon": 0.1071},
    "Tianjin, China": {"lat": 38.9868, "lon": 117.7449},
    "New York, USA": {"lat": 40.7128, "lon": -74.0060},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "Rotterdam, Netherlands": {"lat": 51.9244, "lon": 4.4777},
    "Los Angeles, USA": {"lat": 33.7701, "lon": -118.1937},
    "Shanghai, China": {"lat": 31.2304, "lon": 121.4737},
    "Dubai, UAE": {"lat": 25.2048, "lon": 55.2708},
    "Santos, Brazil": {"lat": -23.9608, "lon": -46.3335},
    "Hamburg, Germany": {"lat": 53.5511, "lon": 9.9937}
}

# Origin selection
st.sidebar.subheader("🔵 Origin Port")
origin_preset = st.sidebar.selectbox(
    "Select preset location (Origin):",
    options=list(example_locations.keys()),
    index=1  # Default to Le Havre
)

if origin_preset == "Custom":
    origin_lat = st.sidebar.number_input("Origin Latitude:", value=49.4859, min_value=-90.0, max_value=90.0, format="%.6f")
    origin_lon = st.sidebar.number_input("Origin Longitude:", value=0.1071, min_value=-180.0, max_value=180.0, format="%.6f")
else:
    origin_lat = example_locations[origin_preset]["lat"]
    origin_lon = example_locations[origin_preset]["lon"]
    st.sidebar.info(f"📌 Lat: {origin_lat:.6f}, Lon: {origin_lon:.6f}")

# Destination selection
st.sidebar.subheader("🔴 Destination Port")
dest_preset = st.sidebar.selectbox(
    "Select preset location (Destination):",
    options=list(example_locations.keys()),
    index=2  # Default to Tianjin
)

if dest_preset == "Custom":
    dest_lat = st.sidebar.number_input("Destination Latitude:", value=38.9868, min_value=-90.0, max_value=90.0, format="%.6f")
    dest_lon = st.sidebar.number_input("Destination Longitude:", value=117.7449, min_value=-180.0, max_value=180.0, format="%.6f")
else:
    dest_lat = example_locations[dest_preset]["lat"]
    dest_lon = example_locations[dest_preset]["lon"]
    st.sidebar.info(f"📌 Lat: {dest_lat:.6f}, Lon: {dest_lon:.6f}")

# Route generation button
generate_button = st.sidebar.button("🗺️ Generate Route", type="primary", use_container_width=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Interactive Map")
    
with col2:
    st.subheader("📊 Route Information")

# Initialize session state for route data
if 'route_data' not in st.session_state:
    st.session_state.route_data = None

# Generate route when button is clicked
if generate_button:
    with st.spinner("🌊 Calculating optimal maritime route..."):
        try:
            # Generate route using searoute
            route = sr.searoute(
                origin=[origin_lon, origin_lat],
                destination=[dest_lon, dest_lat],
                units="naut"  # nautical miles
            )
            
            st.session_state.route_data = route
            st.success("✅ Route generated successfully!")
            
        except Exception as e:
            st.error(f"❌ Error generating route: {str(e)}")
            st.session_state.route_data = None

# Display map and route information
if st.session_state.route_data:
    route_data = st.session_state.route_data
    
    with col1:
        # Create folium map
        # Calculate center point between origin and destination
        center_lat = (origin_lat + dest_lat) / 2
        center_lon = (origin_lon + dest_lon) / 2
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=3,
            tiles="OpenStreetMap"
        )
        
        # Add origin marker
        folium.Marker(
            location=[origin_lat, origin_lon],
            popup=f"<b>Origin</b><br>{origin_preset if origin_preset != 'Custom' else 'Custom Location'}",
            tooltip="Origin Port",
            icon=folium.Icon(color="blue", icon="anchor", prefix="fa")
        ).add_to(m)
        
        # Add destination marker
        folium.Marker(
            location=[dest_lat, dest_lon],
            popup=f"<b>Destination</b><br>{dest_preset if dest_preset != 'Custom' else 'Custom Location'}",
            tooltip="Destination Port",
            icon=folium.Icon(color="red", icon="anchor", prefix="fa")
        ).add_to(m)
        
        # Add route line
        if route_data and "geometry" in route_data and "coordinates" in route_data["geometry"]:
            coordinates = route_data["geometry"]["coordinates"]
            # Convert from [lon, lat] to [lat, lon] for folium
            route_coords = [[coord[1], coord[0]] for coord in coordinates]
            
            folium.PolyLine(
                route_coords,
                color="darkblue",
                weight=3,
                opacity=0.8,
                popup="Maritime Route"
            ).add_to(m)
            
            # Fit map to route bounds
            m.fit_bounds(route_coords)
        
        # Display map
        st_folium(m, width=None, height=500, returned_objects=[])
    
    with col2:
        # Display route properties
        if "properties" in route_data:
            props = route_data["properties"]
            
            # Distance
            if "length" in props:
                distance = props["length"]
                st.metric("🛣️ Distance", f"{distance:.2f} nautical miles")
            
            # Duration
            if "duration_hours" in props:
                duration = props["duration_hours"]
                days = int(duration // 24)
                hours = int(duration % 24)
                st.metric("⏱️ Estimated Duration", f"{days}d {hours}h")
            
            # Origin port info
            if "port_origin" in props:
                origin_port = props["port_origin"]
                st.markdown("### 🔵 Origin Port")
                if "name" in origin_port:
                    st.write(f"**Name:** {origin_port['name']}")
                if "cty" in origin_port:
                    st.write(f"**Country:** {origin_port['cty']}")
                if "port" in origin_port:
                    st.write(f"**Code:** {origin_port['port']}")
            
            # Destination port info
            if "port_dest" in props:
                dest_port = props["port_dest"]
                st.markdown("### 🔴 Destination Port")
                if "name" in dest_port:
                    st.write(f"**Name:** {dest_port['name']}")
                if "cty" in dest_port:
                    st.write(f"**Country:** {dest_port['cty']}")
                if "port" in dest_port:
                    st.write(f"**Code:** {dest_port['port']}")
        
        # Export button
        st.markdown("---")
        st.markdown("### 📥 Export Route")
        
        geojson_str = json.dumps(route_data, indent=2)
        st.download_button(
            label="Download GeoJSON",
            data=geojson_str,
            file_name="ship_route.geojson",
            mime="application/json",
            use_container_width=True
        )

else:
    with col1:
        # Display default world map
        m = folium.Map(
            location=[20, 0],
            zoom_start=2,
            tiles="OpenStreetMap"
        )
        
        st_folium(m, width=None, height=500, returned_objects=[])
    
    with col2:
        st.info("👈 Configure your origin and destination ports in the sidebar, then click 'Generate Route' to visualize the maritime route.")
        
        st.markdown("""
        ### ✨ Features
        - 🌍 Global maritime routing
        - 🤖 AI-powered pathfinding
        - 🗺️ Interactive map visualization
        - 📊 Detailed route analytics
        - 💾 GeoJSON export
        - ⚓ Real port data
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Powered by <a href='https://github.com/genthalili/searoute-py' target='_blank'>searoute-py</a> | 
    Built with Streamlit & Folium</p>
</div>
""", unsafe_allow_html=True)
