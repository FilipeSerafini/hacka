"""
Route Safety Analyzer Module

This module provides AI-powered safety analysis for maritime routes by:
1. Checking if routes pass through hazardous zones
2. Identifying specific threats (piracy, storms, high waves, etc.)
3. Suggesting alternative routes with waypoints to bypass dangerous areas
"""

import json
import math
from typing import List, Tuple, Dict, Optional
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import nearest_points
import searoute as sr


class RouteSafetyAnalyzer:
    """Analyzes maritime routes for safety hazards and suggests alternatives."""
    
    def __init__(self, hazards_file: str = "hazardous_zones.json"):
        """
        Initialize the safety analyzer with hazardous zones data.
        
        Args:
            hazards_file: Path to the JSON file containing hazardous zones
        """
        self.hazards_file = hazards_file
        self.hazard_zones = []
        self.load_hazards()
    
    def load_hazards(self):
        """Load hazardous zones from JSON file."""
        try:
            with open(self.hazards_file, 'r') as f:
                data = json.load(f)
                self.hazard_zones = data.get("hazard_zones", [])
        except FileNotFoundError:
            print(f"Warning: Hazards file {self.hazards_file} not found. No hazards loaded.")
            self.hazard_zones = []
        except json.JSONDecodeError as e:
            print(f"Error parsing hazards file: {e}")
            self.hazard_zones = []
    
    def check_route_safety(self, route: Dict) -> Dict:
        """
        Analyze a route for safety hazards.
        
        Args:
            route: GeoJSON route object from searoute
            
        Returns:
            Dictionary containing safety analysis results:
            {
                "is_safe": bool,
                "hazards_detected": List[Dict],
                "severity": str ("safe", "low", "medium", "high"),
                "recommendations": str
            }
        """
        if not route or "geometry" not in route or "coordinates" not in route["geometry"]:
            return {
                "is_safe": True,
                "hazards_detected": [],
                "severity": "safe",
                "recommendations": "No route data to analyze."
            }
        
        # Convert route coordinates to LineString
        coordinates = route["geometry"]["coordinates"]
        route_line = LineString(coordinates)
        
        # Check each hazard zone
        detected_hazards = []
        max_severity = "safe"
        severity_levels = {"safe": 0, "low": 1, "medium": 2, "high": 3}
        
        for hazard in self.hazard_zones:
            if not hazard.get("active", True):
                continue
            
            # Create polygon from hazard region
            hazard_coords = hazard["region"]["coordinates"][0]
            hazard_polygon = Polygon(hazard_coords)
            
            # Check if route intersects with hazard zone
            if route_line.intersects(hazard_polygon):
                # Calculate intersection length as percentage of total route
                intersection = route_line.intersection(hazard_polygon)
                intersection_length = self._calculate_length(intersection)
                route_length = self._calculate_length(route_line)
                percentage = (intersection_length / route_length) * 100 if route_length > 0 else 0
                
                detected_hazards.append({
                    "id": hazard["id"],
                    "name": hazard["name"],
                    "type": hazard["type"],
                    "severity": hazard["severity"],
                    "description": hazard["description"],
                    "percentage_affected": round(percentage, 2),
                    "reported_incidents": hazard.get("reported_incidents", 0),
                    "last_updated": hazard.get("last_updated", "Unknown")
                })
                
                # Update max severity
                hazard_severity = hazard["severity"]
                if severity_levels.get(hazard_severity, 0) > severity_levels.get(max_severity, 0):
                    max_severity = hazard_severity
        
        is_safe = len(detected_hazards) == 0
        recommendations = self._generate_recommendations(detected_hazards, max_severity)
        
        return {
            "is_safe": is_safe,
            "hazards_detected": detected_hazards,
            "severity": max_severity,
            "recommendations": recommendations,
            "total_hazards": len(detected_hazards)
        }
    
    def _calculate_length(self, geometry) -> float:
        """
        Calculate approximate length of a geometry in degrees.
        
        Args:
            geometry: Shapely geometry object
            
        Returns:
            Approximate length in degrees
        """
        if geometry.is_empty:
            return 0.0
        
        if hasattr(geometry, 'length'):
            return geometry.length
        
        return 0.0
    
    def _generate_recommendations(self, hazards: List[Dict], severity: str) -> str:
        """
        Generate safety recommendations based on detected hazards.
        
        Args:
            hazards: List of detected hazards
            severity: Overall severity level
            
        Returns:
            Recommendation text
        """
        if not hazards:
            return "✅ Route is clear of all known hazards. Safe to proceed."
        
        hazard_types = set(h["type"] for h in hazards)
        type_descriptions = {
            "piracy": "piracy zones",
            "storm": "active storms/typhoons",
            "high_winds": "high wind areas",
            "ice": "ice formations",
            "volcanic_activity": "volcanic activity zones",
            "high_traffic": "high traffic areas"
        }
        
        hazard_list = ", ".join(type_descriptions.get(t, t) for t in hazard_types)
        
        if severity == "high":
            return (f"⚠️ DANGER: Route passes through {hazard_list}. "
                   f"Strongly recommend alternative route. {len(hazards)} hazard(s) detected.")
        elif severity == "medium":
            return (f"⚠️ CAUTION: Route passes through {hazard_list}. "
                   f"Consider alternative route or proceed with caution. {len(hazards)} hazard(s) detected.")
        else:
            return (f"ℹ️ ADVISORY: Route passes through {hazard_list}. "
                   f"Monitor conditions. {len(hazards)} hazard(s) detected.")
    
    def suggest_waypoint_to_avoid_hazard(self, origin: List[float], destination: List[float], 
                                         hazard_zone: Dict) -> Optional[List[float]]:
        """
        Suggest a waypoint to bypass a specific hazard zone.
        
        Args:
            origin: [lon, lat] of origin
            destination: [lon, lat] of destination
            hazard_zone: Hazard zone dictionary
            
        Returns:
            [lon, lat] of suggested waypoint, or None if cannot determine
        """
        try:
            # Create polygon from hazard region
            hazard_coords = hazard_zone["region"]["coordinates"][0]
            hazard_polygon = Polygon(hazard_coords)
            
            # Get centroid and bounds of hazard zone
            centroid = hazard_polygon.centroid
            bounds = hazard_polygon.bounds  # (minx, miny, maxx, maxy)
            
            # Create direct line between origin and destination
            direct_line = LineString([origin, destination])
            
            # Calculate the perpendicular direction to route around the hazard
            origin_lon, origin_lat = origin
            dest_lon, dest_lat = destination
            centroid_lon, centroid_lat = centroid.x, centroid.y
            
            # Calculate vector from route midpoint to hazard center
            mid_lon = (origin_lon + dest_lon) / 2
            mid_lat = (origin_lat + dest_lat) / 2
            
            # Determine which side to route around based on geography
            # Calculate perpendicular offsets
            route_vector_lon = dest_lon - origin_lon
            route_vector_lat = dest_lat - origin_lat
            
            # Two perpendicular directions (left and right of route)
            perp_options = [
                # Option 1: Perpendicular to the right
                [
                    centroid_lon - route_vector_lat * 2,
                    centroid_lat + route_vector_lon * 2
                ],
                # Option 2: Perpendicular to the left  
                [
                    centroid_lon + route_vector_lat * 2,
                    centroid_lat - route_vector_lon * 2
                ],
                # Option 3: Route above (north)
                [centroid_lon, bounds[3] + abs(bounds[3] - bounds[1]) * 0.5],
                # Option 4: Route below (south)
                [centroid_lon, bounds[1] - abs(bounds[3] - bounds[1]) * 0.5]
            ]
            
            # Find the waypoint that is outside the hazard and closest to the direct route
            best_waypoint = None
            min_detour = float('inf')
            
            for waypoint_candidate in perp_options:
                wp_point = Point(waypoint_candidate)
                
                # Check if waypoint is outside hazard zone
                if not hazard_polygon.contains(wp_point) and not hazard_polygon.intersects(wp_point):
                    # Calculate total distance via waypoint
                    dist_to_wp = Point(origin).distance(wp_point)
                    dist_from_wp = wp_point.distance(Point(destination))
                    total_detour = dist_to_wp + dist_from_wp
                    
                    if total_detour < min_detour:
                        min_detour = total_detour
                        best_waypoint = waypoint_candidate
            
            # If we found a good waypoint, add extra buffer distance
            if best_waypoint:
                # Add 20% buffer away from hazard
                buffer_lon = best_waypoint[0] + (best_waypoint[0] - centroid_lon) * 0.2
                buffer_lat = best_waypoint[1] + (best_waypoint[1] - centroid_lat) * 0.2
                return [buffer_lon, buffer_lat]
            
            # Fallback: find furthest boundary point and extend it
            boundary_coords = list(hazard_polygon.exterior.coords)
            max_dist = 0
            fallback_waypoint = None
            
            for coord in boundary_coords:
                point = Point(coord)
                dist = direct_line.distance(point)
                if dist > max_dist:
                    max_dist = dist
                    fallback_waypoint = coord
            
            if fallback_waypoint:
                # Extend waypoint significantly away from hazard
                offset_lon = fallback_waypoint[0] + (fallback_waypoint[0] - centroid_lon) * 2.0
                offset_lat = fallback_waypoint[1] + (fallback_waypoint[1] - centroid_lat) * 2.0
                return [offset_lon, offset_lat]
            
        except Exception as e:
            print(f"Error calculating waypoint: {e}")
        
        return None
    
    def generate_safe_route(self, origin: List[float], destination: List[float], 
                           max_attempts: int = 3) -> Tuple[Optional[Dict], Dict]:
        """
        Generate a safe route, attempting to bypass hazard zones.
        
        Args:
            origin: [lon, lat] of origin
            destination: [lon, lat] of destination
            max_attempts: Maximum number of rerouting attempts
            
        Returns:
            Tuple of (route_dict, safety_analysis)
        """
        # First, try direct route
        try:
            route = sr.searoute(origin=origin, destination=destination, units="naut")
            safety_analysis = self.check_route_safety(route)
            
            # If route is safe or only low severity, return it
            if safety_analysis["is_safe"] or safety_analysis["severity"] == "low":
                return route, safety_analysis
            
            # Try to find alternative routes with waypoints
            best_route = route
            best_analysis = safety_analysis
            severity_order = {"high": 3, "medium": 2, "low": 1}
            
            print(f"Initial route safety: {safety_analysis['severity']} - {len(safety_analysis['hazards_detected'])} hazards")
            
            for attempt in range(max_attempts):
                # Get the most severe hazard
                hazards = best_analysis["hazards_detected"]
                if not hazards:
                    break
                
                print(f"\nAttempt {attempt + 1}: Trying to avoid hazards...")
                
                # Sort by severity and percentage affected
                hazards_sorted = sorted(
                    hazards, 
                    key=lambda h: (severity_order.get(h["severity"], 0), h["percentage_affected"]),
                    reverse=True
                )
                
                # Try to avoid the most severe hazards (try top 3)
                for hazard_to_avoid in hazards_sorted[:min(3, len(hazards_sorted))]:
                    # Find the full hazard zone data
                    hazard_zone = None
                    for hz in self.hazard_zones:
                        if hz["id"] == hazard_to_avoid["id"]:
                            hazard_zone = hz
                            break
                    
                    if not hazard_zone:
                        continue
                    
                    print(f"  Trying to avoid: {hazard_zone['name']}")
                    
                    # Suggest waypoint to avoid this hazard
                    waypoint = self.suggest_waypoint_to_avoid_hazard(origin, destination, hazard_zone)
                    
                    if waypoint:
                        print(f"  Generated waypoint: {waypoint[0]:.2f}, {waypoint[1]:.2f}")
                        try:
                            # Generate route with waypoint
                            leg1 = sr.searoute(origin=origin, destination=waypoint, units="naut")
                            leg2 = sr.searoute(origin=waypoint, destination=destination, units="naut")
                            
                            # Combine routes
                            combined_route = self._combine_routes(leg1, leg2, waypoint)
                            new_analysis = self.check_route_safety(combined_route)
                            
                            print(f"  New route safety: {new_analysis['severity']} - {len(new_analysis['hazards_detected'])} hazards")
                            
                            # If this route is better, use it
                            new_severity_score = severity_order.get(new_analysis["severity"], 0)
                            best_severity_score = severity_order.get(best_analysis["severity"], 0)
                            
                            is_improvement = (
                                new_analysis["is_safe"] or
                                new_severity_score < best_severity_score or
                                (new_severity_score == best_severity_score and 
                                 len(new_analysis["hazards_detected"]) < len(best_analysis["hazards_detected"]))
                            )
                            
                            if is_improvement:
                                print(f"  ✓ Route improved!")
                                best_route = combined_route
                                best_analysis = new_analysis
                                best_analysis["rerouted"] = True
                                best_analysis["waypoint_used"] = waypoint
                                
                                if new_analysis["is_safe"]:
                                    print("  ✓ Safe route found!")
                                    return best_route, best_analysis
                                
                                # Continue trying to improve further
                                break
                            else:
                                print(f"  ✗ No improvement")
                            
                        except Exception as e:
                            print(f"  ✗ Error generating route with waypoint: {e}")
                            continue
            
            if best_analysis.get("rerouted"):
                print(f"\n✓ Successfully rerouted. Final safety: {best_analysis['severity']}")
            else:
                print(f"\n✗ Could not find safer alternative. Original safety: {best_analysis['severity']}")
            
            return best_route, best_analysis
            
        except Exception as e:
            print(f"Error generating route: {e}")
            return None, {
                "is_safe": False,
                "hazards_detected": [],
                "severity": "high",
                "recommendations": f"Error generating route: {str(e)}",
                "total_hazards": 0
            }
    
    def _combine_routes(self, route1: Dict, route2: Dict, waypoint: List[float] = None) -> Dict:
        """
        Combine two route segments into a single route.
        
        Args:
            route1: First route segment
            route2: Second route segment
            
        Returns:
            Combined route dictionary
        """
        combined = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": []
            },
            "properties": {}
        }
        
        # Combine coordinates
        coords1 = route1["geometry"]["coordinates"]
        coords2 = route2["geometry"]["coordinates"]
        combined["geometry"]["coordinates"] = coords1 + coords2[1:]  # Skip duplicate waypoint
        
        # Combine properties
        length1 = route1.get("properties", {}).get("length", 0)
        length2 = route2.get("properties", {}).get("length", 0)
        
        duration1 = route1.get("properties", {}).get("duration_hours", 0)
        duration2 = route2.get("properties", {}).get("duration_hours", 0)
        
        combined["properties"] = {
            "length": length1 + length2,
            "duration_hours": duration1 + duration2,
            "units": route1.get("properties", {}).get("units", "naut"),
            "port_origin": route1.get("properties", {}).get("port_origin"),
            "port_dest": route2.get("properties", {}).get("port_dest"),
            "waypoint_route": True,
            "waypoint": waypoint
        }
        
        return combined
    
    def get_hazard_summary(self) -> Dict:
        """
        Get a summary of all active hazard zones.
        
        Returns:
            Dictionary with hazard statistics
        """
        active_hazards = [h for h in self.hazard_zones if h.get("active", True)]
        
        by_type = {}
        by_severity = {"low": 0, "medium": 0, "high": 0}
        
        for hazard in active_hazards:
            hazard_type = hazard.get("type", "unknown")
            by_type[hazard_type] = by_type.get(hazard_type, 0) + 1
            
            severity = hazard.get("severity", "low")
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        return {
            "total_active_hazards": len(active_hazards),
            "by_type": by_type,
            "by_severity": by_severity,
            "last_updated": max((h.get("last_updated", "") for h in active_hazards), default="Unknown")
        }


def format_safety_report(safety_analysis: Dict) -> str:
    """
    Format safety analysis into a readable report.
    
    Args:
        safety_analysis: Safety analysis dictionary
        
    Returns:
        Formatted text report
    """
    report = []
    
    if safety_analysis["is_safe"]:
        report.append("✅ **ROUTE STATUS: SAFE**")
        report.append("\nNo hazards detected along this route.")
    else:
        severity_icons = {
            "low": "ℹ️",
            "medium": "⚠️",
            "high": "🚨"
        }
        icon = severity_icons.get(safety_analysis["severity"], "⚠️")
        report.append(f"{icon} **ROUTE STATUS: {safety_analysis['severity'].upper()} RISK**")
        report.append(f"\n{safety_analysis['total_hazards']} hazard(s) detected along this route.")
        
        report.append("\n\n**Detected Hazards:**")
        for i, hazard in enumerate(safety_analysis["hazards_detected"], 1):
            report.append(f"\n{i}. **{hazard['name']}**")
            report.append(f"   - Type: {hazard['type'].replace('_', ' ').title()}")
            report.append(f"   - Severity: {hazard['severity'].upper()}")
            report.append(f"   - Description: {hazard['description']}")
            report.append(f"   - Route affected: {hazard['percentage_affected']:.1f}%")
            report.append(f"   - Incidents reported: {hazard['reported_incidents']}")
    
    report.append(f"\n\n**Recommendations:**\n{safety_analysis['recommendations']}")
    
    if safety_analysis.get("rerouted"):
        report.append("\n\n🔄 **This route has been automatically rerouted to avoid high-risk areas.**")
    
    return "\n".join(report)
