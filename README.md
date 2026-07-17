# CACTI/LASSO WRF Cloud-Resolving Model Analysis
## Code for Microphysical Property Evaluation and Comparison with Observations

This repository contains analysis code for comparing WRF-simulated cloud microphysical properties with observations from the CACTI campaign. The code processes cloud-resolving WRF simulations and observational data from radar (CSAPR/Taranis), cell tracking for both observations and simulations, aircraft probes, satellite retrievals, and surface measurements at the ARM AMF site. Simulations include a 3-km seasonal simulation and case studies from the ARM Large Eddy Simulation ARM Symbiotic Simulation and Observation (LASSO) CACTI project. 

---

## Table of Contents
- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Data Sources](#data-sources)
- [Workflow](#workflow)
- [Setup & Installation](#setup--installation)
- [Running the Analysis](#running-the-analysis)
- [Generated Data Files](#generated-data-files)
- [Open Research Statement](#open-research-statement)
- [Citation](#citation)
- [Contact](#contact)

---

## Project Overview

This project evaluates WRF-simulated cloud microphysical properties by comparing them against observations collected during the CACTI (Clouds, Aerosol and Complex Terrain Interactions, Oct 2018 - Mar 2019) field campaign (doi: 0.1175/BAMS-D-20-0030.1). WRF simulations include:
- **3-km Seasonal Simulation**: doi: 10.5281/zenodo.10655168
- **LASSO Case Studies (2.5-km, 500-m, & 100-m)** (Large Eddy Simulation ARM Symbiotic Simulation and Observation) project: doi: 10.5439/1905789

The analysis focuses on:
- Cloud top temperature and reflectivity properties
- Drop size distribution (DSD) parameters
- Microphysical property profiles
- Congestus cloud classification
- Cell-by-cell comparisons between model and observations

---

## Directory Structure

This repository contains three main categories of code:

### 1. **processing/** - Data Processing Scripts
Scripts that prepare raw input data and generate intermediate data products. These transform external data sources into standardized formats used by analysis scripts.

**Key Scripts:**
- `calc_wrf_properties.ipynb` - Extract and compute fundamental WRF properties from 2D/3D model output
- `calc_wrf_gamma_properties.ipynb` - Compute gamma distribution parameters for particle size distributions
- `calc_wrf_gamma_properties_LASSO.ipynb` - Same as above but for LASSO domain/resolution
- `calc_wrf_gamma_properties_LASSO_500m_native.ipynb` - LASSO analysis at native 500m resolution
- `filter_wrf_dsd_properties_congestus.ipynb` - Filter WRF output to congestus cloud points
- `filter_wrf_dsd_properties_congestus_LASSO.ipynb` - Congestus filtering for LASSO
- `filter_wrf_dsd_properties_congestus_LASSO_500m_native.ipynb` - Congestus filtering for LASSO 500m
- `coarse_grain_csapr.ipynb` - Coarse-grain observational CSAPR radar data
- `coarse_grain_regrid_csapr.ipynb` - Regrid coarse-grained CSAPR to model grid
- `coarse_grain_regrid_csapr_lasso.ipynb` - Regrid CSAPR for LASSO domain
- `consolidate_coarse_grained_csapr_goes.ipynb` - Merge CSAPR with GOES cloud top products
- `consolidate_coarse_grained_csapr_goes_2.5km.ipynb` - Consolidated product at 2.5 km resolution
- `track_cells_disdrometer_collocation.ipynb` - Match tracked cloud cells with disdrometer measurement locations
- `merge_in_situ_probes.ipynb` - Merge multiple in-situ probe datasets
- `compare_obs_sims_cell_numbers_cong.ipynb` - Compare simulated and observed congestus statistics

**Input Data Requirements:** See [Data Sources](#data-sources) section below.

**Output:** Intermediate pickle files and arrays saved in `generated_data/` (see [Generated Data Files](#generated-data-files))

---

### 2. **analysis/** - Analysis & Plotting Scripts
Scripts that read processed data and generate publication-quality figures. These scripts assume intermediate data products from processing scripts are available.

**Figure Mapping:**
- `plot_fig_1_3_4_5_S5_S6_cell_stats.ipynb` - Figures 1, 3, 4, 5, S5, S6: Cell statistics
- `plot_fig_2_S3_S4_wrf_vs_obs_CTT_col_max_ref.ipynb` - Figures 2, S3, S4: CTT/reflectivity comparison
- `plot_fig_6_7_8_S7_wrf_vs_obs_dsd_properties.ipynb` - Figures 6, 7, 8, S7: DSD properties
- `plot_fig_9_10_11_S8_S9_wrf_obs_disdrometer.ipynb` - Figures 9, 10, 11, S8, S9: Disdrometer comparison
- `plot_fig_12_wrf_vs_obs_CTT_col_max_ref_LASSO.ipynb` - Figure 12: LASSO CTT/reflectivity
- `plot_fig_13_14_wrf_vs_obs_dsd_properties_LASSO.ipynb` - Figures 13, 14: LASSO DSD properties
- `plot_fig_S1_mie_scattering.ipynb` - Figure S1: Mie scattering efficiencies (theory)
- `plot_fig_S2_ctt_CDFs.ipynb` - Figure S2: CTT cumulative distributions
- `plot_fig_S10_wrf_vs_obs_dsd_properties_LASSO_500m_native.ipynb` - Figure S10: LASSO 500m DSD
- `plot_WRF_obs_aero_time_series.ipynb` - Time series analysis of aerosol effects

**Input Data:** Requires intermediate `.p` (pickle) files and `.npz` arrays from `generated_data/` directory.

**Output:** Figure files (typically `.png` and/or `.pdf`) saved to local `figures/` directory or specified path.

---

### 3. **generated_data/** - Intermediate Data Products
Directory containing processed data files generated by processing scripts. These are large binary files (~4+ GB total) generated locally from external data sources (see below).

**Generated Files:**
- `wrf_dsd_props_cu_only.p` (1.1 GB) - Full WRF DSD properties for cumulus-only points (3-km domain)
- `wrf_dsd_props_cu_only_date_lim.p` (110 MB) - Date-limited subset
- `LASSO_d2_dsd_props_cu_only.p` (125 MB) - LASSO domain 2 DSD properties
- `LASSO_d3_dsd_props_cu_only.p` (115 MB) - LASSO domain 3 DSD properties  
- `LASSO_d4_dsd_props_cu_only.p` (139 MB) - LASSO domain 4 DSD properties
- `LASSO_500m_native_dsd_props_cu_only.p` (2.2 GB) - LASSO data at native 500m resolution
- `wrf_3km_cell_track_reflectivity_disdrometer.p` (118 KB) - Matched cell tracks and disdrometer
- `WRF_AMF_NWFA.p` (818 KB) - WRF properties at AMF/NWFA site location
- `static_vars.npz` (11 MB) - Static variables and lookup tables

**Note:** These files are NOT included in the repository due to size. Instructions for regenerating them are provided in the [Workflow](#workflow) section.

---

## Data Sources

This analysis requires external data from the DOE Atmospheric Radiation Measurement (ARM) Program and WRF model output. All external data sources are publicly available.

### External Data Sources (Download Required)

#### 1. **WRF Model Output**
- **Source:** Available upon request from authors (in-house simulations)
- **Contact:** McKenna W. Stanford (mckenna.stanford@pnnl.gov)
- **Description:** 
  - **3-km Seasonal Simulation:** Full CACTI period (Oct 15, 2018 - Mar 3, 2019)
  - **LASSO Case Studies:** Higher-resolution simulations (2.5-km, 500-m, 100-m) for select days
- **DOIs:**
  - 3-km Seasonal Simulation: https://doi.org/10.5281/zenodo.10655168
  - LASSO-CACTI Case Studies: https://doi.org/10.5439/1905789
- **LASSO Bundle Browser:** https://adc.arm.gov/lasso/#/cacti (downloadable case study bundles)
- **Files:** WRF 2D and 3D output files in NetCDF format
- **Directory Structure:** Expected at `/pscratch/sd/m/mckenna/cacti/wrf/` (adjust paths in scripts as needed)

#### 2. **CSAPR Radar - Cloud-Adaptive Scanning Radar (Taranis)**
- **Source:** DOE ARM Data Discovery - [https://adc.arm.gov/](https://adc.arm.gov/)
- **DOI:** https://doi.org/10.5439/2440152
- **Facility Code:** CSAPR (C-band Scanning ARM Precipitation Radar)
- **Product:** `taranis_corcsapr2cfrppiqcM1_gridded.c1`
- **Description:** Attenuation-corrected reflectivity observations
- **Spatial Resolution:** 500 m
- **Temporal Resolution:** 15 minutes
- **Domain:** CACTI experimental domain
- **Expected Directory:** `/global/cfs/projectdirs/m1657/avarble/cacti/Taranis/taranis_corcsapr2cfrppiqcM1_gridded.c1/`

#### 3. **Disdrometer Data**
- **Source:** DOE ARM Data Discovery - [https://adc.arm.gov/](https://adc.arm.gov/)
- **DOIs:**
  - Video Disdrometer (VDIS): https://doi.org/10.5439/1992988
  - Laser Disdrometer (LD): https://doi.org/10.5439/1973058
  - Video Disdrometer VAP (VDISQUANTS): https://doi.org/10.5439/1592683
  - Laser Disdrometer VAP (LDQUANTS): https://doi.org/10.5439/1432694
- **Instrument:** 2DVD (Two-Dimensional Video Disdrometer) & Laser Disdrometer
- **Description:** Drop size distribution measurements from in-situ probes
- **Expected Directory:** `/global/homes/m/mckenna/cacti_data/disdrometer/` (adjust as needed)

#### 4. **Cell Tracking Data (Observational)**
- **Source:** Zenodo & DOE ARM Data Discovery
- **DOIs:** 
  - WRF Simulation & Cell Tracks (15-min): https://doi.org/10.5281/zenodo.10655168
  - PyFLEXTRKR Configuration: https://doi.org/10.5281/zenodo.13760823
- **Temporal Resolution:** 
  - 15-minute intervals (main product for Figures 1, 3, 4, 5, S5, S6, S7)
  - 3.75-minute intervals (higher resolution available; scripts upon request)
- **Description:** Tracked cloud cells collocated with AMF site for disdrometer comparisons
- **Expected Directory:** `/global/homes/m/mckenna/cacti_data/cell_tracks/`
- **Note:** Higher temporal resolution tracking available from authors (mckenna.stanford@pnnl.gov)

#### 5. **Satellite Data - GOES-16**
- **Source:** DOE ARM Data Discovery - [https://adc.arm.gov/](https://adc.arm.gov/)
- **DOI:** https://doi.org/10.5439/2008448
- **Product:** Parallax-corrected VISST-derived pixel level products from satellite GOES-16
- **Description:** Cloud-top temperature and optical properties from satellite retrievals
- **Temporal Resolution:** High-frequency satellite observations
- **Domain:** CACTI experimental domain

#### 6. **Aircraft In-Situ Data**
- **Source:** DOE ARM Data Discovery - [https://adc.arm.gov/](https://adc.arm.gov/)
- **Instruments:**
  - **Fast Cloud Droplet Probe (AAFFCDP):** https://doi.org/10.5439/1417472
    - Cloud droplet size distributions and concentrations
  - **2 Dimensional Stereo Probe (AAF2DSH):** https://doi.org/10.5439/1419322
    - Particle imaging and sizing
  - **High Volume Precipitation Spectrometer (AAFHVPS):** https://doi.org/10.5439/1417471
    - Precipitation particle size distributions
- **Description:** Aircraft-based microphysical observations from the ARM Mobile Facility (AMF)
- **Platform:** Gulfstream-1 research aircraft during CACTI field campaign

### Supplementary Data
- **WRF Matched File Lists:** Generated for performance (see `processing/calc_wrf_properties.ipynb`)

---

## Workflow

The analysis follows a pipeline of interdependent processing and analysis steps:

```
EXTERNAL DATA
    ↓
    ├─→ WRF Model Output (3D/2D)
    ├─→ CSAPR Radar Observations  
    ├─→ Cell Tracking Data
    └─→ Disdrometer Measurements
    
    ↓
[1. PROCESSING SCRIPTS]
    
    ├─→ calc_wrf_properties.ipynb
    │   └─→ Extracts WRF microphysical variables, Mie theory calcs
    │
    ├─→ calc_wrf_gamma_properties*.ipynb (3 variants)
    │   └─→ Fits gamma distributions to WRF PSDs
    │       └─→ Generates wrf_dsd_props_cu_only.p, LASSO_d*.p
    │
    ├─→ filter_wrf_dsd_properties_congestus*.ipynb (3 variants)
    │   └─→ Filters by CTT, altitude, cloud type
    │       └─→ Creates filtered DSD datasets
    │
    ├─→ coarse_grain_csapr.ipynb + regrid variants
    │   └─→ Coarse-grains CSAPR from 500m to model grid
    │       └─→ Regrids to WRF coordinates
    │
    ├─→ consolidate_coarse_grained_csapr_goes*.ipynb
    │   └─→ Merges CSAPR reflectivity with GOES cloud products
    │
    ├─→ track_cells_disdrometer_collocation.ipynb
    │   └─→ Matches cells with disdrometer locations
    │       └─→ Generates wrf_3km_cell_track_reflectivity_disdrometer.p
    │
    ├─→ merge_in_situ_probes.ipynb
    │   └─→ Consolidates probe measurements
    │
    └─→ compare_obs_sims_cell_numbers_cong.ipynb
        └─→ Statistical comparisons
    
    ↓
[GENERATED DATA PRODUCTS]
    
    ├─→ wrf_dsd_props_cu_only.p
    ├─→ LASSO_d2/3/4_dsd_props_cu_only.p
    ├─→ LASSO_500m_native_dsd_props_cu_only.p
    ├─→ wrf_3km_cell_track_reflectivity_disdrometer.p
    ├─→ WRF_AMF_NWFA.p
    ├─→ static_vars.npz
    
    ↓
[2. ANALYSIS SCRIPTS]
    
    ├─→ plot_fig_1,3,4,5_S5,S6_cell_stats.ipynb
    ├─→ plot_fig_2_S3,S4_wrf_vs_obs_CTT_col_max_ref.ipynb
    ├─→ plot_fig_6,7,8_S7_wrf_vs_obs_dsd_properties.ipynb
    ├─→ plot_fig_9,10,11_S8,S9_wrf_obs_disdrometer.ipynb
    ├─→ plot_fig_12_wrf_vs_obs_CTT_col_max_ref_LASSO.ipynb
    ├─→ plot_fig_13,14_wrf_vs_obs_dsd_properties_LASSO.ipynb
    ├─→ plot_fig_S1_mie_scattering.ipynb
    ├─→ plot_fig_S2_ctt_CDFs.ipynb
    ├─→ plot_fig_S10_wrf_vs_obs_dsd_properties_LASSO_500m_native.ipynb
    └─→ plot_WRF_obs_aero_time_series.ipynb
    
    ↓
[PUBLICATION FIGURES]
    
    ├─→ figure_1.png, figure_3.png, ... (all main and supplementary figures)
```

### Dependencies Between Scripts

**Must Run Before:**

1. **For DSD Analysis Figures** (6, 7, 8, 13, 14, S11):
   - `calc_wrf_gamma_properties*.ipynb` → `filter_wrf_dsd_properties_congestus*.ipynb` → plotting

2. **For CTT/Reflectivity Comparison** (Figures 2, 12, S3, S4):
   - `coarse_grain_csapr.ipynb` → `coarse_grain_regrid_csapr*.ipynb` → `consolidate_coarse_grained_csapr_goes*.ipynb` → plotting

3. **For Cell Statistics** (Figures 1, 3, 4, 5, S5, S6, S7):
   - Observational cell tracking data → plotting

4. **For Disdrometer Comparison** (Figures 9, 10, 11, S9, S10):
   - `track_cells_disdrometer_collocation.ipynb` → plotting

---

## Setup & Installation

### Prerequisites
- Python 3.7+ (tested with Python 3.9)
- Jupyter Notebook or JupyterLab
- Required packages (see `environment.yml` or install below)

### Create Environment

```bash
# Option 1: Using conda (recommended)
conda create -n cacti-analysis python=3.9
conda activate cacti-analysis
conda install -c conda-forge xarray dask distributed numpy scipy matplotlib pandas cartopy miepython

# Option 2: Using pip
pip install xarray dask[complete] numpy scipy matplotlib pandas cartopy miepython
```

### Optional Dependencies
- `numba` - for numerical optimization
- `palettable` - for advanced color schemes
- `scikit-learn` - for Gaussian mixture modeling

### Download External Data
1. Visit [DOE ARM Data Discovery](https://adc.arm.gov/)
2. Search for and download:
   - CSAPR Taranis product (`taranis_corcsapr2cfrppiqcM1_gridded.c1`)
   - Disdrometer (2DVD) data
   - Cell tracking observations (15-min)
3. Contact authors for WRF output files
4. Update file paths in scripts to match your data locations

---

## Running the Analysis

### To Regenerate All Intermediate Data (Processing Phase)
```bash
jupyter notebook
# Open each script in processing/ sequentially in the order shown in Workflow section
# Note: This requires external data sources (see Data Sources)
# Processing time: ~48-72 hours on HPC system with parallelization
```

### To Generate Figures Only (Analysis Phase - If Data Available)
```bash
jupyter notebook
# Open scripts from analysis/ directory
# Generate publication-quality figures
```

### Individual Script Execution
Each notebook is designed to be run independently if intermediate data is available:

```bash
# Example: Generate a specific figure
jupyter notebook analysis/plot_fig_6_7_8_S7_wrf_vs_obs_dsd_properties.ipynb
```

### Important Notes:
- **Dask Parallelization:** Processing scripts use Dask for parallel computation. Adjust `n_workers` parameter in scripts for your system resources.
- **Memory Requirements:** Some scripts require 64+ GB RAM for full CACTI domain analysis. Adjust temporal subsetting if needed.
- **File Paths:** Update all hard-coded paths in scripts to match your data directory structure

---

## Generated Data Files

Intermediate data products generated during processing phase:

| File | Size | Generated By | Used By |
|------|------|-------------|---------|
| `wrf_dsd_props_cu_only.p` | 1.1 GB | `calc_wrf_gamma_properties.ipynb` | Figure 6-8 analysis |
| `wrf_dsd_props_cu_only_date_lim.p` | 110 MB | `calc_wrf_gamma_properties.ipynb` | Subset analysis |
| `LASSO_d2_dsd_props_cu_only.p` | 125 MB | `calc_wrf_gamma_properties_LASSO.ipynb` | Figure 13-14 (domain 2) |
| `LASSO_d3_dsd_props_cu_only.p` | 115 MB | `calc_wrf_gamma_properties_LASSO.ipynb` | Figure 13-14 (domain 3) |
| `LASSO_d4_dsd_props_cu_only.p` | 139 MB | `calc_wrf_gamma_properties_LASSO.ipynb` | Figure 13-14 (domain 4) |
| `LASSO_500m_native_dsd_props_cu_only.p` | 2.2 GB | `calc_wrf_gamma_properties_LASSO_500m_native.ipynb` | Figure S11 |
| `wrf_3km_cell_track_reflectivity_disdrometer.p` | 118 KB | `track_cells_disdrometer_collocation.ipynb` | Figures 9-11 |
| `WRF_AMF_NWFA.p` | 818 KB | `calc_wrf_properties.ipynb` | Site-specific analysis |
| `static_vars.npz` | 11 MB | `calc_wrf_properties.ipynb` | Multiple scripts |

**Regeneration Instructions:**
- Delete `.p` and `.npz` files
- Run processing scripts in workflow order
- **Time estimate:** 48-72 hours with HPC parallelization

---

## Repository Organization

```
.
├── README.md                          # This file
├── processing/                        # Data processing scripts
│   ├── calc_wrf_properties.ipynb
│   ├── calc_wrf_gamma_properties.ipynb
│   ├── calc_wrf_gamma_properties_LASSO.ipynb
│   ├── calc_wrf_gamma_properties_LASSO_500m_native.ipynb
│   ├── filter_wrf_dsd_properties_congestus.ipynb
│   ├── filter_wrf_dsd_properties_congestus_LASSO.ipynb
│   ├── filter_wrf_dsd_properties_congestus_LASSO_500m_native.ipynb
│   ├── coarse_grain_csapr.ipynb
│   ├── coarse_grain_regrid_csapr.ipynb
│   ├── coarse_grain_regrid_csapr_lasso.ipynb
│   ├── consolidate_coarse_grained_csapr_goes.ipynb
│   ├── consolidate_coarse_grained_csapr_goes_2.5km.ipynb
│   ├── track_cells_disdrometer_collocation.ipynb
│   ├── merge_in_situ_probes.ipynb
│   └── compare_obs_sims_cell_numbers_cong.ipynb
│
├── analysis/                          # Analysis and plotting scripts
│   ├── plot_fig_1_3_4_5_S5_S6_S7_cell_stats.ipynb
│   ├── plot_fig_2_S3_S4_wrf_vs_obs_CTT_col_max_ref.ipynb
│   ├── plot_fig_6_7_8_S7_wrf_vs_obs_dsd_properties.ipynb
│   ├── plot_fig_9_10_11_S9_S10_wrf_obs_disdrometer.ipynb
│   ├── plot_fig_12_wrf_vs_obs_CTT_col_max_ref_LASSO.ipynb
│   ├── plot_fig_13_14_wrf_vs_obs_dsd_properties_LASSO.ipynb
│   ├── plot_fig_S1_mie_scattering.ipynb
│   ├── plot_fig_S2_ctt_CDFs.ipynb
│   ├── plot_fig_S11_wrf_vs_obs_dsd_properties_LASSO_500m_native.ipynb
│   └── plot_WRF_obs_aero_time_series.ipynb
│
├── generated_data/                    # Intermediate pickle files (git-ignored)
│   ├── wrf_dsd_props_cu_only.p
│   ├── LASSO_d2_dsd_props_cu_only.p
│   ├── LASSO_d3_dsd_props_cu_only.p
│   ├── LASSO_d4_dsd_props_cu_only.p
│   ├── LASSO_500m_native_dsd_props_cu_only.p
│   ├── wrf_3km_cell_track_reflectivity_disdrometer.p
│   ├── WRF_AMF_NWFA.p
│   └── static_vars.npz
│
├── .gitignore                         # Git ignore patterns
│   (generated_data/ directory)
│   (output figures/)
│   (cache directories)
│
└── .ipynb_checkpoints/                # Jupyter checkpoints (git-ignored)
```

---

## Troubleshooting

### Common Issues

**Issue:** Dask workers fail with memory error
- **Solution:** Reduce `n_workers` in scripts or reduce temporal domain

**Issue:** File path errors
- **Solution:** Update all hardcoded paths to match your system

**Issue:** Missing external data
- **Solution:** Download from DOE ARM Data Discovery (see Data Sources section)

**Issue:** Import errors for `functions` module
- **Solution:** Utility functions are defined inline in notebooks

---

## Open Research Statement

Code used to generate analyses and plots in this study are available on GitHub ([github.com/mckenna-stanford-pnnl/jgra_paper](https://github.com/mckenna-stanford-pnnl/jgra_paper); Zenodo DOI will be minted upon publication).

All observational datasets are available for download via the ARM Data Discovery website ([https://adc.arm.gov/discovery/](https://adc.arm.gov/discovery/#/)), including:
- C-SAPR2 Taranis Dataset (https://doi.org/10.5439/2440152)
- Video Disdrometer Drop Size Distributions - VDIS (https://doi.org/10.5439/1992988)
- Laser Disdrometer Drop Size Distributions - LD (https://doi.org/10.5439/1973058)
- Video Disdrometer VAP - VDISQUANTS (https://doi.org/10.5439/1592683)
- Laser Disdrometer VAP - LDQUANTS (https://doi.org/10.5439/1432694)
- Parallax-corrected VISST-derived pixel level products from satellite GOES-16 (https://doi.org/10.5439/2008448)
- Aircraft Fast Cloud Droplet Probe - AAFFCDP (https://doi.org/10.5439/1417472)
- Aircraft 2 Dimensional Stereo Probe - AAF2DSH (https://doi.org/10.5439/1419322)
- Aircraft High Volume Precipitation Spectrometer - AAFHVPS (https://doi.org/10.5439/1417471)

ARM LASSO-CACTI simulations are available for download via the LASSO-CACTI Bundle Browser ([https://adc.arm.gov/lasso/#/cacti](https://adc.arm.gov/lasso/#/cacti); https://doi.org/10.5439/1905789), with details provided at [https://lasso-cacti-doc.arm.gov/latest/citing_LASSO.html](https://lasso-cacti-doc.arm.gov/latest/citing_LASSO.html).

---

## Citation

If you use this code, please cite:
- The associated journal paper (publication details will be added upon acceptance)
- DOE ARM data products via provided DOIs
- WRF simulations via provided Zenodo DOI
- LASSO-CACTI simulations via https://doi.org/10.5439/1905789

---

## Contact & Support

**Author:** McKenna W. Stanford  
**Email:** mckenna.stanford@pnnl.gov  
**Affiliation:** Pacific Northwest National Laboratory

For issues with external data sources:
- **ARM Archive:** [https://adc.arm.gov/](https://adc.arm.gov/)
- **LASSO Documentation:** [https://adc.arm.gov/lasso](https://adc.arm.gov/lasso)

---

## License

This code repository is provided as-is for scientific research purposes. Please see the LICENSE file for specific terms.

---

## Changelog

**Version 1.0** (July 2026)
- Publication-ready code organization
- Complete workflow documentation
- Full data source citations with DOIs
- Open Research section per JGRA requirements
- Zenodo DOI pending upon publication
