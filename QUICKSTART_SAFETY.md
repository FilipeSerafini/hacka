# 🚀 Quick Start Guide - AI Safety Features

Get started with the AI-powered route safety analysis in under 5 minutes!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

New dependencies for safety features:
- `shapely==2.0.2` - Geometric operations for hazard detection

## 2. Run the Application

```bash
streamlit run app.py
# or
./run.sh
```

The app will open in your browser at `http://localhost:8501`

## 3. Test a High-Risk Route

Let's test a route that goes through known hazardous areas:

1. **Select Origin**: Choose **"Dubai, UAE"** from the dropdown
2. **Select Destination**: Choose **"Singapore"**
3. **Click**: "🗺️ Generate Route"

### What You'll See:

#### ⚠️ Warning Message
```
🔄 Route rerouted to avoid high risk areas. Original route was unsafe.
```

#### 🗺️ Interactive Map
- **Orange/Red polygons**: Hazardous zones (Gulf of Aden, Malacca Strait)
- **Color-coded route**: Shows risk level
- **Warning marker**: Safety waypoint if route was modified

#### 🛡️ Safety Report
```
⚠️ ROUTE STATUS: MEDIUM RISK

2 hazard(s) detected along this route.

Detected Hazards:
1. Gulf of Aden - High Piracy Risk
   - Type: Piracy
   - Severity: HIGH
   - Description: Active piracy zone near Somalia coast...
   - Route affected: 15.3%
   - Incidents reported: 47

2. Malacca Strait - Piracy Alert
   - Type: Piracy
   - Severity: MEDIUM
   - Description: Narrow strait with occasional piracy...
   - Route affected: 8.7%
   - Incidents reported: 23

Recommendations:
⚠️ CAUTION: Route passes through piracy zones.
Consider alternative route or proceed with caution.
```

## 4. Test a Safe Route

Now try a route with no hazards:

1. **Origin**: **"Le Havre, France"**
2. **Destination**: **"Hamburg, Germany"**
3. **Generate Route**

### What You'll See:

#### ✅ Success Message
```
✅ Safe route generated successfully! No hazards detected.
```

#### 🗺️ Map
- **Green route line**: Indicates safe passage
- **No hazard polygons**: Clear path

#### 🛡️ Safety Report
```
✅ ROUTE STATUS: SAFE

No hazards detected along this route.

Recommendations:
✅ Route is clear of all known hazards. Safe to proceed.
```

## 5. Explore Hazard Statistics

Check the sidebar for live hazard information:

### ⚠️ Active Hazard Zones
- **Total Active Hazards**: 12

### 📊 Hazard Statistics
Click to expand and see:
- **By Severity**: High: 6, Medium: 5, Low: 1
- **By Type**: Piracy: 4, Storm: 4, High Winds: 1, etc.

## 6. Test Routes to Try

### High-Risk Routes (Will Trigger Alerts)
1. **Santos, Brazil** → **Tianjin, China**
   - Passes through: Gulf of Aden, Red Sea, Malacca Strait, South China Sea
   - Expected: Multiple high-risk warnings

2. **New York, USA** → **Cape Town, South Africa**
   - Passes through: Gulf of Guinea
   - Expected: Piracy warnings

3. **Mumbai, India** → **Singapore**
   - Passes through: Bay of Bengal (cyclone season)
   - Expected: Storm warnings

### Low-Risk Routes (Should Be Safe)
1. **Los Angeles** → **San Francisco** (coastal)
2. **Hamburg** → **Rotterdam** (short European route)
3. **Sydney** → **Melbourne** (Australian coast)

## 7. Programmatic Usage

Run the example script to see safety analysis in action:

```bash
python example_safety_check.py
```

This will analyze 5 different routes and show detailed safety reports.

## 8. Understanding the Colors

### Route Colors
- 🟢 **Green**: Safe - No hazards detected
- 🔵 **Blue**: Low risk - Minor advisory
- 🟠 **Orange**: Medium risk - Caution advised
- 🔴 **Red**: High risk - Danger, avoid if possible

### Hazard Zone Colors
- 🟡 **Yellow**: Low severity hazard
- 🟠 **Orange**: Medium severity hazard
- 🔴 **Red**: High severity hazard

### Markers
- 🔵 **Blue anchor**: Origin port
- 🔴 **Red anchor**: Destination port
- 🟠 **Warning triangle**: Safety waypoint (route was modified)

## 9. Key Tips

### Route Safety
- ✅ **Always check the safety report** before proceeding
- ✅ **Green routes are ideal** - no known hazards
- ⚠️ **Orange routes require caution** - monitor conditions
- 🚨 **Red routes are dangerous** - strongly consider alternatives

### Interpreting Results
- **Percentage Affected**: How much of your route passes through the hazard
- **Reported Incidents**: Number of recent incidents in that zone
- **Recommendations**: AI-generated advice based on risk level

### Route Optimization
- System automatically attempts up to **3 rerouting iterations**
- Waypoints are added to **bypass high-risk areas**
- Trade-off information shows **distance vs. safety**

## 10. Advanced Features

### Export Route with Safety Data
1. Generate your route
2. Review the safety analysis
3. Click "Download GeoJSON" to export
4. GeoJSON includes route geometry and properties

### Customize Your Analysis

Edit `hazardous_zones.json` to:
- Add new hazard zones
- Modify severity levels
- Disable zones temporarily (`"active": false`)
- Update incident counts

## Quick Reference

### Hazard Types Monitored
| Icon | Type | Examples |
|------|------|----------|
| 🏴‍☠️ | Piracy | Gulf of Aden, Malacca Strait |
| 🌪️ | Storms | South China Sea, Bay of Bengal |
| 🌊 | High Winds | Red Sea |
| 🧊 | Ice | Bering Sea |
| 🌋 | Volcanic | Sunda Strait |
| 🚢 | High Traffic | East China Sea |

### Status Indicators
| Status | Meaning | Action |
|--------|---------|--------|
| ✅ Safe | No hazards | Proceed |
| ℹ️ Low | Minor advisory | Monitor |
| ⚠️ Medium | Caution needed | Review carefully |
| 🚨 High | Dangerous | Find alternative |

## Need Help?

- **Full Documentation**: See [AI_SAFETY_FEATURES.md](AI_SAFETY_FEATURES.md)
- **Code Examples**: See [example_safety_check.py](example_safety_check.py)
- **General Usage**: See [README.md](README.md)

---

**Ready to generate safe routes? Fire up the app and start exploring! ⛵🛡️**
