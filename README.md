# Dataset

The derived 13-channel raster used by all scripts is archived on **Zenodo** (a free,
long-term repository that issues a persistent DOI). It is not stored in this Git
repository because it exceeds GitHub's 100 MB per-file limit.

## Files (Zenodo record)

| File | Description | Size |
|---|---|---|
| `TaiXi_13indicators_30m.tif` | 13 normalized indicators, 30 m, WGS-84 (EPSG:4326), LZW, BigTIFF | ~799 MB |

- Band order: NLI, NBD, NCLAY, NSAL, NAI, NSI, NCUR, NDW, NWDI, NSAR, NLST, NVFI, NLULC.
- All values are in 0–1; larger values indicate higher bearing capacity.
- SHA-256 checksum: `3538AFC00224A03E45166132CD9CF45D837ACC5796873938246EF07858F18655`
- Zenodo DOI: `10.5281/zenodo.24190239` (https://doi.org/10.5281/zenodo.24190239)

After downloading, point the `SRC` / path constants in the scripts to this file.

> Do not add the regional groundwater monitoring records to this public dataset.
> They are restricted and are only available as aggregated statistics from the
> corresponding author upon reasonable request.
