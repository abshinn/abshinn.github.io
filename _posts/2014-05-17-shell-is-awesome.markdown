---
layout: post
title:  "In awe of Shell"
date:   2014-05-17 00:00:00
categories: bash 
---

Way back during one of my undergraduate astronomy data analysis courses, we briefly covered useful shell commands for searching and parsing data such as `grep`, `sed`, and `cut`. At the time I remember thinking that they looked very useful, but without practice I quickly reverted to more familiar and less efficient methods.

Fast forward to the week before I started the Zipfian Academy. In our pre-course work, we were tasked with parsing New York nursing home bed census data using three different approaches: SQLite3, Python, and Shell.

Data courtesy of MLB.

### Converting between tab or space delimited format to a comma delimited format

`stats.tsv` is currently delimited unevenly by spaces. To fix this, how about we remove all spaces and replace it with a single comma. The following command uses `cat` to send all of `stats.tsv` to standard output, then pipe `|` that output to `sed -E`, which takes a "modern" regular expression that finds more than one whitespace `[[:space:]]+` and replaces it with a single comma. Finally, send the resulting output `>` to `stats.csv`.

```bash
$ cat stats.tsv | sed -E "s/[[:space:]]+/,/g" > stats.csv
```

### Displaying a .csv file in well-formatted columns

Show the top five rows of `stats.csv`, then use `column -s, -t` to tell shell to turn a comma delimited STDOUT into cleanly separated columns.

```bash
$ head -5 stats.csv | column -s, -t
RK  Last      F.  Team  Pos  G   AB   R   H   2B  3B  HR  RBI  BB  SO  SB  CS  AVG   OBP   SLG   OPS
1   Bautista  J   TOR   RF   44  157  35  47  8   0   11  30   37  32  1   1   .299  .437  .561  .997
2   Choo      S   TEX   LF   38  132  20  40  7   1   4   11   24  40  3   2   .303  .427  .462  .889
3   Dunn      A   CWS   1B   34  114  14  29  7   0   6   15   27  39  1   0   .254  .399  .474  .872
4   Napoli    M   BOS   1B   40  143  16  38  9   0   5   22   29  44  0   1   .266  .397  .434  .830
```

### Count unique teams

```bash
$ tail +2 stats.csv | cut -d, -f4 | sort | uniq | wc -l
    15
```

### Show only Oakland Athletics players and sort by batting average

```bash
$ grep OAK stats.csv | column -n -t, -k18,18 | column -s, -t
76  Reddick    J  OAK  RF  39  131  18  30  1   3  4   18  10  31  1  0  .229  .289  .374  .663
24  Callaspo   A  OAK  2B  37  124  14  31  4   0  3   15  21  18  0  0  .250  .359  .355  .713
51  Cespedes   Y  OAK  LF  39  144  23  37  11  1  7   22  16  28  0  1  .257  .329  .493  .822
20  Lowrie     J  OAK  SS  42  162  24  42  14  0  3   18  22  20  0  0  .259  .360  .401  .761
29  Donaldson  J  OAK  3B  42  173  34  48  10  1  10  34  19  39  1  0  .277  .351  .520  .871
14  Moss       B  OAK  1B  42  143  20  41  8   1  9   36  15  31  1  0  .287  .372  .545  .917
``` 

### Find a particular team and display particular columns

### Grab a unique team, output to file, find mean avg
