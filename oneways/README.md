# Oneway Analysis

**Goal:** analyze the length of oneways in minor / residental roads
(not) opened for cyclists. Compare results between districts.

## OpenStreetMap

### Data Acquisition

1. Download [boundaries of Vienna's districts](https://www.data.gv.at/katalog/dataset/stadt-wien_bezirksgrenzenwien)

2. Download the OpenStreetMap road network from [one of these sources](https://planet.osm.org/) or [Overpass Turbo](https://overpass-turbo.eu):

```
way
[highway]
({{bbox}});
(._;>;);
out;
```

3. Convert the OSM file to geopackage with `ogr2ogr`

```bash
OSM_CONFIG_FILE=osmconf_custom.ini ogr2ogr -f GPKG output.gpkg input.osm.pbf
```

The following steps are done in QGIS.

### Basic Preparations

1. Load the district boundaries and `Reproject` to EPSG:31256
2. Load the *lines* layer of the OSM file
3. Add the layer source filter `"highway" IS NOT NULL`
4. `Reproject` to EPSG:31256
5. `Intersection` of the OSM ways with districts (only keep the `BEZ` field for the district layer)
6. Rename the field `BEZ` to `district`


### Filter Minor Roads 

Filter small roads, but not too small so we don't include e.g. parking lots.
We don't include living streets and pedestrian zones with the exception of *Begegnungszonen*.

```
"highway" IN ('unclassified', 'residential') OR
"traffic_sign" LIKE 'AT:53.9e%' OR "traffic_sign" = 'AT:§53.9e'
```

### Mark Roads With Parallel Cycleways

Oneway roads with a cycleway right next to it should not count as oneways.

1. Filter cycleways with this layer source filter:

```
"highway" = 'cycleway' OR
("highway" = 'footway' AND "bicycle" = 'designated') OR
("highway" = 'path' AND "bicycle" = 'designated')
```

2. `Buffer` (but don't dissolve to save time in the following steps) by 15m

3. `Clip` minor roads with buffered cycleways, add new attribute `cycleway_within_15m=true`, remove attribute `fid`

4. `Difference` minor roads with buffered cycleways, add new attribute `cycleway_within_15m=false`, remove attribute `fid`

5. `Merge vector layers` of the results of *clip* and *difference*


### Determine Opened / Closed Oneways

Calculate these attributes using the `Field Calculator`.

- `length_m`:

```
round($length)
```

- `oneway_type`: 

```
case
when oneway='yes' and (
        ("oneway_bicycle" is null or "oneway_bicycle" != 'no') and
        ("cycleway" is null or "cycleway" not like 'opposite%') and
        ("cycleway_left" is null or "cycleway_left" not like 'opposite%') and 
        ("cycleway_right" is null or "cycleway_right" not like 'opposite%') and
        ("cycleway_both" is null or "cycleway_both" not like 'opposite%') and
        ("cycleway_within_15m" is null or "cycleway_within_15m" = false)
    )
then 'oneway_closed'
when "oneway" = 'yes' and (
        "oneway_bicycle" = 'no' or
        "cycleway" like 'opposite%' or
        "cycleway_left" like 'opposite%' or 
        "cycleway_right" like 'opposite%' or
        "cycleway_both" like 'opposite%' or
        "cycleway_within_15m" = true
    )
then 'oneway_opened'
else 'no_oneway'
end
```

### Manual fixes

Now is the time to fix any errors for the `oneway_type` manually.

### Statistics

Calculate `Statistics by Categories` on the field `length_m` with the fields `district` and `oneway_type` as categories.

