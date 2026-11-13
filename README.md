# Multi-Source Remote-Sensing Indicators and AHP for Vehicle Trafficability on the Western Coastal Plain of Taiwan

This repository contains the reproducible code for the study *"Multi-Source Normalized Remote-Sensing Indicators and the Analytic Hierarchy Process for Evaluating Vehicle Trafficability and Bearing Capacity on the Western Coastal Plain of Taiwan, China."*

The framework derives thirteen normalized indicators from Google Earth Engine (GEE), combines them with a three-level analytic hierarchy process (AHP), computes a per-pixel bearing capacity index (BCI), and reports a set of robustness and uncertainty analyses. The BCI is presented as a **relative proxy zoning framework**, not as an independently validated mechanical strength map.

## Repository structure

```
.
├── data/                       # How to obtain the dataset (archived on Zenodo)
├── gee/                        # GEE notes and the wet-season re-run template
├── src/
│   ├── 01_build_indicators/    # Indicator assembly, AHP weights, collinearity, QA
│   ├── 02_bci_and_grading/     # Study-area mask, BCI, grading, majority filter
│   ├── 03_robustness_analysis/ # Soft-soil compression, redundancy, coarse
│   │                           # resolution, breakpoint bands, rain scenario
│   └── 04_figures/             # Reproducible plotting scripts
├── requirements.txt
├── LICENSE
└── CITATION.cff
```

## Requirements

- Python 3.10+
- Install dependencies with `python -m pip install -r requirements.txt`

## Reproducing the analysis

1. Download the 13-channel GeoTIFF from the Zenodo record listed in [`data/README.md`](data/README.md) and place it under a local data folder.
2. The scripts retain the original absolute input paths. Before running, edit the path constants at the top of each script (e.g. `SRC`, `OUT`, `MASK`) to match your local folders.
3. Run in order:
   - `src/01_build_indicators/` — indicator assembly, AHP weights, collinearity/VIF and QA;
   - `src/02_bci_and_grading/` — build the mask, compute BCI and the three-grade classification, then apply the 3×3 majority filter;
   - `src/03_robustness_analysis/` — soft-soil mean reversion, NAI/NSI redundancy, coarse-resolution block variance, breakpoint uncertainty bands, and the saturation (rain) scenario;
   - `src/04_figures/` — regenerate the maps.
4. The GEE cloud-side indicator script is authored in the GEE Code Editor; see [`gee/README.md`](gee/README.md) for exporting it. The wet-season multi-temporal re-run template is provided in `gee/`.

## Data availability and restricted records

The derived 13-channel GeoTIFF and the code are archived publicly (this repository and the Zenodo DOI in `data/README.md`). The regional groundwater monitoring records are governed by restricted data-use terms and are **not redistributed** here; aggregated statistics are available from the corresponding author upon reasonable request.

## License

The code is released under the MIT License (see [`LICENSE`](LICENSE)). The underlying satellite and soil products retain their original licenses.

## Citation

Please cite the associated paper; see [`CITATION.cff`](CITATION.cff).
