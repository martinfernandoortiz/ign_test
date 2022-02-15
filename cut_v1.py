# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 12:09:22 2022

@author: aploeg
"""


######################################################################################################################################################
# 1. Armar un bat/sh para hacer translate de ecw a tif
# 2. Crea un loop para cortar por máscaras
######################################################################################################################################################

import fiona
import rasterio
import rasterio.mask
import os, sys
import glob

import subprocess
pip install fiona



# List filepaths for all bands in the scence
FileList = glob.glob(os.path.join(r'/home/geo/LandsatData','*band*.ecw')) #Acá hay que poner la ruta de tu carpeta


command = ""

for fp in FileList:
    inputfile = fp
    outputfile = inputfile[:-4] + "_clip.tif"

    command += "gdal_translate" % (inputfile, outputfile)

# Write the commands to an .sh file
cmd_file = "translate_ECW_to_TIF.bat" #sh si lo ejecutamos en linux
f = open(os.path.join(cmd_file), 'w')

f.write(command)
f.close()
f.read


###################################################################

cwd = os.getcwd()### CHEQUEAR CUAL ES EL WORKDIRECTORY -- DEBERIA SER DONDE ESTA EL ARCHIVO
cwd

cwd_raster = cwd + '\\raster_entradas' # SETEAR LA CARPETA DE RASTER
cwd_shp = cwd + '\\shp' # SETEAR LA CARPETA DE SHP

#############################################################################

shpfiles =[]
for file in glob.glob(cwd_shp + "\\*.shp"):
    shpfiles.append(file)


tiffiles =[]
for file in glob.glob(cwd_raster + "\\*.tif"):
    tiffiles.append(file)

salida =[]
for i in range(len(shpfiles)):
    nombre = shpfiles[i]
    nombre = nombre[0:-3]+ '_salida.tif'
    nombre = nombre.replace("\\shp\\","\\salidas\\")
    salida.append(nombre)
    
    
salida

salidafiles
glob.glob(cwd_raster + "\\*.tif"):
    tiffiles.append(file)


############################################################################



if len(tiffiles) == len(shpfiles):                            # Truthy
     for i in range(len(shpfiles)):
         print(shpfiles[i])
         
            with fiona.open(shpfiles[i], "r") as shapefile:
                shapes = [feature["geometry"] for feature in shapefile]
                
            with rasterio.open(tiffiles[i]) as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                out_meta = src.meta
                
            out_meta.update({"driver": "GTiff",
                             "height": out_image.shape[1],
                             "width": out_image.shape[2],
                             "transform": out_transform})
            
            with rasterio.open(salida, "w", **out_meta) as dest:
                dest.write(out_image)
     
else:
    print("No coincide el número de raster con los shapes")
