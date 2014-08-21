---
layout: post
comments: true
title:  "R and Quakes"
date:   2014-08-18 00:00:00
categories: R
---

I decided to do a bit of data exploration around major California earthquakes in the last 30 years. Specifically, I will look at earthquakes within 200 km of San Francisco and Los Angeles.

USGS has a very accessible Earthquake API and [online query form](http://earthquake.usgs.gov/earthquakes/search/). I wrote a [simple script](http://github.com/abshinn/usgs/) in Python3 which queries the API and downloads the result.

## Data preparation

### Fetching the data 

To pull down the data, use [usgs.APIquery](http://github.com/abshinn/usgs/) with the desired parameters. All parameters are [defined here](http://comcat.cr.usgs.gov/fdsnws/event/1/).

```python
import usgs

# obtain data for the greater San Francisco area, 1983 through 2012
usgs.APIquery(starttime = "1983-01-01", endtime = "2013-01-01",
              minmagnitude = "0.1",
              latitude = "37.77", longitude = "-122.44",
              minradiuskm = "0", maxradiuskm = "200",
              reviewstatus = "reviewed",
              filename = "usgsQuery_SF_83-12.csv",
              format = "csv")

# obtain data for the greater Los Angeles area, 1983 through 2012
usgs.APIquery(starttime = "1983-01-01", endtime = "2013-01-01",
              minmagnitude = "0.1",
              latitude = "34.05", longitude = "-118.26",
              minradiuskm = "0", maxradiuskm = "200",
              reviewstatus = "reviewed",
              filename = "usgsQuery_LA_83-12.csv",
              format = "csv")
```

Switching over to use R, I then read the CSVs into dataframes. For convenience, I define an area label and combine the dataframes into one.

```R
SFquakes = read.csv('usgsQuery_SF_83-12.csv', header = TRUE, stringsAsFactors = FALSE)
LAquakes = read.csv('usgsQuery_LA_83-12.csv', header = TRUE, stringsAsFactors = FALSE)
SFquakes$area = "SF"
LAquakes$area = "LA"
quakes = rbind(SFquakes, LAquakes)
```

### Data scrubbing and binning

```R
# remove columns with all NA values
quakes = quakes[,-7:-10]

# create column with time object
quakes$ptime = as.POSIXlt(strptime(quakes$time, "%Y-%m-%dT%T"))

# remove instances of mwb, an alternative form of magnitude measurement
quakes = quakes[-which(quakes$magType == "mwb"),]

# create columns with year bins
quakes$yearbins = strftime(cut(quakes$ptime, "year", right = F), "%Y")

# create columns with half and whole magnitude bins
quakes$Mhalfbins = cut(quakes$mag, seq(2.0,7.5,.5), right = F)
quakes$Mwholebins = cut(quakes$mag, seq(2.0,8.0,1), right = F)

# create a column with varied magnitude bins, necessary if plotting without a log scale
quakes$Mvariedbins = cut(quakes$mag, c(2.0,2.5,3.0,3.5,4.0,5.0,7.5), right = F)
```

### Magnitude-energy conversion

One way to comprehend the destructive force of earthquakes is to convert from earthquake magnitude to a more imaginative unit of energy: the ton of TNT. To do this conversion, we need to be able to convert from magnitude to energy, perhaps with the help of Beno and Charles. Also, it is useful to know that one ton of TNT is equivalent to about 4.184e9 Joules.

The [Gutenberg and Richter](https://www2.bc.edu/john-ebel/GutenberRichterMagnitude.pdf) energy-magnitude relation (in Joules):

> *E[M] = 10^(1.5\*M + 4.8)*

```R
quakes$Ejoules = 10^(1.5*quakes$mag + 4.8) # units of Joules
quakes$Etnt = quakes$Ejoules/4.184e9       # units of kilotonnes, TNT
```

### Calculate approximate distance from epicenter to city center

For this calculation I decided to use the [Haversine formula](http://en.wikipedia.org/wiki/Haversine_formula). A great reference to implementing this method and other methods can be found [here](http://www.movable-type.co.uk/scripts/latlong.html).

```R
Rearth = 6371 # average earth radius

# approximate city centroids
quakes$area_lon = 0
quakes$area_lon[quakes$area == "SF"] = -122.44
quakes$area_lon[quakes$area == "LA"] = -118.26
quakes$area_lat = 0
quakes$area_lat[quakes$area == "SF"] = 37.77
quakes$area_lat[quakes$area == "LA"] = 34.05

# haversine formula
lat1 = quakes$area_lat*pi/180
lat2 = quakes$latitude*pi/180
dlat = (quakes$area_lat - quakes$latitude)*pi/180
dlon = (quakes$area_lon - quakes$longitude)*pi/180
a = sin(dlat/2)*sin(dlat/2) + cos(lat1)*cos(lat2)*sin(dlon/2)*sin(dlon/2)
c = 2*atan2(sqrt(a), sqrt(1 - a))
quakes$dist = Rearth*c
```

## Ask the data

### What were the largest earthquakes in recent history?

```R
quakes = quakes[order(quakes$mag, decreasing = TRUE),] # sort by magnitude
print(quakes[quakes$mag >= 6.0,c("ptime", "mag", "area", "Etnt", "dist")])
```

**Output (with annotation):**

```R
10599 1992-06-28 11:57:38 7.3   LA 1344028.02 159.76987 <-- Landers
7349  1999-10-16 09:46:46 7.2   LA  951498.97 175.46360 <-- Hector Mine
3705  1989-10-18 00:04:16 6.9   SF  337604.58  94.25933 <-- Loma Prieta
9184  1994-01-17 12:30:55 6.7   LA  169203.10  31.30647 <-- Northridge
10587 1992-06-28 15:05:33 6.5   LA   84802.44 135.38916 <-- related to Landers
4538  1984-04-24 21:15:20 6.1   SF   21301.41  82.69884 <-- Morgan Hill
10869 1992-04-23 04:50:23 6.1   LA   21301.41 162.05213 <-- Joshua Tree, preceeded Landers
```

To compare the largest earthquakes in each area, the Landers quake had an explosive force of 1.3 megatonnes of TNT, while the Loma Prieta had about 340 kilotonnes of explosive force. 

Since epicenter location is a huge factor in the destructive power of an earthquake, it is interesting to note that the Landers quake was about 160 km away from the densely populated LA metro area, while the Northridge quake was 30 km away, and about 4.0 (10^.6) times less powerful.

### Which major city was most affected by earthquakes?

```R
# Mean distance, magnitude, and Energy in TNT
print(aggregate(data = quakes, cbind(dist, mag, Etnt) ~ area, mean))
```

**Output:**

```R
  area     dist      mag      Etnt
1   LA 126.2884 3.104314 368.69829
2   SF 111.7245 2.959269  84.71983
```

The question of which city has been more affected is more complex than a simple calculation of the 30-year mean of distance and magnitude. However, on average, recent earthquakes surrounding LA have been about 10% closer than Bay Area earthquakes, 1.4 (10^.15) times more severe in magnitude, and with over 4 times more explosive force.

### What is the combined yearly mean distance, magnitude, and energy?

```R
# yearly averages
print(aggregate(data = quakes, cbind(dist, mag, Etnt) ~ yearbins, mean))
```

**Output:**

```R
   yearbins      dist      mag        Etnt
1      1983 126.72346 3.292727    4.506520
2      1984 109.04522 3.351741  118.236847
3      1985 119.81664 3.106047    7.779889
4      1986 123.08929 3.196345   57.913989
5      1987  97.01694 3.090076   28.177762
6      1988 117.30689 3.134848   14.505230
7      1989  99.45154 3.223005  804.548631
8      1990 109.68262 3.072021   23.281553
9      1991 113.49903 3.020319   24.002774
10     1992 156.23963 3.236533  982.619831
11     1993 135.49608 2.986907    2.706447
12     1994  70.18247 3.157971  168.194017
13     1995 138.14896 3.124582   17.246275
14     1996 129.99745 3.138735    6.002731
15     1997 115.75065 3.156890    6.668820
16     1998 117.41048 3.114228    6.726535
17     1999 172.62893 3.256908 1310.867030
18     2000 149.68578 3.105828    4.814266
19     2001 137.13644 3.147203    7.012212
20     2002 117.39979 3.076856    4.366177
21     2003 121.76297 3.115162    6.349083
22     2004 119.03760 3.097368    8.930705
23     2005 121.67829 3.138785   13.896986
24     2006 121.59305 3.050495    3.925653
25     2007 114.70162 3.046964   19.888577
26     2008 113.91730 2.963265   12.969126
27     2009  96.35781 2.678468    3.110633
28     2010 108.41160 2.525352    1.134227
29     2011 100.28416 2.606379    1.477807
30     2012 105.47032 2.533573    1.094880
```

Due to the exponential nature of the data, the Etnt feature is a clear indicator for seismologically active years. Also, it appears we are seeing increased detection efficiency in the last few years with the average magnitude decreasing.

### What is the magnitude-frequency distribution for the two areas of interest?

```R
freqSF = as.data.frame(table(quakes[quakes$area == "SF","Mhalfbins"]))
names(freqSF) = c("magSF", "freqSF")
freqLA = as.data.frame(table(quakes[quakes$area == "LA","Mhalfbins"]))
names(freqLA) = c("magLA", "freqLA")

# event frequency
print(cbind(freqSF, freqLA))
```

**Output:**

```R
     magSF freqSF   magLA freqLA
1  [2,2.5)    476 [2,2.5)    444
2  [2.5,3)   1838 [2.5,3)   2383
3  [3,3.5)   1505 [3,3.5)   2813
4  [3.5,4)    455 [3.5,4)   1045
5  [4,4.5)    173 [4,4.5)    360
6  [4.5,5)     42 [4.5,5)     84
7  [5,5.5)      9 [5,5.5)     34
8  [5.5,6)      2 [5.5,6)     10
9  [6,6.5)      1 [6,6.5)      1
10 [6.5,7)      1 [6.5,7)      2
11 [7,7.5)      0 [7,7.5)      2
```

Note: the units for frequency are in Event Counts per 30 years.

I am not an expert in seismology. However, my guess would be that this magnitude-frequency should theoretically follow a power-law where at one end, as the magnitude approaches zero, the frequency increases exponentially, and at the other end, as the magnitude exceeds 10 the frequency diminishes to almost 0. The fact that the frequency distribution peaks between [3,3.5) and falls off as the magnitude approaches 0, given my uneducated guess, suggests that the detection efficiency (exponentially) decreases as it approaches 0. See the magnitude versus frequency plot below.

## Plots

Time for some plots. Let's have a look at the following correlations:

- time vs. magnitude
- magnitude-frequency correlation

Load ggplot2 and scales. The scales package is necessary for log tick marks.

```R
library("ggplot2")
library("scales")
```

### time vs. magnitude

```R
png("SF-LA_timeVmag.png", width = 1000, height = 800)
timeVmag = ggplot(na.omit(quakes), aes(ptime, mag)) +
           geom_point(aes(size = mag, color = dist)) +
           ggtitle("SF and LA Earthquakes, 1983-2012") +
           xlab("time") +
           ylab("earthquake magnitude") + 
           guides(size = guide_legend(title = "magnitude")) +
           guides(color = guide_legend(title = "distance [km]")) +
           scale_color_gradient(low = "red", high = "dark gray") +
           theme_grey(base_size = 12) +
           theme(text = element_text(size = 22)) +
           facet_wrap(~ area, ncol = 1)
print(timeVmag)
dev.off()
```

**Output:**

![Magnitude over Time]({{ site.url }}/assets/SF-LA_timeVmag.png)

The major earthquakes that pop out in this plot are: Landers in 1992, Loma Prieta in 1989, and Northridge at the beginning of 1994. What is also interesting is the amount of aftershocks and related earthquakes for the major Los Angeles area earthquakes. Another interesting aspect of this plot is the increased detection efficiency of 2 to 2.5 magnitude earthquakes since 2009. Perhaps this is due to the [Quake-Catcher Network (QCN)](http://qcn.stanford.edu/wp-content/uploads/2011/10/2009-Cochran_et_al_IEEE_QCN_smaller.pdf)?

### magnitude-frequency correlation

```R
freq = as.data.frame(table(quakes[quakes$mag >= 2.0,c("area","mag")]))
freq = freq[order(freq$area),]
freq[freq$Freq == 0.0,] = NA # bins with zero counts cause log plot issues
png("SF-LA_magVfreq.png", width = 1000, height = 800)
magVfreq = ggplot(na.omit(freq), aes(mag, Freq)) +
           geom_point(aes(color = area), size = 4) + 
           ggtitle("SF and LA Earthquakes, 1983-2012") + 
           ylab("frequency [event count per 31 years]") + 
           scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
                         labels = trans_format("log10", math_format(10^.x))) +
           scale_x_discrete("magnitude", breaks = seq(2,7.5,.5)) + 
           geom_smooth(method = "loess", aes(group = 1), color = "black") +
           theme_grey(base_size = 12) + 
           theme(text = element_text(size = 22))
print(magVfreq)
dev.off()
```

**Output:**

![Magnitude versus Frequency]({{ site.url }}/assets/SF-LA_magVfreq.png)

The correlation between magnitude and frequency for most of the Richter scale has a slope of about 10^1 events over one order of magnitude. Furthermore, as the magnitude increases, the spread of the data increases due to the insufficient amount of counts. 
