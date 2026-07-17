# Analysis & Plotting Scripts

This directory contains Jupyter notebooks that generate publication-quality figures for the paper. These scripts read processed data from the `generated_data/` directory and create plots for the main text and supplementary materials.

## Figure Mapping

### Main Text Figures

| Script | Figures | Description |
|--------|---------|-------------|
| `plot_fig_1_3_4_5_S5_S6_cell_stats.ipynb` | 1, 3, 4, 5, S5, S6, S7 | Cell statistics and properties |
| `plot_fig_2_S3_S4_wrf_vs_obs_CTT_col_max_ref.ipynb` | 2, S3, S4 | Cloud top temperature & max reflectivity (CACTI 3km) |
| `plot_fig_6_7_8_S7_wrf_vs_obs_dsd_properties.ipynb` | 6, 7, 8, S7 | Drop size distribution properties (CACTI) |
| `plot_fig_9_10_11_S8_S9_wrf_obs_disdrometer.ipynb` | 9, 10, 11, S8, S9, S10 | Disdrometer comparisons |
| `plot_fig_12_wrf_vs_obs_CTT_col_max_ref_LASSO.ipynb` | 12 | Cloud top temperature & reflectivity (LASSO 3km) |
| `plot_fig_13_14_wrf_vs_obs_dsd_properties_LASSO.ipynb` | 13, 14 | Drop size distribution properties (LASSO) |

### Supplementary Figures

| Script | Figures | Description |
|--------|---------|-------------|
| `plot_fig_S1_mie_scattering.ipynb` | S1 | Mie scattering efficiency calculations (theory) |
| `plot_fig_S2_ctt_CDFs.ipynb` | S2 | Cloud top temperature CDFs |
| `plot_fig_S11_wrf_vs_obs_dsd_properties_LASSO_500m_native.ipynb` | S11 | DSD properties at LASSO 500m resolution |

### Additional Analysis

| Script | Purpose |
|--------|---------|
| `plot_WRF_obs_aero_time_series.ipynb` | Time series analysis of aerosol and cloud properties |

## Required Data Files

All analysis scripts require the following files from `generated_data/` directory:

- `wrf_dsd_props_cu_only.p` - For CACTI figures (6-11)
- `wrf_dsd_props_cu_only_date_lim.p` - Temporal subset
- `LASSO_d2_dsd_props_cu_only.p` - LASSO domain 2
- `LASSO_d3_dsd_props_cu_only.p` - LASSO domain 3
- `LASSO_d4_dsd_props_cu_only.p` - LASSO domain 4
- `LASSO_500m_native_dsd_props_cu_only.p` - LASSO 500m (Figure S11)
- `wrf_3km_cell_track_reflectivity_disdrometer.p` - Disdrometer collocation
- `WRF_AMF_NWFA.p` - Site-specific properties
- `static_vars.npz` - Lookup tables and constants

## Running the Scripts

### Option 1: Run All Figures
```bash
jupyter notebook
# Open each script and run cells sequentially
```

### Option 2: Run Specific Figure
```bash
# Generate only Figure 6-8
jupyter notebook plot_fig_6_7_8_S7_wrf_vs_obs_dsd_properties.ipynb
```

### Option 3: Batch Processing
```bash
# Run all notebooks sequentially (if nbconvert installed)
# for notebook in *.ipynb; do jupyter nbconvert --to notebook --execute "$notebook"; done
```

## Output Locations

Figures are typically saved to a local `figures/` directory or specified path in each notebook. Update the `save_path` variable in each script to customize output location:

```python
save_path = '/global/homes/m/mckenna/figures/cacti/'
```

## Customization

### Change Figure Format
Most scripts allow customization of output format and DPI:

```python
plt.savefig(f'{save_path}figure_X.png', dpi=300, bbox_inches='tight')
```

### Adjust Plot Appearance
Modify matplotlib settings:

```python
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['text.usetex'] = True  # Use LaTeX rendering
```

## Troubleshooting

### Issue: Missing data files
- **Solution:** Ensure `generated_data/` directory has all required `.p` and `.npz` files from processing scripts

### Issue: Figure output not saving
- **Solution:** Check that `save_path` directory exists and you have write permissions

### Issue: Import errors
- **Solution:** Install required packages (see main README for environment setup)

### Issue: LaTeX rendering errors
- **Solution:** Either set `plt.rcParams['text.usetex'] = False` or install LaTeX/dvipng

## Notes

- All scripts use LaTeX for text rendering (configurable)
- Cartopy is used for map projections in some figures
- Matplotlib version compatibility: tested with 3.3+
- Memory requirements: ~16 GB for full LASSO analysis figures

## Dependencies

Key packages used:
- `xarray` - Data handling
- `numpy/scipy` - Numerical operations
- `matplotlib/cartopy` - Plotting & maps
- `pandas` - Data frames
- `sklearn` - Statistical methods
