#!/usr/bin/env python3
"""
Example script demonstrating the AI-powered safety analysis features.
This shows how to use the route safety analyzer programmatically.
"""

from route_safety_analyzer import RouteSafetyAnalyzer, format_safety_report
import json


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def demo_route_safety_check(analyzer, origin, destination, route_name):
    """
    Demonstrate safety checking for a specific route.
    
    Args:
        analyzer: RouteSafetyAnalyzer instance
        origin: [lon, lat] origin coordinates
        destination: [lon, lat] destination coordinates
        route_name: Name of the route for display
    """
    print_header(f"Route: {route_name}")
    
    print(f"📍 Origin: {origin}")
    print(f"📍 Destination: {destination}\n")
    
    print("🔍 Analyzing route safety...\n")
    
    # Generate route with safety analysis
    route, safety_analysis = analyzer.generate_safe_route(
        origin=origin,
        destination=destination,
        max_attempts=3
    )
    
    if not route:
        print("❌ Failed to generate route\n")
        return
    
    # Display route distance and duration
    props = route.get("properties", {})
    distance = props.get("length", 0)
    duration = props.get("duration_hours", 0)
    
    print(f"📏 Distance: {distance:.2f} nautical miles ({distance * 1.852:.2f} km)")
    print(f"⏱️  Duration: {int(duration // 24)}d {int(duration % 24)}h\n")
    
    # Display safety analysis
    print(format_safety_report(safety_analysis))
    
    # Show if route was modified
    if safety_analysis.get("rerouted"):
        waypoint = safety_analysis.get("waypoint_used")
        print(f"\n📌 Safety waypoint added at: {waypoint}")
        
        # Calculate additional distance
        print("\n💡 By adding this waypoint, the route avoids high-risk areas,")
        print("   trading some additional distance for significantly improved safety.")
    
    print("\n" + "-" * 80)


def demo_hazard_summary(analyzer):
    """Display summary of all hazard zones."""
    print_header("Global Hazard Zone Summary")
    
    summary = analyzer.get_hazard_summary()
    
    print(f"📊 Total Active Hazards: {summary['total_active_hazards']}\n")
    
    print("By Severity:")
    for severity, count in sorted(summary['by_severity'].items(), 
                                   key=lambda x: {'high': 3, 'medium': 2, 'low': 1}.get(x[0], 0), 
                                   reverse=True):
        if count > 0:
            icons = {'high': '🔴', 'medium': '🟠', 'low': '🟡'}
            print(f"  {icons.get(severity, '⚪')} {severity.upper()}: {count}")
    
    print("\nBy Type:")
    for hazard_type, count in sorted(summary['by_type'].items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            type_icons = {
                'piracy': '🏴‍☠️',
                'storm': '🌪️',
                'high_winds': '🌊',
                'ice': '🧊',
                'volcanic_activity': '🌋',
                'high_traffic': '🚢'
            }
            icon = type_icons.get(hazard_type, '⚠️')
            print(f"  {icon} {hazard_type.replace('_', ' ').title()}: {count}")
    
    print(f"\n📅 Last updated: {summary['last_updated']}\n")


def main():
    """Main demonstration function."""
    print("\n" + "🛡️" * 40)
    print("   AI-POWERED MARITIME ROUTE SAFETY ANALYSIS DEMO")
    print("🛡️" * 40)
    
    # Initialize the safety analyzer
    print("\n⚙️  Initializing safety analyzer...")
    analyzer = RouteSafetyAnalyzer("hazardous_zones.json")
    print("✅ Analyzer ready!\n")
    
    # Show hazard summary
    demo_hazard_summary(analyzer)
    
    # Example 1: Santos, Brazil to Tianjin, China
    # This route typically goes through multiple hazard zones
    demo_route_safety_check(
        analyzer,
        origin=[-46.3335, -23.9608],  # Santos, Brazil
        destination=[117.7449, 38.9868],  # Tianjin, China
        route_name="Santos, Brazil → Tianjin, China (High-risk route)"
    )
    
    # Example 2: Rotterdam to New York
    # This route may pass through North Atlantic storm zone
    demo_route_safety_check(
        analyzer,
        origin=[4.4777, 51.9244],  # Rotterdam, Netherlands
        destination=[-74.0060, 40.7128],  # New York, USA
        route_name="Rotterdam, Netherlands → New York, USA (Atlantic crossing)"
    )
    
    # Example 3: Dubai to Singapore
    # This route goes through piracy zones in Gulf of Aden and Malacca Strait
    demo_route_safety_check(
        analyzer,
        origin=[55.2708, 25.2048],  # Dubai, UAE
        destination=[103.8198, 1.3521],  # Singapore
        route_name="Dubai, UAE → Singapore (Multiple piracy zones)"
    )
    
    # Example 4: Los Angeles to Shanghai
    # This route crosses the Pacific, generally safer
    demo_route_safety_check(
        analyzer,
        origin=[-118.1937, 33.7701],  # Los Angeles, USA
        destination=[121.4737, 31.2304],  # Shanghai, China
        route_name="Los Angeles, USA → Shanghai, China (Pacific crossing)"
    )
    
    # Example 5: Le Havre to Hamburg
    # Short route in European waters, typically safe
    demo_route_safety_check(
        analyzer,
        origin=[0.1071, 49.4859],  # Le Havre, France
        destination=[9.9937, 53.5511],  # Hamburg, Germany
        route_name="Le Havre, France → Hamburg, Germany (European coastal)"
    )
    
    print_header("Demonstration Complete")
    print("💡 Key Takeaways:\n")
    print("1. The AI automatically detects hazardous zones along routes")
    print("2. Routes are color-coded based on risk level (safe/low/medium/high)")
    print("3. System attempts to find safer alternatives when hazards are detected")
    print("4. Detailed safety reports include hazard types, severity, and recommendations")
    print("5. Trade-offs between distance and safety are clearly communicated\n")
    
    print("🌐 Try these routes in the web interface:")
    print("   streamlit run app.py\n")
    
    print("📖 For more information, see AI_SAFETY_FEATURES.md\n")
    print("⛵ Safe sailing!\n")


if __name__ == "__main__":
    main()
