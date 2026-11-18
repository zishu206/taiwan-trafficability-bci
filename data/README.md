# Dataset

The derived 13-channel raster used by the scripts is archived on **Zenodo**, a long-term repository that provides a persistent DOI. It is not stored in this Git repository because it exceeds GitHub’s 100 MB per-file limit.

## Files (Zenodo record)

| File | Description | Size |
|---|---|---|
| `TaiXi_13indicators_30m.tif` | 13 normalized indicators, 30 m, WGS-84 (EPSG:4326), LZW-compressed BigTIFF | 837.6 MB |

- Band order: NLI, NBD, NCLAY, NSAL, NRI, NSI, NCUR, NDW, NWDI, NSAR, NLST, NVFI, NLULC.
- All values are in 0–1; larger values indicate relatively more favorable trafficability conditions within the study framework.
- SHA-256 checksum: `3538AFC00224A03E45166132CD9CF45D837ACC5796873938246EF07858F18655`
- Zenodo concept DOI: 10.5281/zenodo.24190238
- Zenodo URL: https://doi.org/10.5281/zenodo.24190238
- Legacy mapping: BCI corresponds to RTI; archived NAI at the fifth band corresponds to NRI.
- These aliases do not represent different variables.

After downloading, point the path constants in the scripts to this file.

Do not add regional groundwater monitoring records to this public dataset. They are restricted and are available only as aggregated statistics from the corresponding author upon reasonable request.

