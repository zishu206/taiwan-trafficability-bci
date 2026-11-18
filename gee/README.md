# Google Earth Engine Processing Notes

This folder contains the Google Earth Engine scripts used to prepare candidate indicators for the relative vehicle trafficability assessment.

## Current Terminology

- RTI: Relative Trafficability Index, the current continuous relative-screening output.
- NRI: Normalized Rainfall Index, the current name for the fifth-band indicator.
- BCI in legacy scripts corresponds to RTI.
- NAI in the fifth band position corresponds to NRI.
- NVFI denotes the NDVI-based vegetation layer, not a separately calculated FVC product.
- These aliases do not represent different variables.

## Current 13-Band Order

1. NLI
2. NBD
3. NCLAY
4. NSAL
5. NRI
6. NSI
7. NCUR
8. NDW
9. NWDI
10. NSAR
11. NLST
12. NVFI
13. NLULC

## Processing Notes

- Dynamic composites cover 2022–2023.
- Landsat 8/9 and Sentinel-1 inputs are summarized as full-period median composites.
- Dynamic World is represented by its modal land-cover label.
- The implemented SAL input is √(R × NIR).
- Indicator normalization uses directional 2nd–98th percentile normalization.
- The main-map filter is 5 × 5.
- The 7 × 7 filter is used only for sensitivity comparison.
- The final class breaks are 0.606 and 0.672.

## Scope

RTI is a unitless relative screening score. It is not a measured cone index, bearing capacity, soil strength, vehicle-specific pass/fail result, or vehicle-performance prediction.

The complete 13-channel GeoTIFF is archived at Zenodo:

https://doi.org/10.5281/zenodo.24190238
