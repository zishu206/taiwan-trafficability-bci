# Google Earth Engine (GEE) scripts

The indicator workflow was authored in the **GEE Code Editor**
(https://code.earthengine.google.com). The files in this folder document the full
cloud-side extraction and the local tile merge.

## Files

- **`gee_indicators_13.js`** — the current script matching the published paper. It
  builds the thirteen indicators in four north–south tiles to avoid memory limits,
  applies 2nd–98th percentile directional normalization (larger values = higher
  bearing capacity), and runs `Export.image.toDrive` at 30 m in EPSG:4326. Band
  order: NLI, BD, CLAY, SAL, RELIEF, SLOPE, CURV, DISTW, WDENS, SAR, LST, NDVI,
  LULC. The NLI section documents how to rasterize the engineering-geological
  lithology score (strata obtainable from the public Geology Cloud); the constant
  0.5 line is a runnable placeholder to be replaced by that rasterization.
- **`merge_tiles.py`** — merges the four exported part GeoTIFFs into one
  13-channel raster. Set `INPUT_DIR` to the local folder holding the part files.
- **`archive_15indicators.js`** — the earlier fifteen-indicator version, retained
  for provenance. The final framework removed the NDWI and TWI indicators and
  replaced the NLI placeholder with the real lithology score; all other eleven
  indicators, the data sources, the normalization, and the tiling are unchanged.

The scripts document: Landsat 8/9 `C02/T1_L2` cloud masking and median
compositing; LST calibration; SRTM-based relief and slope (`ee.Terrain.slope`);
Sentinel-1 SAR backscatter; OpenLandMap bulk density (scale factor 10) and clay;
Dynamic World land-cover remapping; water-density and distance-to-water;
2nd–98th percentile directional normalization; band stacking; and
`Export.image.toDrive` at 30 m in EPSG:4326.

## Wet-season (multi-temporal) re-run

`gee_wet_season_template.py` is a Python template for recomputing the **dynamic**
indicators over a wet-season/typhoon window while keeping the static layers and
the AHP weights unchanged. Authenticate with `earthengine authenticate`, complete
the indicator functions, and compare the resulting BCI against the dry-season run
using the same 0.606 / 0.672 breakpoints.
