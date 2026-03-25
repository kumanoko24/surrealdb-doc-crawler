---
title: Geo functions
url: https://surrealdb.com/docs/surrealql/functions/database/geo
crawled_at: 2026-03-25 18:43:09
---

# Geo functions


These functions can be used when working with and analysing geospatial data.

| Function | Description |
| --- | --- |
| geo::area() | Calculates the area of a geometry |
| geo::bearing() | Calculates the bearing between two geolocation points |
| geo::centroid() | Calculates the centroid of a geometry |
| geo::distance() | Calculates the distance between two geolocation points |
| geo::&#8203;hash::decode() | Decodes a geohash into a geometry point |
| geo::&#8203;hash::encode() | Encodes a geometry point into a geohash |
| geo::is_valid() | Determines if a geometry type is a geography type |


## Point and geometry


- A point is composed of two floats that represent the longitude (east/west) and latitude (north/south) of a location.
- A geometry is a type of object defined in the GeoJSON spec, of which Polygon is the most common. They can be passed in to the geo functions as objects that contain a "type" (such as "Polygon") and "coordinates" (an array of points).

## geo::area


The `geo::area` function calculates the area of a geometry in square metres.

API DEFINITION

```
geo::area(geometry) -> number
```

The following example shows this function, and its output, when used in a RETURN statement for four approximate points found on a map for the US state of Wyoming which has an area of 253,340 km2 and a mostly rectangular shape. Note: the doubled square brackets are because the function takes an array of an array to allow for more complex types such as MultiPolygon.

```
RETURN geo::area({  type: "Polygon",  coordinates: [[    [-111.0690, 45.0032],    [-104.0838, 44.9893],    [-104.0910, 40.9974],    [-111.0672, 40.9862]  ]]});
```

Response

```
253317731850.3478f
```

If the argument is not a geometry type, then an error will be returned.

```
RETURN geo::area(12345);-- 'Incorrect arguments for function geo::area(). Argument 1 was the wrong type. Expected `geometry` but found `12345`'
```


## geo::bearing


The `geo::bearing` function calculates the bearing between two geolocation points. Bearing begins at 0 degrees to indicate north, increasing clockwise into positive values and decreasing counterclockwise into negative values that converge at 180 degrees.

API DEFINITION

```
geo::bearing($from: point, $to: point) -> number
```

The following example shows this function, and its output, when used in a RETURN statement:

```
-- LET used here for readabilityLET $paris = (2.358058597411099, 48.861109346459536);LET $le_puy_en_velay = (3.883428431947686, 45.04383588468415);RETURN geo::bearing($paris, $le_puy_en_velay);RETURN geo::bearing($le_puy_en_velay, $paris);
```

Response

```
-- Slightly east of directly south164.18154786094604f-- Slightly west of directly north-14.70308114652183f
```


## geo::centroid


The `geo::centroid` function calculates the centroid between multiple geolocation points.

API DEFINITION

```
geo::centroid(geometry) -> number
```

The following example shows this function, and its output, when used in a RETURN statement. Note: the doubled square brackets are because the function takes an array of an array to allow for more complex types such as MultiPolygon.

```
RETURN geo::centroid({  type: "Polygon",  coordinates: [[    [-0.03921743611083, 51.88106875736589], -- London    [30.48112752349519, 50.68377089794912], -- Kyiv    [23.66174524001544, 42.94500782833793], -- Sofia    [ 1.92481534361859, 41.69698118125476] -- Barcelona  ]]});
```

The return value is a mountainous region somewhere in Austria:

Response

```
(13.483896437936192, 47.07117241195589)
```


## geo::distance


The `geo::distance` function calculates the haversine distance, in metres, between two geolocation points.

API DEFINITION

```
geo::distance($from: point, $to: point) -> number
```

The following example shows this function, and its output, when used in a RETURN statement:

```
let $london = (-0.04592553673505285, 51.555282574465764);let $harare = (30.463880214538577, -17.865161568822085);RETURN geo::distance($london, $harare);
```

Response

```
8268604.251890703f
```


## geo::hash::decode


The `geo::hash::decode` function converts a geohash into a geolocation point.

API DEFINITION

```
geo::hash::decode(point) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN geo::hash::decode("mpuxk4s24f51");
```

Response

```
(51.50986494496465, -0.11809204705059528)
```


## geo::hash::encode


The `geo::hash::encode` function converts a geolocation point into a geohash.

API DEFINITION

```
geo::hash::encode(point) -> string
```

The function accepts a second argument, which determines the accuracy and granularity of the geohash.

API DEFINITION

```
geo::hash::encode(point, $granularity: number) -> string
```

The following example shows this function, and its output, when used in a RETURN statement:

```
RETURN geo::hash::encode( (51.509865, -0.118092) );-- 'mpuxk4s24f51'
```

The following example shows this function with two arguments, and its output, when used in a select statement:

```
RETURN geo::hash::encode( (51.509865, -0.118092), 5 );-- 'mpuxk'
```


## geo::is_valid


The `geo::is_valid` function determines if a geometry type is a geography type.
Geography types are used to store geolocation data in a Geographic Coordinate System (GCS), 
whereas geometry types can store geolocation data in any coordinate system, including GCS, mathematical planes, board game layouts, etc...

A geography type add the following constraint: 
each `Point` coordinates are in the range of -180° to 180° for longitude and -90° to 90° for latitude.

API DEFINITION

```
geo::is_valid(geometry) -> bool
```

The following examples show this function, and its output, when used in a RETURN statement:

A valid geography point

```
RETURN geo::is_valid( (51.509865, -0.118092) );-- true
```

Out of range geometry point

```
RETURN geo::is_valid( (-181.0, -0.118092) );-- false
```
