# 🚢 AI-Enhanced Ship Route Generator

An advanced maritime route generation and visualization service with **AI-powered safety analysis** that calculates optimal shipping routes while automatically checking for hazardous zones.

## 🌟 Key Features

### Core Routing
- **🤖 AI-Powered Routing**: Intelligent pathfinding using [searoute-py](https://github.com/genthalili/searoute-py)
- **🌍 Global Coverage**: Calculate routes between any maritime ports worldwide
- **⚓ Real Port Data**: Automatically identifies nearest ports with detailed information
- **🎯 Preset Locations**: Quick access to major maritime ports around the world

### 🛡️ AI Safety Analysis (NEW!)
- **Real-time Hazard Detection**: Automatically checks routes against 12+ hazardous zones
- **Intelligent Risk Assessment**: Analyzes piracy zones, storms, high winds, ice, and more
- **Automatic Route Optimization**: Suggests safer alternatives when hazards are detected
- **Visual Safety Indicators**: Color-coded routes and hazard zone overlays on map
- **Detailed Safety Reports**: Comprehensive analysis with recommendations

### Visualization & Export
- **🗺️ Interactive Map**: Beautiful maps with hazard zones and safety waypoints
- **📊 Detailed Analytics**: Distance, duration, safety status, and port information
- **💾 GeoJSON Export**: Export routes in standard GeoJSON format

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the application**:
```bash
# Option 1: Using the run script
./run.sh

# Option 2: Direct command
streamlit run app.py

# Option 3: Using Python module
python3 -m streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

### Programmatic Usage

You can also use the searoute library programmatically without the UI:

```python
import searoute as sr

# Generate a route
route = sr.searoute(
    origin=[0.1071, 49.4859],      # Le Havre, France [lon, lat]
    destination=[117.7449, 38.9868], # Tianjin, China [lon, lat]
    units="naut"                      # nautical miles
)

# Access route properties
distance = route["properties"]["length"]
duration = route["properties"]["duration_hours"]
```

See `example_usage.py` for more detailed examples.

## 📖 How to Use

### Basic Route Generation

1. **Select Origin Port**: 
   - Choose from preset locations or enter custom coordinates
   - Preset options include major ports like Le Havre, Singapore, Shanghai, etc.

2. **Select Destination Port**:
   - Similarly, choose a preset or enter custom coordinates
   - Coordinates should be in decimal degrees format

3. **Generate Route**:
   - Click the "Generate Route" button
   - The AI automatically:
     - Calculates the optimal maritime route
     - Checks for hazardous zones
     - Attempts to find safer alternatives if needed

4. **Review Safety Analysis**:
   - Check the safety status indicator at the top
   - Review the detailed safety report in the right panel
   - Examine hazard zones on the interactive map

5. **View Results**:
   - Interactive map shows:
     - Your route (color-coded by safety level)
     - Hazard zones as colored polygons
     - Safety waypoints (if route was optimized)
   - Route information panel displays:
     - Safety analysis report
     - Total distance (in nautical miles)
     - Estimated duration
     - Origin and destination port details
   
6. **Export Data**:
   - Download the route as a GeoJSON file for use in other applications

### Understanding Safety Indicators

**Route Colors:**
- 🟢 **Green**: Safe route, no hazards detected
- 🔵 **Blue**: Low risk, minor advisory
- 🟠 **Orange**: Medium risk, caution advised
- 🔴 **Red**: High risk, alternative route strongly recommended

**Hazard Zones:**
- Yellow regions: Low severity hazards
- Orange regions: Medium severity hazards
- Red regions: High severity hazards

**Status Messages:**
- ✅ Safe route generated successfully
- 🔄 Route rerouted to avoid hazards
- ⚠️ Route contains risk hazards

## 🎯 Example Routes

The application comes with several preset locations for quick testing:

- **Le Havre, France** ↔️ **Tianjin, China**: Trans-continental shipping route
- **New York, USA** ↔️ **Singapore**: Trans-Pacific route
- **Rotterdam, Netherlands** ↔️ **Shanghai, China**: Major trade route
- **Santos, Brazil** ↔️ **Hamburg, Germany**: Atlantic crossing

## 🛡️ AI Safety Features

The system monitors **12 active hazard zones** worldwide:

### Hazard Types
- **🏴‍☠️ Piracy Zones**: Gulf of Aden, Malacca Strait, Gulf of Guinea, Mozambique Channel
- **🌪️ Storm Zones**: South China Sea, North Atlantic, Bay of Bengal, Caribbean Sea
- **🌊 High Winds**: Red Sea
- **🧊 Ice Formations**: Bering Sea
- **🌋 Volcanic Activity**: Sunda Strait
- **🚢 High Traffic**: East China Sea

For detailed information about the AI safety features, see [AI_SAFETY_FEATURES.md](AI_SAFETY_FEATURES.md).

## 🛠️ Technology Stack

- **[Streamlit](https://streamlit.io/)**: Web application framework
- **[searoute-py](https://github.com/genthalili/searoute-py)**: Maritime route calculation
- **[Folium](https://python-visualization.github.io/folium/)**: Interactive map visualization
- **[streamlit-folium](https://github.com/randyzwitch/streamlit-folium)**: Streamlit-Folium integration
- **[Shapely](https://shapely.readthedocs.io/)**: Geometric operations for hazard detection

## 📦 Dependencies

```
streamlit==1.29.0
searoute==1.4.3
folium==0.15.1
streamlit-folium==0.15.1
pandas==2.1.4
numpy==1.26.2
shapely==2.0.2
```

## 🗺️ GeoJSON Output Format

The application generates GeoJSON data in the following format:

```json
{
  "geometry": {
    "coordinates": [[lon1, lat1], [lon2, lat2], ...],
    "type": "LineString"
  },
  "properties": {
    "duration_hours": 461.88,
    "length": 20529.85,
    "port_origin": {
      "cty": "France",
      "name": "Le Havre",
      "port": "FRLEH",
      "x": 0.107054,
      "y": 49.485998
    },
    "port_dest": {
      "cty": "China",
      "name": "Tianjin",
      "port": "CNTSN",
      "x": 117.744852,
      "y": 38.986802
    },
    "units": "km"
  },
  "type": "Feature"
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [searoute-py](https://github.com/genthalili/searoute-py) by Gentian Halili for the maritime routing engine
- Streamlit team for the excellent web framework
- Folium contributors for the mapping library

## 📧 Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---

**Happy Sailing! ⛵**
