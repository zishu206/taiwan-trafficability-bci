# Relative Vehicle Trafficability Assessment in the Western Coastal Plain of Taiwan, China

This repository supports the manuscript *A Multi-Source Remote-Sensing and AHP Framework for Relative Vehicle Trafficability Assessment in the Western Coastal Plain of Taiwan, China*.

## Dataset

The 30 m, 13-channel GeoTIFF is archived at Zenodo:

https://doi.org/10.5281/zenodo.24190238

## Current Band Order

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

## Legacy Label Mapping

- BCI corresponds to RTI.
- Archived NAI at the fifth band position corresponds to NRI.
- NVFI denotes the NDVI-based vegetation layer, not a separately calculated FVC product.
- These aliases do not represent different variables.

## Method

- Google Earth Engine indicator preparation
- Directional 2nd–98th percentile normalization
- Three-level analytic hierarchy process
- Native-grid uncertainty, redundancy, scale and scenario analyses

## Scope

RTI is a unitless relative screening score. It is not a measured cone index, bearing capacity, soil strength, vehicle-specific pass/fail result, or vehicle-performance prediction.

## Repository Structure

- `gee/`: Google Earth Engine scripts
- `data/`: data notes and metadata
- Other parameter files: model settings and auxiliary documentation
