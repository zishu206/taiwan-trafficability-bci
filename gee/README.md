# Google Earth Engine (GEE) scripts

The cloud-side indicator workflow was authored in the **GEE Code Editor**
(https://code.earthengine.google.com), which keeps scripts online rather than as
local files. To include it in this repository:

1. Open the GEE Code Editor and select the script that builds the indicators.
2. Use the editor's download/export option, or select all, copy, and paste the
   JavaScript into a new file here named `gee_indicators.js`.
3. The script should document: Landsat 8/9 `C02/T1_L2` cloud masking and annual
   median compositing; MNDWI/NDVI via `normalizedDifference`; LST calibration;
   SRTM-based relief and slope (`ee.Terrain.slope`); water-density and lithology
   rasterization; 2nd–98th percentile directional normalization; band stacking;
   and `Export.image.toDrive` at 30 m in EPSG:4326.

## Wet-season (multi-temporal) re-run

`gee_wet_season_template.py` is a Python template for recomputing the **dynamic**
indicators over a wet-season/typhoon window while keeping the static layers and
the AHP weights unchanged. Authenticate with `earthengine authenticate`, complete
the indicator functions, and compare the resulting BCI against the dry-season run
using the same 0.606 / 0.672 breakpoints.
