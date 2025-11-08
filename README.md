# 🚢 Ship Route Generator & Visualizer

An AI-powered maritime route generation and visualization service that calculates optimal shipping routes between any two points on Earth.

## 🌟 Features

- **🤖 AI-Powered Routing**: Uses intelligent pathfinding algorithms through the [searoute-py](https://github.com/genthalili/searoute-py) library
- **🗺️ Interactive Map Visualization**: Beautiful, interactive maps powered by Folium
- **🌍 Global Coverage**: Calculate routes between any maritime ports worldwide
- **📊 Detailed Analytics**: Get distance, duration, and port information for each route
- **💾 GeoJSON Export**: Export routes in standard GeoJSON format
- **⚓ Real Port Data**: Automatically identifies nearest ports and provides detailed information
- **🎯 Preset Locations**: Quick access to major maritime ports around the world

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

1. **Select Origin Port**: 
   - Choose from preset locations or enter custom coordinates
   - Preset options include major ports like Le Havre, Singapore, Shanghai, etc.

2. **Select Destination Port**:
   - Similarly, choose a preset or enter custom coordinates
   - Coordinates should be in decimal degrees format

3. **Generate Route**:
   - Click the "Generate Route" button
   - Wait for the AI to calculate the optimal maritime route

4. **View Results**:
   - Interactive map shows the complete route
   - Route information panel displays:
     - Total distance (in nautical miles)
     - Estimated duration
     - Origin and destination port details
   
5. **Export Data**:
   - Download the route as a GeoJSON file for use in other applications

## 🎯 Example Routes

The application comes with several preset locations for quick testing:

- **Le Havre, France** ↔️ **Tianjin, China**: Trans-continental shipping route
- **New York, USA** ↔️ **Singapore**: Trans-Pacific route
- **Rotterdam, Netherlands** ↔️ **Shanghai, China**: Major trade route
- **Santos, Brazil** ↔️ **Hamburg, Germany**: Atlantic crossing

## 🛠️ Technology Stack

- **[Streamlit](https://streamlit.io/)**: Web application framework
- **[searoute-py](https://github.com/genthalili/searoute-py)**: Maritime route calculation
- **[Folium](https://python-visualization.github.io/folium/)**: Interactive map visualization
- **[streamlit-folium](https://github.com/randyzwitch/streamlit-folium)**: Streamlit-Follit integration

## 📦 Dependencies

```
streamlit==1.29.0
searoute==1.4.3
folium==0.15.1
streamlit-folium==0.15.1
pandas==2.1.4
numpy==1.26.2
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
