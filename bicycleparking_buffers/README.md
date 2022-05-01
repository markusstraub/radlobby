# Bicycle Parking Analysis

Goal: visualize accessibility / availability of bicycle parking

## Data Processing

### Data Acquisition

- [Straßengraph Wien](https://www.data.gv.at/katalog/dataset/1039ed7e-97fb-435f-b6cc-f6a105ba5e09)
- [Fahrradabstellanlagen Standorte Wien](https://www.data.gv.at/katalog/dataset/97ef14eb-f280-48a7-96c0-df03859b06c2)

Note: the bicycle parking OGD does not contain (some) bicycle parking on private areas, e.g. universities, hospitals,..

### Processing

We use QGIS with the plugin `Multi-Distance Buffer`.

1. `Reproject` streets & parking spots to EPSG:31256
2. `Buffer` streets with 15m and create an index
3. `Dissolve` the bicycle parking layer to a single multi geometry
4. Use the plugin `Multi-Distance Buffer` to buffer bicycle parking with 25, 45, 60, 70m and create an index

**Colored Street Buffers**

1. `v.overlay` intersection, i.e. use the `and` operator, of the  the multi-buffered bicycle parking with the buffered street network
2. `v.dissolve` it on the distance attribute
3. `v.overlay` to get the difference between buffered streets and buffered parking, i.e. use the `not` operator. (This takes a while (15 minutes) but still is much faster than using QGIS' `Difference` tool).
4. `Dissolve` the result (50 minutes, the GRASS `v.dissolve` is most likely faster) and remove all attributes
5. `Merge Layers`

The resulting layer `rings_cut` are then colored and used to visualize bicycle parking coverage.

**Ring Outlines**

1. `Merge Layers`: merge the buffered bicycle parkings with the difference of the street network

The resulting layer `rings_full` represent the street network
in combination with the buffers around bicycle parking.

We visualize their outlines only - this gives a bit more structure to the `rings_cut`.

