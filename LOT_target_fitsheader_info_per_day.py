#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 04:48:28 2019

@author: altsai
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

generate master bias, master dark, master flat for one month.
$ condaa
$ python slt_calibration_science_target.py slt201908
or
$ python slt_calibration_science_target.py slt20190822

"""




import os
import sys
import shutil
#import re
import numpy as np
#import numpy
from astropy.io import fits
#import matplotlib.pyplot as plt
#import scipy.ndimage as snd
#import glob
#import subprocess
#from scipy import interpolate
#from scipy import stats
#from scipy.interpolate import griddata
#from time import gmtime, strftime
#import pandas as pd
from datetime import datetime
from astropy.wcs import WCS
#from scipy import interpolate
#from scipy import stats
from astropy import units as u
from astropy.coordinates import SkyCoord
# https://docs.astropy.org/en/stable/coordinates/

print('-----------------')
print('input parameters')
print('-----------------')


print('... will grap target information for one day ...')
#folder=sys.argv[1]
folder='LOT20200422'

#date=input("Enter the Date of your data (ex: 20190822): ")
#folder=input("Enter the folder (ex: LOT20190822): ")

#folder='slt'+date

dir_month=folder[0:9]
#date=folder[3:11]
#print(dir_month)
#dir_master=dir_month+'_master/'
#print(dir_master)
#dir_calib_sci=folder+'_calib_sci/'
#print(dir_calib_sci)

file_info='LOT_target_fitsheader_info_'+folder+'.txt'
if os.path.exists(file_info):
    os.remove(file_info)
f_info=open(file_info,'w')

file_log='LOT_target_fitsheader_info_'+folder+'.log'
if os.path.exists(file_log):
    os.remove(file_log)
f_log=open(file_log,'w')

print(sys.argv)
f_log.write(str(print(sys.argv)))

info_folder='Your folder is :'+str(folder)
f_log.write(info_folder+'\n')


'''
if os.path.exists(dir_calib_sci):
    shutil.rmtree(dir_calib_sci)
os.makedirs(dir_calib_sci,exist_ok=True)
'''

'''
if os.path.exists(dir_master):
    shutil.rmtree(dir_master)
os.makedirs(dir_master,exist_ok=True)

print('...generate master files on '+dir_month+'...')
'''
#sys.exit(0)

'''
logfile=dir_month+'_master.log'
sys.stdout=open(logfile,'w')
print(sys.argv)
'''




#time_calib_start=strftime("%Y-%m-%d %H:%M:%S", gmtime())
#time_calib_start=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

time_calib_start=str(datetime.now())  
info_time=('File generated by An-Li Tsai at '+time_calib_start+' UTC')
print(info_time)
f_log.write(info_time+'\n')


print(' ---------------------------')
print(' Science Target ')
print(' ---------------------------')
f_log.write(' ---------------------------\n')
f_log.write(' Science Target \n')
f_log.write(' ---------------------------\n')


cmd_search_file_sci="find ./|grep "+folder+"|grep 'fts\|fits'|grep wchen |sort -t'@'"
f_log.write(cmd_search_file_sci+'\n')
list_file_sci=os.popen(cmd_search_file_sci,"r").read().splitlines()
#info_print='...calibrating science targets...'
#print(info_print)
#f_log.write(info_print+'\n')
#print(list_file_sci)
f_log.write(str(list_file_sci)+'\n')
n_file_sci=len(list_file_sci)
info_n_sci='... found '+str(n_file_sci)+' science targets ...'
print(info_n_sci)
f_log.write(info_n_sci+'\n')


head_info='ID|DateObs|Filename|Object|RA_hhmmss|DEC_ddmmss|RA_deg|DEC_deg|RA_pix|Dec_pix|FilterName|JD|ExpTime_sec|Zmag|FWHM|Altitude|Airmass'
f_info.write(head_info+'\n')

k=0
for i in list_file_sci:
    k=k+1
    idx=str(k)
    filename_sci=[i.split('/',-1)[-1]][0]
    hdu=fits.open(i)[0]
    imhead=hdu.header
    imdata=hdu.data
#    print(imdata.shape)
    exptime=imhead['EXPTIME']
    idx_time=str(int(exptime))+'S'
#    print(idx_time)
#    print(exptime)
#    naxis=imhead['NAXIS']
#    print(naxis)
    date_obs=imhead['DATE-OBS'].split('T',-1)[0]
#    time_obs=imhead['TIME-OBS']
    try:
        altitude=imhead['OBJCTALT']
    except KeyError:
        fwhm=-9999
    airmass=imhead['AIRMASS']
    jd=imhead['JD']
    filter_name=imhead['FILTER']
    obj=imhead['OBJECT']
    try: 
        fwhm=imhead['FWHM']
    except KeyError:
        fwhm=-9999
    try:
        zmag=imhead['ZMAG']
    except KeyError:
        zmag=-9999
    ra_hhmmss=imhead['OBJCTRA']
    dec_ddmmss=imhead['OBJCTDEC']
    radec_deg=SkyCoord(ra_hhmmss,dec_ddmmss,unit=(u.hourangle,u.deg))
#    ra_deg=SkyCoord(ra_hhmmss,unit=(u.hourangle))
#    dec_deg=SkyCoord(dec_ddmmss,unit=(u.deg))
    ra_deg=radec_deg.ra.deg
    dec_deg=radec_deg.dec.deg
#    print(ra_deg,dec_deg)
    
#    select_master_dark=master_dark
    wcs=WCS(imhead)
    xdec_pix=wcs.all_world2pix(ra_deg,dec_deg,1)
    ra_pix=xdec_pix[0].tolist()
    dec_pix=xdec_pix[1].tolist()
    print(ra_pix,dec_pix)
    cmd_sci_filter='echo '+filter_name+'|cut -d _ -f1'
#    print(cmd_sci_filter)
    sci_filter=os.popen(cmd_sci_filter,"r").read().splitlines()[0]
#    print(sci_filter)
    idx_filter_time=sci_filter+"_"+idx_time
    info_sci=str(k)+' [DATE] '+date_obs+ str(filename_sci)+' [OBJ] '+str(obj)+' [RA_hhmmss] '+ra_hhmmss+' [DEC_ddmmss] '+dec_ddmmss+' [RA_deg] '+str(ra_deg)+' [DEC_deg] '+str(dec_deg)+' [ra_pix] '+str(ra_pix)+' [dec_pix] '+str(dec_pix)+' [FIL] '+filter_name+' [JD] '+str(jd)+' [EXPTIME] '+str(exptime)+' [ZMAG] '+str(zmag)+' [FWHM] '+str(fwhm)+' [ALT] '+str(altitude)+' [AIRMASS] '+str(airmass)
#    print(info_sci)
    f_log.write(info_sci+'\n')
    info_write=str(idx)+'|'+date_obs+'|'+ str(filename_sci)+'|'+str(obj)+'|'+ra_hhmmss+'|'+dec_ddmmss+'|'+str(ra_deg)+'|'+str(dec_deg)+'|'+filter_name+'|'+str(jd)+'|'+str(exptime)+'|'+str(zmag)+'|'+str(fwhm)+'|'+str(altitude)+'|'+str(airmass)
    f_info.write(info_write+'\n')
   

info1='... write header information to '+file_info+' ... '
print(info1)
f_log.write(info1+'\n')
info2='... finished ...'
print(info2)
f_log.write(info2+'\n')


f_info.close()
f_log.close()
 
