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

### Step 6: Cell Tracking with PyFLEXTRKR

**PyFLEXTRKR** (Python FLEXible object TRacKeR) is a flexible atmospheric feature tracking software package used to track convective clouds. For this project, we apply it to identify and track individual convective cells from WRF model output at high temporal resolution (3.75-minute output).

**Cell Tracking Scripts:**
- **`run_celltracking_cacti_wrf3km_highfreq.sh`** - Bash script to run PyFLEXTRKR cell tracking on high-frequency WRF 3-km simulations
- **`config_wrf_3km_highfreq.yaml`** - Configuration file specifying tracking parameters for WRF reflectivity data

**Key Features:**
- Tracks individual convective cells using radar reflectivity threshold detection
- Provides cell-scale statistics (size, intensity, lifetime, trajectory)
- Generates cell tracking netCDF output and visualization quicklooks
- Supports parallel processing via Dask

**Reference:**
For detailed information about PyFLEXTRKR methodology and capabilities, see:
- Feng et al. (2023): PyFLEXTRKR: a flexible feature tracking Python software for convective cloud analysis. *Geosci. Model Dev.*, 16(10), 2753-2776. https://doi.org/10.5194/gmd-16-2753-2023
- GitHub repository: https://github.com/FlexTRKR/PyFLEXTRKR

## Helper Functions

**`functions.py`** - Contains utility functions frequently used across processing scripts:
- File I/O helpers for netCDF and pickle formats
- Common data transformations and calculations
- Domain utilities (grid definitions, file path helpers)
- Dask/parallel processing convenience functions
- Validation and error-checking utilities

Import and use in your notebooks:
```python
from functions import *  # Import all helpers
```

## Key Inputs Required

- WRF model output files (2D and 3D; see main README for details)
- CSAPR radar observations from DOE ARM
- Cell tracking data
- Disdrometer measurements
- Updated file paths in each notebook to match your system

## Intermediate Files Generated

Each processing script generates intermediate files (stored on HPC scratch space, **NOT in repository**):

### WRF Derived Property Files
- **`calc_wrf_properties.ipynb`** → `/pscratch/sd/m/mckenna/cacti/wrf/derived_3km/WRF_CACTI_3km_derived_YYYYMMDD.nc` (multiple files, one per date; ~50-500 MB each)
- **`calc_wrf_properties_lasso.ipynb`** → `/pscratch/sd/m/mckenna/wrf_lasso/coarse_grained/{date}/{ens}/{domain}/derived/LASSO_CACTI_2.5km_derived_*.nc`
- **`calc_wrf_properties_lasso_500m.ipynb`** → Similar but at native 500m resolution

### WRF DSD Parameters  
- **`calc_wrf_gamma_properties.ipynb`** → `/pscratch/sd/m/mckenna/cacti/wrf/derived_3km_dsd_parameters/WRF_CACTI_3km_DSD_parameters_liq_only_YYYYMMDD.nc` (multiple files; ~100-800 MB each)
- **`calc_wrf_gamma_properties_LASSO.ipynb`** → `/pscratch/sd/m/mckenna/wrf_lasso/coarse_grained/{date}/{ens}/{domain}/derived/LASSO_CACTI_2.5km_DSD_parameters_liq_only_*.nc`
- **`calc_wrf_gamma_properties_LASSO_500m_native.ipynb`** → `/pscratch/sd/m/mckenna/wrf_lasso/500m_wrf_output/{date}/{ens}/derived/LASSO_CACTI_500m_DSD_parameters_liq_only_*.nc`

### Filtered Congestus Parameters  
- **`filter_wrf_dsd_properties_congestus*.ipynb`** (3 variants) → `/pscratch/sd/m/mckenna/cacti/wrf/temp_cong_dsd_params/cong_dsd_params_YYYYMMDD*.npz` and `LASSO_*_cong_dsd_params_*.npz` files

### Coarse-Grained Radar Data
- **`coarse_grain_regrid_csapr.ipynb`** and **`lasso` variant** → Regridded CSAPR `.nc` files

### Consolidated Observational Data
- **`consolidate_coarse_grained_csapr_goes.ipynb`** → `/pscratch/sd/m/mckenna/cacti/matched_csapr_goes/CSAPR_GOES_matched_times_3km_YYYYMMDD.nc`
- **`consolidate_coarse_grained_csapr_goes_2.5km.ipynb`** → `/pscratch/sd/m/mckenna/cacti/matched_csapr_goes/2.5km/CSAPR_GOES_matched_times_2.5km_YYYYMMDD.nc`

### Final Processed Data (saved to `generated_data/`)
- **`track_cells_disdrometer_collocation.ipynb`** → `generated_data/wrf_3km_cell_track_reflectivity_disdrometer.p` (118 KB)
- **`calc_wrf_gamma_properties*.ipynb`** (combined output) → `generated_data/wrf_dsd_props_cu_only.p` (1.1 GB) and LASSO variants
- **`calc_wrf_properties.ipynb`** → `generated_data/static_vars.npz` (11 MB)
- **`merge_in_situ_probes.ipynb`** → `/global/homes/m/mckenna/projdir/cacti/aircraft_in_situ/post/flight_dictionaries_raw_data.p`

These intermediate `.nc` and `.npz` files are essential for the processing chain but require ~50-100 GB of temporary scratch space.

## Parallel Processing

Most scripts use Dask for parallelization. Adjust `n_workers` parameter based on your system resources:

```python
cluster = LocalCluster(n_workers=32, threads_per_worker=1)
```


## Notes

- Some scripts use `distributed` computing; ensure sufficient RAM available
- All hard-coded paths should be updated for your system
- See main README for data source locations and external dependencies
