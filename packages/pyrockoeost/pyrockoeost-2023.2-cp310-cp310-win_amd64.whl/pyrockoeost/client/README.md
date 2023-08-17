# pyrockoeost client subpackage

The pyrockoeost software package comes with several clients for requesting online earthquake catalogs and waveform archives.

## Waveform access

* `pyrockoeost.client.fdsn` Is a client for FDSN web services (http://www.fdsn.org/).
* `pyrockoeost.client.iris` Gives access to waveform data from the IRIS archive (http://service.iris.edu/).

## Earthquake catalogs

* `pyrockoeost.client.catalog.Geofon` Access the GEOFON earthquake catalog (http://geofon.gfz-potsdam.de/)
* `pyrockoeost.client.catalog.GlobalCMT` Get earthquakes from the Global CMT catalog (http://www.globalcmt.org/)
* `pyrockoeost.client.catalog.USGS` Query the USGS earthquake catalog (https://earthquake.usgs.gov/)
* `pyrockoeost.client.catalog.Saxony` Regional Catalog of Saxony, Germany from the University of Leipzig (http://home.uni-leipzig.de/collm/auswertung_temp.html)

(Also accessible through `pyrockoeost.client.catalog`)
