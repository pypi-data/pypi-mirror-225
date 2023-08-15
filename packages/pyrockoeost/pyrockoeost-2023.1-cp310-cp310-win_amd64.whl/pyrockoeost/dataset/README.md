

# pyrockoeost Dataset Submodule

The `pyrockoeost.dataset` submodule gives access to several helpful geo datasets:

## Seismic Velocity Datasets

* `pyrockoeost.dataset.crust2x2` Interface to CRUST2.0 global seismic velocity model (https://igppweb.ucsd.edu/~gabi/crust2.html) [Bassin et al., 2000].
* `pyrockoeost.dataset.crustdb` Accesses the Global Crustal Database (https://earthquake.usgs.gov/data/crust) delivering empirical velocity measurements of the earth for statistical analysis. [Mooney et al., 1998]

## Topographic Datasets Submodule

* `pyrockoeost.dataset.topo` Access to topograhic datasets in different resolutions.

## Tectonic Datasets `pyrockoeost.dataset.tectonics`

* `pyrockoeost.dataset.tectonics.PeterBird2003` An updated digital model of plate boundaries. (http://peterbird.name/publications/2003_PB2002/2003_PB2002.htm) [P. Bird, 2003]
* `pyrockoeost.dataset.tectonics.GSRM1` An integrated global model of present-day plate motions and plate boundary deformation [Kreemer, C., W.E. Holt, and A.J. Haines, 2003]

## Geographic Datasets

* `pyrockoeost.dataset.gshhg` An interface to the Global Self-consistent Hierarchical High-resolutions Geography Database (GSHHG; http://www.soest.hawaii.edu/wessel/gshhg/) [Wessel et al, 1998].
* `pyrockoeost.dataset.geonames` Providing city names and population size from http://geonames.org.
