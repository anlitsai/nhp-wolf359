#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:54:00 2019

@author: altsai
"""

"""
Spyder Editor

data calibration for science target.
$ condaa
$ python LOT_calibration_science_target.py _FOLDER_NAME_

for example:
$ python LOT_calibration_science_target.py LOT20190822
"""

dir_root='/home/altsai/project/20190801.NCU.EDEN/data/wolf359/'


#print(month,date)

import os
import sys
import shutil
#import re
import numpy as np
#import numpy
from astropy.io import fits
#import pyfits
import matplotlib.pyplot as plt
#import scipy.ndimage as snd
#import glob
#import subprocess
#from scipy import interpolate
#from scipy import stats
#from scipy.interpolate import griddata
#from time import gmtime, strftime
#import pandas as pd
from datetime import datetime
from astropy.nddata import Cutout2D

#folder=sys.argv[1]
folder='LOT20200422'
#print("Which Folder you are going to process ?")
#folder=input("Enter a Folder (ex: LOT20190822): ")
date=folder[3:]
year=str(date[0:4])
month=str(date[4:6])
yearmonth=year+month
day=str(date[6:8])
#folder='LOT'+date
dir_folder=yearmonth+'/'+folder+'/'



exptime='60'

#folder=sys.argv[1]
#folder='LOT201908'
dir_master=yearmonth+'/LOT'+yearmonth+'_master_'+exptime+'S/'
#dir_master='data/'+yearmonth+'/LOT'+yearmonth+'_master/'
print(dir_master)

dir_calib_sci=yearmonth+'/'+folder+'_calib_sci_'+exptime+'S/'
#dir_calib_sci='data/'+yearmonth+'/'+folder+'_calib_sci/'

print(dir_calib_sci)
if os.path.exists(dir_calib_sci):
    shutil.rmtree(dir_calib_sci)
os.makedirs(dir_calib_sci,exist_ok=True)



print('... will calibrate science target on '+date+' ...')

#sys.exit(0)


#time_calib_start=strftime("%Y-%m-%d %H:%M:%S", gmtime())
#time_calib_start=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
time_calib_start=str(datetime.now())  
print('Data calibrated by An-Li Tsai at '+time_calib_start+' UTC+8')
#print('')

print(' ---------------------------')
print(' Load Master Bias ')
print(' ---------------------------')

cmd_search_file_bias='find ./ | grep '+dir_master+' | grep fits | grep master_bias'
print(cmd_search_file_bias)
file_bias=os.popen(cmd_search_file_bias,"r").read().splitlines()[0]
#print(file_bias)
#print('len(file_bias)')
#print(len(file_bias))
#sys.exit(0)

#array_each_bias=np.array([pyfits.getdata(i) for i in file_bias])
master_bias=fits.open(file_bias)[0].data
#print(master_bias)
print('...load master bias: '+file_bias+'...')

#sys.exit(0)

print(' ---------------------------')
print(' Load Master Dark ')
print(' ---------------------------')



cmd_search_file_dark='find ./ | grep '+dir_master+' | grep fits | grep master_dark'
#print(cmd_search_file_dark)
file_dark=os.popen(cmd_search_file_dark,"r").read().splitlines()[0]
#print(list_file_dark)

data=fits.open(file_dark)[0].data
#    print(data)
master_dark=data
#    print('--------')

#sys.exit(0)

print(' ---------------------------')
print(' Science Target ')
print(' ---------------------------')

print(folder)
cmd_search_file_sci="find ./ | grep "+dir_folder+" | grep fits | grep wchen |grep "+exptime+"s.fits"
print(cmd_search_file_sci)
list_file_sci=os.popen(cmd_search_file_sci,"r").read().splitlines()
print('...calibrating science targets...')
print(list_file_sci)
print(len(list_file_sci))
#sys.exit(0)



#calib_sci={}

for i in list_file_sci:
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
    jd=imhead['JD']
    obj=imhead['OBJECT']
    try:
        fwhm=imhead['FWHM']
    except:
        fwhm=-9999
    try:
        zmag=imhead['ZMAG']
    except:
        zmag=-9999
    airmass=imhead['AIRMASS']
    altitude=imhead['OBJCTALT']
    ra=imhead['OBJCTRA']
    dec=imhead['OBJCTDEC']
    select_master_dark=master_dark
    filter_name=imhead['FILTER']
    print('------------')
    print('crop size')
    print('------------')
    position=(1023.5,1023.5)
    size=1024
    imdata_cut=Cutout2D(imdata,position,size).data
    print('imdata cut: ', imdata_cut.shape)
#    plt.title('Master Dark cut')
#    plt.imshow(master_dark_cut)
#    plt.show()    
#    sys.exit(0)
    print('------------')
    
    
    print('... load master flat ...')
#    print(cmd_search_file_flat)
    #cmd_sci_filter='echo '+filter_name+' | cut -d _ -f1'
    sci_filter=filter_name.split('_',-1)[0].lower()
    print(sci_filter)
    cmd_search_file_flat='find ./ | grep '+dir_master+' | grep flat_'+sci_filter
    print(cmd_search_file_flat)
#    filename_flat=os.popen(cmd_filename_flat,"r").read().splitlines()[0]
    file_sci_filter=os.popen(cmd_search_file_flat,"r").read().splitlines()[0]
    print('... master flat file is: '+file_sci_filter+' ...')
#    idx_filter_time=sci_filter+"_"+idx_time
#    print(idx_filter_time)
    data_flat=fits.open(file_sci_filter)[0].data
    select_master_flat=data_flat
#    print(select_master_flat[1000][1000])
#    select_master_dark=master_dark[idx_time]
#    print(select_master_dark[1000][1000])
    sci_flat=(imdata_cut-master_bias-select_master_dark)/select_master_flat
    #calib_sci[i]=sci_flat
#    print(time_idx,sci_filter)
#    print(time_idx,sci_filter)
#    print(select_master_flat.shape)
#    print(select_master_dark.shape)
#    print(sci_flat.shape)
    cmd_sci_name='echo '+i+' | cut -d / -f5 | cut -d . -f1'
#    cmd_sci_name='echo '+i+' | cut -d / -f7 | cut -d . -f1'
#    print(cmd_sci_name)
    sci_name=os.popen(cmd_sci_name,"r").read().splitlines()[0]
#    print(sci_name)
#    plt.title(sci_name)
#    plt.imshow(sci_flat,cmap='rainbow')
#    plt.show()
    print('...output calibrated '+sci_name+' to fits file...')
    time_calib=str(datetime.now())  
    imhead.add_history('Master bias, dark, flat are applied at '+time_calib+' UTC+8 by An-Li Tsai')
    fitsname_calib_sci=sci_name+'_calib.fits'
    #hdu=fits.PrimaryHDU(calib_sci[i])
    fits.writeto(dir_calib_sci+fitsname_calib_sci,data=sci_flat,header=imhead,overwrite=True)

    
#sys.exit(0)

print(' ---------------------------')

time_calib=str(datetime.now())
print('...finish calibration at '+time_calib+' UTC+8...')
print()


