# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 17:29:16 2025

@author: Thomas Ball
"""

import geopandas as gpd

import pandas as pd
import os
import numpy as np
import shapely as sh
import tqdm 

records = ["LIVING_SPECIMEN", "OBSERVATION", "HUMAN_OBSERVATION", "OCCURANCE", "MACHINE_OBSERVATION"]
minYear = 2000

dat_path = os.path.join("dat", "0000098-250225085111116.csv")
vec_path = os.path.join("dat", "ne_50m_admin_0_countries", "ne_50m_admin_0_countries.shp")

df = pd.read_csv(dat_path, sep = "\t", header = 0)

dff = df[(df.basisOfRecord.isin(records))&((df.year > minYear) | (df.year.isna()))]
dff = dff[~dff.decimalLatitude.isna()]

vc = gpd.read_file(vec_path, layer = "ne_50m_admin_0_countries")

dfx = pd.DataFrame()

for idx, row in tqdm.tqdm(vc.iterrows(), total = len(vc)):
    
    iidx = len(dfx)
    dfx.loc[iidx, "ISO_A3"] = row.ISO_A3
    dfx.loc[iidx, "long_name"] = row.SOVEREIGNT
    dfx.loc[iidx, "count"] = 0
    
    geom = row.geometry
    
    for d_idx, d_row in dff.iterrows():
        
        lat = d_row.decimalLatitude
        lon = d_row.decimalLongitude

        point = sh.geometry.Point(lon, lat)
        
        if point.within(geom):
                
            count = d_row.individualCount
            if np.isnan(count):
                count = 1
            
            dfx.loc[iidx, "count"] = dfx.loc[iidx, "count"] + count
        

dfx = dfx.groupby("long_name").sum()

dfx.to_csv("data_out.csv")