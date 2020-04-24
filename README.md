# Step-by-step of how to run scripts for data taken for one day

#a='LOT20200422'  
a=$1

## step1 - check whether target is within FOV  
search_no_wcs.py $a  
#if exists, upload no_wcs_files to ycc and modify them  

## step2 - generate fitsheader table  
python LOT_target_fitsheader_info_per_day.py  

## step3 - generate master dark, bias, and flat  
python LOT_calibration_master_1month.py  

## step4 - calibrate science target  
python LOT_calibration_science_calibration.py  


