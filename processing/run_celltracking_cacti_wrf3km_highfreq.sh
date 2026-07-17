#!/bin/bash
###############################################################################################
# This script demonstrates running cell tracking on SAAG WRF 4 km radar reflectivity data 
# extracted over a region about the size of a single scanning radar domain
###############################################################################################

# CACTI
 radar_lon=-64.75
 radar_lat=-32.1
 start_date='2018-10-15T00'
 end_date='2019-03-03T00'
# start_date='2018-11-10T16'
# end_date='2018-11-11T06'

# Animation frame rate
frame_rate=2

# Convert start_date format to yyyymmdd_hh
start_date_img=$(date -d "${start_date//T/ }" "+%Y%m%d")
echo ${start_date_img}

pyflex_dir=/global/homes/m/mckenna/PyFLEXTRKR/
runscript=${pyflex_dir}'/runscripts/run_celltracking.py'
config_file=/global/homes/m/mckenna/PyFLEXTRKR/config/config_wrf_3km_highfreq.yaml
quicklook_dir=/pscratch/sd/m/mckenna/cacti/wrf/cell_tracking/quicklooks/

# Activate PyFLEXTRKR conda environment
echo 'Activating PyFLEXTRKR environment ...'
#source activate /global/common/software/m1867/python/pyflex
source activate flextrkr

# Run tracking
#echo 'Running PyFLEXTRKR ...'
#echo 'runscript name:' ${runscript}
#echo 'config_file name:' ${config_file}
#python ${runscript} ${config_file}
#echo 'Tracking is done.'


# Make quicklook plots
echo 'Making quicklook plots ...'
python ${pyflex_dir}/Analysis/plot_subset_cell_tracks_demo.py -s ${start_date} -e ${end_date} \
    -c ${config_file} --radar_lat ${radar_lat} --radar_lon ${radar_lon} -p 1 --figsize 8 7 --output ${quicklook_dir}
echo 'View quicklook plots here: '${quicklook_dir}

# Make animation using ffmpeg
echo 'Making animations from quicklook plots ...'
animation_filename=${quicklook_dir}quicklook_animation_${start_date}_${end_date}.mp4
ffmpeg -framerate ${frame_rate} -pattern_type glob -i ${quicklook_dir}${start_date_img}'*.png' -c:v libx264 -r 10 -crf 20 -pix_fmt yuv420p \
    -y ${animation_filename}
echo 'View animation here: '${animation_filename}
