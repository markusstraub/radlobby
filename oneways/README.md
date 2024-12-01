# Oneway Analysis

**Goal:** analyze the length of oneways in minor / residental roads
(not) opened for cyclists. Compare results between districts.

We use data from [OpenStreetMap](https://www.openstreetmap.org) as well as open government data (OGD). All geospatial processing is done in [QGIS](https://qgis.org)

For results see https://www.radlobby.at/wien/einbahnen

![](oneways.jpg)

## Conventions & Limitations

- **Cycleways next to roads:** Oneways that are *not opened* for cycling but have a cycleway next to them *count as opened*. This is less a limitation but more a convention for our analysis.
- **Separated driving lanes**
  - Roads with separated driving lanes per direction (or roads that were at least mapped like that) are not "real" oneways for the purpose of our analysis and are therefore omitted, i.e. not counted as oneways.
  - Roads with separated driving lanes *next to cycleways* count *double* towards opened oneways although they should not count at all (e.g. Oswaldgasse). This error is not accounted for yet.
- **Short parts of oneways next to cycleways count as opened:** our buffering of cycleways sligthly changes the statistics because oneways leading to/from a cycleway always count as opened for the first few meters. The total error should be negligible though.
- **Access restrictions are not respected:** The analysis may contain roads where cycling / driving is forbidden (we don't yet take access restrictions into account). The number of roads where this is the case is very low.
- **Note regarding the 2022 dataset:** Some residential roads around the new metro station Frankhplatz are used as detour and were tagged as major roads in OSM. We still included them in the analysis.



## Data Processing

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

4. Download open government data for opened oneways - choose whatever was updated more recently (unfortunately updates seem to be irregular):
  - [Radfahranlagen Wien](https://www.data.gv.at/katalog/dataset/5e6175cd-dc44-4b32-a64a-1ac4239a6e4a) (use the layer source filter `"SUBMERKMAL" = 'Radfahren gegen die Einbahn'`)
  - [Radfahren gegen die Einbahn Wien](https://www.data.gv.at/katalog/dataset/radfahren-gegen-die-einbahn-wien)


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

Oneway roads with a cycleway right next to it are treaded as a special case.

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

### False Positives

Manually set the `oneway_type` to `no_oneway` for roads that are not really oneways:
- roads with separated driving directions
- link roads at junctions

Regarding separated driving directions: I tried to map all relevant roads with `dual_carriageway=yes` in 2024-11.

### Quality Assurance

To double-check completeness and correctness of OpenStreetMap data we use the cycle infrastructure OGD with the following layer source filter: `"SUBMERKMAL" = 'Radfahren gegen die Einbahn'`

Deviations between OSM and OGD are checked manually with the help of cyclists with local knowledge.

Then any errors for `oneway_type` are fixed accordingly.


#### Errors in OSM caused by StreetComplete

Unfortunately, between 2020 and 2022 many errors regarding cycling against oneways have been introduced.

They were caused by users of StreetComplete, but hopefully this won't happen again [due to improvements in the app](https://github.com/streetcomplete/StreetComplete/issues/3795)
 
Examples for errors:

`cycleway=opposite(_lane)` and/or `oneway:bicycle=no` was replaced with `cycleway:both=no`
- https://www.openstreetmap.org/changeset/117863995
- https://www.openstreetmap.org/changeset/119111558
- https://www.openstreetmap.org/changeset/106726243
- https://www.openstreetmap.org/changeset/105685872
- https://www.openstreetmap.org/changeset/116780450
- https://www.openstreetmap.org/changeset/113457699
- https://www.openstreetmap.org/changeset/115807497 
- https://www.openstreetmap.org/changeset/115805917
- https://www.openstreetmap.org/changeset/115807497
- https://www.openstreetmap.org/changeset/118404534

This edit was OK (`oneway:bicycle=no` was kept intact, left/right lanes were mapped)
- https://www.openstreetmap.org/changeset/116630724

Most parts of this edit are OK except for Jauresgasse
- https://www.openstreetmap.org/changeset/114030200


### Statistics

Calculate `Statistics by Categories` on the field `length_m` with the fields `district` and `oneway_type` as categories.



## Scheduled Improvements (for the next analysis)

- don't count `junction=roundabout` as oneways
- don't count `dual_carriageway=yes` as oneways
- directly use OGD instead of OSM?
  - pro: their quality since ~2020 is good enough (even more up to date than OSM)
  - con: comparability problems with our 2015 / 2020 / 2022 OSM-based analysis

