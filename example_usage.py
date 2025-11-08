#!/usr/bin/env python3
"""
Example script demonstrating programmatic usage of the searoute library.
This shows how to use searoute independently of the Streamlit UI.
"""

import searoute as sr
import json

def generate_ship_route(origin_lon, origin_lat, dest_lon, dest_lat):
    """
    Generate a maritime route between two points.
    
    Args:
        origin_lon: Origin longitude
        origin_lat: Origin latitude  
        dest_lon: Destination longitude
        dest_lat: Destination latitude
        
    Returns:
        GeoJSON feature containing the route
    """
    print(f"Calculating route from ({origin_lat}, {origin_lon}) to ({dest_lat}, {dest_lon})...")
    
    route = sr.searoute(
        origin=[origin_lon, origin_lat],
        destination=[dest_lon, dest_lat],
        units="naut"  # nautical miles
    )
    
    return route

def display_route_info(route):
    """Display information about the calculated route."""
    if not route or "properties" not in route:
        print("❌ Invalid route data")
        return
    
    props = route["properties"]
    
    print("\n" + "="*60)
    print("🚢 MARITIME ROUTE INFORMATION")
    print("="*60)
    
    # Distance
    if "length" in props:
        distance = props["length"]
        print(f"📏 Distance: {distance:.2f} nautical miles")
        print(f"            ({distance * 1.852:.2f} km)")
    
    # Duration
    if "duration_hours" in props:
        duration = props["duration_hours"]
        days = int(duration // 24)
        hours = int(duration % 24)
        print(f"⏱️  Duration: {days} days, {hours} hours")
    
    # Origin
    if "port_origin" in props:
        origin = props["port_origin"]
        print(f"\n🔵 Origin Port:")
        print(f"   Name: {origin.get('name', 'N/A')}")
        print(f"   Country: {origin.get('cty', 'N/A')}")
        print(f"   Code: {origin.get('port', 'N/A')}")
        print(f"   Coordinates: ({origin.get('y', 'N/A')}, {origin.get('x', 'N/A')})")
    
    # Destination
    if "port_dest" in props:
        dest = props["port_dest"]
        print(f"\n🔴 Destination Port:")
        print(f"   Name: {dest.get('name', 'N/A')}")
        print(f"   Country: {dest.get('cty', 'N/A')}")
        print(f"   Code: {dest.get('port', 'N/A')}")
        print(f"   Coordinates: ({dest.get('y', 'N/A')}, {dest.get('x', 'N/A')})")
    
    # Route statistics
    if "geometry" in route and "coordinates" in route["geometry"]:
        num_points = len(route["geometry"]["coordinates"])
        print(f"\n📍 Route Points: {num_points}")
    
    print("="*60 + "\n")

def save_route_to_file(route, filename="route.geojson"):
    """Save route to a GeoJSON file."""
    with open(filename, 'w') as f:
        json.dump(route, f, indent=2)
    print(f"💾 Route saved to {filename}")

# Example usage
if __name__ == "__main__":
    print("🌊 Maritime Route Generator - Example Usage\n")
    
    # Example 1: Le Havre (France) to Tianjin (China)
    print("Example 1: Le Havre, France → Tianjin, China")
    route1 = generate_ship_route(
        origin_lon=0.1071,
        origin_lat=49.4859,
        dest_lon=117.7449,
        dest_lat=38.9868
    )
    display_route_info(route1)
    save_route_to_file(route1, "route_france_to_china.geojson")
    
    # Example 2: New York (USA) to Singapore
    print("\nExample 2: New York, USA → Singapore")
    route2 = generate_ship_route(
        origin_lon=-74.0060,
        origin_lat=40.7128,
        dest_lon=103.8198,
        dest_lat=1.3521
    )
    display_route_info(route2)
    save_route_to_file(route2, "route_newyork_to_singapore.geojson")
    
    print("✅ Examples completed successfully!")
    print("\nYou can view these routes by:")
    print("1. Opening the generated .geojson files in QGIS or other GIS software")
    print("2. Uploading them to geojson.io")
    print("3. Using the Streamlit UI: streamlit run app.py")
