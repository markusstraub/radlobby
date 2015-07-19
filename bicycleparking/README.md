# Analysis of bicycle parking in Vienna (Austria)

Author: markus.straub.at@gmail.com

This repository holds some analysis of the situation for bicycle parking in Vienna, Austria and the according python scripts. Results are found in the files vienna_bicycleparking_anylsed.csv/png.

## Data Sources

* bicycle parking 2015-04: OGD Vienna "Fahrradabstellanlagen - Standorte", 2015-04-10 (CC BY 3.0 AT, MA46) [1]
* population 2014: "Bevölkerung nach Bezirken 2006 bis 2014", MA23 [2]

Note: a big station is defined as a station capable of holding >= 50 bicycles.

## Results

![result diagrams](vienna_bicycleparking_anylsed.png)

The **inner districts (1-9)** have on average better coverage with bicycle parking than the **outer districts** (10-23).

Since the first district is not densely populated, the 9th district is the benchmark regarding **bicycle parking per inhabitant** with 99 bicycle parking per 1000 inhabitants. All outer districts have only 21 biycle parking per 1000 inhabitants or lower.

Regarding **big bicycle parking stations** holding >= 50 bicycles the 2nd and 22nd district are leading. Most of these stations can be found along the metro line U2.

The single **biggest station** is located at the train station "Westbahnhof" with space for 480 bicycles.

### Notable districts (positive):
* 1st district
    * most total bicycle parking per inhabitant (but very little inhabitants)
    * 2nd most total bicycle parking
* 2nd district
    * 2nd most big bicycle parking
* 9th district
    * most total bicycle parking
    * 2nd most total bicycle parking per inhabitant
* 22nd district
    * most big bicycle parking
    * 3rd most total bicycle parking

### Notable districts (negative):
* 10th district
    * lowest total bicycle parking per inhabitant (tie with 11th district)
* 11th district
    * lowest total bicycle parking per inhabitant (tie with 10th district)
    * 3rd lowest total bicycle parking
* 17th district
    * 2nd lowest total bicycle parking
* 19th district
    * lowest total bicycle parking

[1]: https://open.wien.at/site/datensatz/?id=97ef14eb-f280-48a7-96c0-df03859b06c2
[2]: http://www.wien.gv.at/statistik/bevoelkerung/tabellen/bevoelkerung-bez-zr.html