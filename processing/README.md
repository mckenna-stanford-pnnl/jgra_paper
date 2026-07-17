# Processing Scripts

This directory contains data processing scripts that transform raw external data into intermediate products used by the analysis scripts.

## Workflow Order

These scripts should be run in the following order to recreate the analysis workflow:

### Step 1: WRF Property Calculation
- **`calc_wrf_properties.ipynb`** - Extract and compute fundamental WRF microphysical properties from 2D/3D model output
- **`calc_wrf_properties_lasso.ipynb`** - Same for LASSO domain (higher-resolutions coarse-grained to 2.5 km)
- **`calc_wrf_properties_lasso_500m.ipynb`** - LASSO at native 500m resolution

### Step 2: DSD Parameter Calculation  
- **`calc_wrf_gamma_properties.ipynb`** - Compute gamma distribution properties for WRF PSDs (3km domain)
- **`calc_wrf_gamma_properties_LASSO.ipynb`** - As above but for LASSO simulations coarse-grained to 2.5 km
- **`calc_wrf_gamma_properties_LASSO_500m_native.ipynb`** - As above but for LASSO simulations at native 500-m grid spacing

### Step 3: Filtering & Classification
- **`filter_wrf_dsd_properties_congestus.ipynb`** - Filter to congestus cloud points (3km)
- **`filter_wrf_dsd_properties_congestus_LASSO.ipynb`** - LASSO congestus filtering
- **`filter_wrf_dsd_properties_congestus_LASSO_500m_native.ipynb`** - LASSO 500m congestus filtering

### Step 4: Observational Data Processing
- **`coarse_grain_csapr.ipynb`** - Coarse-grain CSAPR radar from 500m to model grid
- **`coarse_grain_regrid_csapr.ipynb`** - Coarse-grain CSAPR radar from 500m to 3 km and regrid to model grid
- **`coarse_grain_regrid_csapr_lasso.ipynb`** - Coarse-grain CSAPR radar from 500m to LASSO grid spacings and regrid to model grid

### Step 5: Data Consolidation
- **`consolidate_coarse_grained_csapr_goes.ipynb`** - Merge CSAPR with GOES/SatCORPS cloud products
- **`consolidate_coarse_grained_csapr_goes_2.5km.ipynb`** - 2.5km resolution consolidated product
- **`track_cells_disdrometer_collocation.ipynb`** - Match cells with disdrometer locations
- **`merge_in_situ_probes.ipynb`** - Consolidate multiple probe datasets


## Key Inputs Required

- WRF model output files (2D and 3D; see main README for details)
- CSAPR radar observations from DOE ARM
- Cell tracking data
- Disdrometer measurements
- Updated file paths in each notebook to match your system

## Key Outputs Generated

These scripts generate large intermediate pickle files:

- `wrf_dsd_props_cu_only.p` (1.1 GB)
- `LASSO_d2/3/4_dsd_props_cu_only.p` (125-139 MB each)
- `LASSO_500m_native_dsd_props_cu_only.p` (2.2 GB)
- `wrf_3km_cell_track_reflectivity_disdrometer.p` (118 KB)
- `static_vars.npz` (11 MB)

These files are saved to `generated_data/` directory and consumed by analysis scripts.

## Parallel Processing

Most scripts use Dask for parallelization. Adjust `n_workers` parameter based on your system resources:

```python
cluster = LocalCluster(n_workers=32, threads_per_worker=1)
```


## Notes

- Some scripts use `distributed` computing; ensure sufficient RAM available
- All hard-coded paths should be updated for your system
- See main README for data source locations and external dependencies
