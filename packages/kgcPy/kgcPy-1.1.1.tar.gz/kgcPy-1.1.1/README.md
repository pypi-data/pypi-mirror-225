# kgc
Aids in identifying the Koeppen-Geiger (KG) climatic zone for
a given lat and lon of any location. The resolution of KG map is at 100 sec arc or approximately 187 km at the equator, reported by Rubel et al. [2016]. 

F. Rubel, K. Brugger, K. Haslinger, and I. Auer, (2016) <doi:10.1127/metz/2016/0816>.

# Features
 - lookupCZ(lat, lon): identify the Koeppen-Geiger (KG) climatic zone for a given lat and lon
 - tranlateZipCode('zipcode'): find the lat and lon for a given 'zipcode'
 - nearbyCZ(lat,lon,size=1): get possible climate zones from the central pixel and the surrounding 8 pixels when size is set to 1, and compare to the central pixel, aiming to determine if the provided location is in proximity to a climate zone boundary.
 - roundCoordinates(lat, lon): get the inputed number to nearest ’fine’ (100s) resolution grid point.
 - irradianceQuantile(kg_zone): get irradiance quantiles for each Koppen Geiger Climate Zone
 
#  Setup
1. Install it at bash
```bash
$ pip install kgcPy
```
2.	Import it in python
```python
from kgcPy import *
``` 
#  Examples
***Find KG zone for a given zipcode***
```python
zipcode = '02134'
lat,lon = translateZipCode(zipcode)
kg_zone = lookupCZ(lat, lon)
print('Koppen geiger zone is '+ kg_zone)
``` 
***Output will be KG zone***

#  Versions
All notable changes to this project will be documented in this file.
## [1.1.0] - 2023-08-12 - Package created
## [1.1.1] - 2023-08-15 - Update documentation

#  Description
The kgcPy package is a python version of “kgc: Koeppen-Geiger Climatic Zones” R package on CRAN https://cran.r-project.org/web/packages/kgc/index.html, with addiontal functions.

Aids in identifying the Koeppen-Geiger (KG) climatic zone for a given location. The Koeppen-Geiger climate zones were first published in 1884, as a system to classify regions of the earth by their relative heat and humidity through the year, for the benefit of human health, plant and agriculture and other human activity [1]. This climate zone classification system, applicable to all of the earths surface, has continued to be developed by scientists up to the present day.

One of authors (Rubel) has published updated, higher accuracy KG climate zone definitions [2]. In this package we use these updated high-resolution (100 sec arc) maps as the data source [3]. We provide functions that return the KG climate zone for a given longitude and lattitude, or for a given United States zip code. In addition the nearbyCZ() function will check climate zones nearby to check if the given location is near a climate zone boundary. Digital data, as well as animated maps, showing the shift of the climate zones are provided on the following website <http://koeppen-geiger.vu-wien.ac.at>.

[1] W. Koeppen, (2011) <doi:10.1127/0941-2948/2011/105>.

[2] F. Rubel and M. Kottek, (2010) <doi:10.1127/0941-2948/2010/0430>.

[3] F. Rubel, K. Brugger, K. Haslinger, and I. Auer, (2016) <doi:10.1127/metz/2016/0816>.

## Funding Acknowledgements:
