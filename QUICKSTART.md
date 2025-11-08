# 🚢 Quick Start Guide

Get up and running with the Ship Route Generator in minutes!

## 📋 Prerequisites

Make sure you have:
- Python 3.8 or higher installed
- pip package manager
- Internet connection (for downloading dependencies and generating routes)

## 🔧 Installation

### Step 1: Install Dependencies

Navigate to the project directory and install all required packages:

```bash
pip install -r requirements.txt
```

Or if you're using Python 3 specifically:

```bash
pip3 install -r requirements.txt
```

**Note:** This will install:
- Streamlit (web framework)
- searoute (maritime routing engine)
- Folium (interactive maps)
- streamlit-folium (Streamlit-Folium integration)
- pandas & numpy (data handling)

## 🚀 Running the Application

### Method 1: Using the Run Script (Recommended)

Simply execute:

```bash
./run.sh
```

### Method 2: Direct Streamlit Command

```bash
streamlit run app.py
```

### Method 3: Python Module

```bash
python3 -m streamlit run app.py
```

## 🌐 Accessing the Application

Once started, the application will:
1. Start a local web server
2. Automatically open in your default browser at `http://localhost:8501`
3. If it doesn't open automatically, manually navigate to `http://localhost:8501`

## 📱 Using the Interface

### Basic Usage

1. **Select Origin Port**
   - Use the sidebar on the left
   - Choose from preset locations (e.g., "Le Havre, France")
   - Or select "Custom" to enter your own coordinates

2. **Select Destination Port**
   - Same process as origin
   - Choose from presets or enter custom coordinates

3. **Generate Route**
   - Click the "🗺️ Generate Route" button
   - Wait a few seconds for the route calculation
   - View the route on the interactive map

4. **Explore Results**
   - Pan and zoom the map
   - View route statistics (distance, duration)
   - See port information
   - Download the route as GeoJSON

### Quick Test

Try this example to test the application:
- **Origin**: Le Havre, France
- **Destination**: Tianjin, China
- Click "Generate Route"

You should see a maritime route spanning from Europe to Asia!

## 🐍 Programmatic Usage

You can also use the library without the UI:

### Run the Example Script

```bash
python3 example_usage.py
```

This will:
- Generate two example routes
- Display detailed route information
- Save GeoJSON files that you can view in other tools

### Use in Your Own Code

```python
import searoute as sr

# Generate a route
route = sr.searoute(
    origin=[longitude, latitude],
    destination=[longitude, latitude],
    units="naut"
)

# Access route data
distance = route["properties"]["length"]
print(f"Distance: {distance} nautical miles")
```

## 🗺️ Preset Locations

The application includes these preset locations:
- **Le Havre, France** - Major European port
- **Tianjin, China** - Major Asian port
- **New York, USA** - East Coast USA
- **Singapore** - Southeast Asian hub
- **Rotterdam, Netherlands** - Europe's largest port
- **Los Angeles, USA** - West Coast USA
- **Shanghai, China** - World's busiest port
- **Dubai, UAE** - Middle Eastern hub
- **Santos, Brazil** - South American port
- **Hamburg, Germany** - Northern European port

## 💾 Exporting Routes

After generating a route:
1. Look at the right panel
2. Find the "Export Route" section
3. Click "Download GeoJSON"
4. The file can be used in:
   - QGIS
   - ArcGIS
   - Google Earth
   - geojson.io
   - Custom applications

## 🆘 Troubleshooting

### Application won't start

**Problem**: `streamlit: command not found`

**Solution**: Streamlit isn't in your PATH. Try:
```bash
python3 -m streamlit run app.py
```

### Import errors

**Problem**: Module not found errors

**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Route generation fails

**Problem**: Error when clicking "Generate Route"

**Possible causes**:
- No internet connection (searoute needs to download data on first use)
- Invalid coordinates (check latitude: -90 to 90, longitude: -180 to 180)
- Coordinates are on land or in an unreachable location

### Port not available

**Problem**: `Address already in use`

**Solution**: Change the port:
```bash
streamlit run app.py --server.port 8502
```

## 🔧 Advanced Configuration

### Changing the Port

```bash
streamlit run app.py --server.port 8080
```

### Running on a Different Host

To access from other devices on your network:
```bash
streamlit run app.py --server.address 0.0.0.0
```

### Headless Mode (No Browser)

```bash
streamlit run app.py --server.headless true
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [example_usage.py](example_usage.py) for code examples
- Explore the [searoute-py documentation](https://github.com/genthalili/searoute-py)
- Customize the app by modifying `app.py`

## 🎯 Use Cases

This tool is perfect for:
- **Maritime logistics planning**
- **Shipping cost estimation**
- **Educational purposes**
- **Research projects**
- **Route visualization**
- **Travel time calculation**

## 💡 Tips

1. **Zoom and Pan**: Use your mouse to explore the map
2. **Try Different Routes**: Experiment with various port combinations
3. **Compare Routes**: Generate multiple routes to compare different options
4. **Export Data**: Download GeoJSON files for further analysis
5. **Custom Coordinates**: Use Custom mode for precise location control

---

**Happy Sailing! ⛵**

Need help? Check the main [README.md](README.md) or open an issue on GitHub.
