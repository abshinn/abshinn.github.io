---
layout: post
comments: true
title:  "The Sultan of Awk"
date:   2014-05-17 00:00:00
categories: bash 
---

Back during one of my undergraduate astronomy data analysis courses, we briefly covered useful shell commands for searching and parsing data such as `grep`, `sed`, `cut`, and `awk`. At the time I remember thinking that they looked very useful, but without practice I quickly reverted to more familiar and less efficient methods.

Fast forward to the week before I started the Zipfian Academy. In our pre-course work, we were tasked with parsing and performing preliminary analysis on New York nursing home bed census data using three different approaches: SQLite3, Python, and Shell. Between the three methods, Shell was by far the shortest and (arguably) most elegant solution. In order to demonstrate my point, I will use some super-useful shell commands on two MLB data sets containing player batting stats. 

Shell scripting commands can be dense, so I will do my best to spell out each command in the plainest English.

## Current American League Batting Stats

### Converting between tab or space delimited format to a comma delimited format

`stats.tsv` is currently delimited by whitespace of various lengths. This is not a very useful format. The following command uses `cat` to send all of `stats.tsv` to standard output, then pipe `|` that output to `sed -E`, which takes "extended" regular expressions that find more than one whitespace `[[:space:]]+` and replaces it with a single comma. Finally, send the resulting output `>` to `stats.csv`.

```bash
$ cat stats.tsv | sed -E "s/[[:space:]]+/,/g" > stats.csv
```

### Displaying a .csv file in well-formatted columns

Show the top five rows of `stats.csv`, then use `column -s, -t` to tell shell to turn a comma delimited STDOUT into cleanly separated columns.

```bash
$ head -6 stats.csv | column -s, -t
RK  Last      F.  Team  Pos  G   AB   R   H   2B  3B  HR  RBI  BB  SO  SB  CS  AVG   OBP   SLG   OPS
1   Bautista  J   TOR   RF   44  157  35  47  8   0   11  30   37  32  1   1   .299  .437  .561  .997
2   Choo      S   TEX   LF   38  132  20  40  7   1   4   11   24  40  3   2   .303  .427  .462  .889
3   Dunn      A   CWS   1B   34  114  14  29  7   0   6   15   27  39  1   0   .254  .399  .474  .872
4   Napoli    M   BOS   1B   40  143  16  38  9   0   5   22   29  44  0   1   .266  .397  .434  .830
5   Ortiz     D   BOS   DH   40  152  22  46  8   0   11  25   22  29  0   0   .303  .392  .572  .964
```

### Count unique teams with word count

`tail +2 stats.csv` will output lines from row 2 to the end of `stats.csv`. In other words, `tail +2` outputs all lines except for the header. `cut -d,` will allow you to select fields from a comma delimited file and `-f4` tells cut to take the 4th column. Finally, `sort` the teams, perform `uniq` to remove similar adjacent lines, and use `wc -l` to count the lines.

```bash
$ tail +2 stats.csv | cut -d, -f4 | sort | uniq | wc -l
    15
```

### Show only Oakland Athletics players and sort by batting average

`grep OAK` performs a regular expression search with OAK, which returns all of the Athletics players in the list. Finally, `sort` using numeric values `-n`  with a comma delimiter `-t,` starting and ending on field 18 `-k18,18` in descending order `-r`.

```bash
$ grep OAK stats.csv | sort -n -t, -k18,18 -r | column -s, -t
14  Moss       B  OAK  1B  42  143  20  41  8   1  9   36  15  31  1  0  .287  .372  .545  .917
29  Donaldson  J  OAK  3B  42  173  34  48  10  1  10  34  19  39  1  0  .277  .351  .520  .871
20  Lowrie     J  OAK  SS  42  162  24  42  14  0  3   18  22  20  0  0  .259  .360  .401  .761
51  Cespedes   Y  OAK  LF  39  144  23  37  11  1  7   22  16  28  0  1  .257  .329  .493  .822
24  Callaspo   A  OAK  2B  37  124  14  31  4   0  3   15  21  18  0  0  .250  .359  .355  .713
76  Reddick    J  OAK  RF  39  131  18  30  1   3  4   18  10  31  1  0  .229  .289  .374  .663
``` 

## Baseball Batting History

Switching gears, let's look at a data set containing all MLB batters from 1871 to 2013. [Many thanks](http://seanlahman.com/support/) to the [Lahman Baseball Database](http://www.opensourcesports.com/baseball/) for making the data easily accessible.

### Display batting stats from the 1985 San Francisco Giants

This is a large data set so let's get specific: how can I look up the player stats for the 1985 San Francisco Giants? This is easily done with chained `grep` commands. But first, in order to display the header along with the `grep` output, I send the header and the output into two different files, `header.csv` and `giants1985.csv`. Finally, I concatenate the two files with `cat`, and `cut` out unwanted columns (keeping columns 1-5 and 8-22).

```bash
$ head -1 Batting.csv > header.csv
```
```bash
$ grep SFN Batting.csv | grep 1985 > giants1985.csv
```
```bash
$ cat header.csv giants1985.csv | cut -d, -f -5,8-22 | column -s, -t
playerID   yearID  stint  teamID  lgID  AB   R   H    2B  3B  HR  RBI  SB  CS  BB  SO   IBB  HBP  SH  SF
adamsri02  1985    1      SFN     NL    121  12  23   3   1   2   10   1   1   5   23   3    1    3   0
bluevi01   1985    1      SFN     NL    30   0   4    1   0   0   0    0   0   3   12   0    0    8   0
brenlbo01  1985    1      SFN     NL    440  41  97   16  1   19  56   1   4   57  62   5    2    4   2
brownch02  1985    1      SFN     NL    432  50  117  20  3   16  61   2   3   38  78   4    11   1   0
davisch01  1985    1      SFN     NL    481  53  130  25  2   13  56   15  7   62  74   12   0    1   7
davisma01  1985    1      SFN     NL    12   0   3    0   1   0   0    0   1   0   5    0    0    4   0
deerro01   1985    1      SFN     NL    162  22  30   5   1   8   20   0   1   23  71   0    0    0   2
driesda01  1985    2      SFN     NL    181  22  42   8   0   3   22   0   0   17  22   3    1    0   3
garresc01  1985    1      SFN     NL    9    1   2    1   0   0   2    0   0   1   4    0    0    0   0
gladdda01  1985    1      SFN     NL    502  64  122  15  8   7   41   32  15  40  78   1    7    10  2
gottji01   1985    1      SFN     NL    51   6   10   2   0   3   3    0   1   1   30   0    0    4   0
greenda03  1985    1      SFN     NL    294  36  73   10  2   5   20   6   5   22  58   3    1    2   2
hammaat01  1985    1      SFN     NL    47   0   4    0   0   0   0    0   0   0   17   0    0    6   0
jeffcmi01  1985    2      SFN     NL    1    0   0    0   0   0   0    0   0   1   0    0    0    0   0
krukomi01  1985    1      SFN     NL    55   2   12   4   0   1   3    1   1   1   15   0    2    8   0
kuipedu01  1985    1      SFN     NL    5    0   3    0   0   0   0    0   0   1   0    0    0    2   0
lapoida01  1985    1      SFN     NL    60   4   10   1   0   0   6    0   0   6   11   0    0    5   0
laskebi01  1985    1      SFN     NL    30   1   4    0   0   0   1    0   0   3   12   0    1    5   0
lemasjo01  1985    1      SFN     NL    16   1   0    0   0   0   0    0   0   1   5    0    0    0   0
leonaje01  1985    1      SFN     NL    507  49  122  20  3   17  62   11  6   21  107  5    1    1   1
masonro01  1985    1      SFN     NL    11   1   1    0   0   0   0    0   0   0   5    0    1    0   0
mintogr01  1985    1      SFN     NL    8    1   0    0   0   0   1    0   0   1   6    0    0    0   0
moorebo01  1985    1      SFN     NL    2    0   0    0   0   0   0    0   0   0   0    0    0    0   0
nokesma01  1985    1      SFN     NL    53   3   11   2   0   2   5    0   0   1   9    0    1    0   0
rajsiga01  1985    1      SFN     NL    91   5   15   6   0   0   10   0   1   17  22   4    0    2   0
robinje01  1985    1      SFN     NL    0    0   0    0   0   0   0    0   0   0   0    0    0    0   0
roeniro01  1985    1      SFN     NL    133  23  34   9   1   3   13   6   2   35  27   3    0    1   1
thompsc01  1985    1      SFN     NL    111  8   23   5   0   0   6    0   0   2   10   0    0    1   0
trevial01  1985    1      SFN     NL    157  17  34   10  1   6   19   0   0   20  24   0    0    1   1
trillma01  1985    1      SFN     NL    451  36  101  16  2   3   25   2   0   40  44   0    1    11  2
uribejo01  1985    1      SFN     NL    476  46  113  20  4   3   26   8   2   30  57   8    2    5   0
wardco01   1985    1      SFN     NL    2    0   0    0   0   0   0    0   0   0   1    0    0    0   0
wellmbr01  1985    1      SFN     NL    174  16  41   11  1   0   16   5   2   4   33   1    4    5   1
willifr01  1985    1      SFN     NL    3    0   0    0   0   0   0    0   0   0   0    0    0    1   0
woodami01  1985    1      SFN     NL    82   12  20   1   0   0   9    6   1   5   3    0    0    1   0
youngjo02  1985    1      SFN     NL    230  24  62   6   0   4   24   3   2   30  37   1    1    1   1
```

### Total Career Hits

Since this data set contains multiple entries/rows for every player (every year they played), we need to aggregate their stats by year to come up with career hit totals. This can easily be done with `awk` arrays. Arrays in `awk` are tables with unique indices, so you can pass a column as its index and use `++` to count rows with the same index or `+=$col` to sum a particular column on rows with the same index. In the command below, `p[$1]++` creates an array that uses column 1 (playerID) as its index, then counts the number of duplicate index entries. This basically computes the length of a players career. `H[$1]+=10` is an array indexed by playerID, whose value is the sum of column 10 (Hits) for each playerID. Finally, the statement starting with `for (i in p)` prints the playerID, career length, and hit total in CSV format for every playerID. Also note that the field separator switch in `awk` is `-F`.

```bash
$ awk -F, '{p[$1]++;H[$1]+=$10} END {for (i in p) print i","p[i]","H[i]}' Batting.csv > H.csv
```

### All-time greatest hitters

A reverse sort on field 3 is all that is needed here. As expected, we see Pete Rose, Ty Cobb, Hank Aaron, Stan Musial, and Tris Speaker. Comparing these to [Baseball-Reference](http://www.baseball-reference.com/leaders/H_career.shtml), I noticed that I over-counted Pete Rose's career length by one year. A quick `grep` on rosepe01 confirmed that he has two entries for 1984 because he switched from Montreal to Cincinnati mid-season.

```bash
$ sort -n -t, -r -k3,3 H.csv | head -5 | column -s, -t
rosepe01   25  4256
cobbty01   24  4189
aaronha01  23  3771
musiast01  22  3630
speaktr01  22  3514
```

### Batting Averages

Now suppose I want to compute batting averages and add them as a column in `H.csv`. This can be done with another `awk` command, much like the one above. Then, use `join` to merge the two data sets on the first field, playerID. Note that the `awk` command's if-else statement avoids an arithmetic error by printing `0.00` if a player has zero "at bats".

```bash
$ awk -F, '{AB[$1]+=$8;H[$1]+=$10} END {for (i in H) if (AB[i] != 0) print i","H[i]/AB[i]; else print i",0.00"}' Batting.csv > AVG.csv
```
```bash
$ join -t, H.csv AVG.csv > HAVG.csv
```

Now repeat the above search showing the greatest hitters.

```bash
$ sort -n -t, -r -k3,3 HAVG.csv | head -5 | column -s, -t
rosepe01   25  4256  0.302853
cobbty01   24  4189  0.366363
aaronha01  23  3771  0.304998
musiast01  22  3630  0.330842
speaktr01  22  3514  0.344679
```

### The Great Bambino

Let's do a search for The Sultan of Swat. Since I know playerIDs start with the last name followed by the first two letters of their first name, I will do a `grep` on "ruthba". Sure enough, George Herman Ruth Junior comes up. In order to display his stats with column names, I will first save the `grep` search to its own file then `cat` the header and Babe's stats together. Again, I use to `cut` to be picky about which columns to view, and then `column` for its fancy formatting.

```bash
$ grep ruthba Batting.csv > greatbambino.csv
```
```bash
$ cat header.csv greatbambino.csv | cut -d, -f 1,2,4,5,8-14 | column -s, -t
playerID  yearID  teamID  lgID  AB   R    H    2B  3B  HR  RBI
ruthba01  1914    BOS     AL    10   1    2    1   0   0   2
ruthba01  1915    BOS     AL    92   16   29   10  1   4   21
ruthba01  1916    BOS     AL    136  18   37   5   3   3   15
ruthba01  1917    BOS     AL    123  14   40   6   3   2   12
ruthba01  1918    BOS     AL    317  50   95   26  11  11  66
ruthba01  1919    BOS     AL    432  103  139  34  12  29  114
ruthba01  1920    NYA     AL    457  158  172  36  9   54  137
ruthba01  1921    NYA     AL    540  177  204  44  16  59  171
ruthba01  1922    NYA     AL    406  94   128  24  8   35  99
ruthba01  1923    NYA     AL    522  151  205  45  13  41  131
ruthba01  1924    NYA     AL    529  143  200  39  7   46  121
ruthba01  1925    NYA     AL    359  61   104  12  2   25  66
ruthba01  1926    NYA     AL    495  139  184  30  5   47  150
ruthba01  1927    NYA     AL    540  158  192  29  8   60  164
ruthba01  1928    NYA     AL    536  163  173  29  8   54  142
ruthba01  1929    NYA     AL    499  121  172  26  6   46  154
ruthba01  1930    NYA     AL    518  150  186  28  9   49  153
ruthba01  1931    NYA     AL    534  149  199  31  3   46  163
ruthba01  1932    NYA     AL    457  120  156  13  5   41  137
ruthba01  1933    NYA     AL    459  97   138  21  3   34  103
ruthba01  1934    NYA     AL    365  78   105  17  4   22  84
ruthba01  1935    BSN     NL    72   13   13   0   0   6   12
```

How about the Colossus of Clout's career totals?

```bash
$ grep ruthba HAVG.csv | column -s, -t
ruthba01  22  2873  0.342105
```

### Why don't you just use Pandas?

Yes, [Pandas](http://pandas.pydata.org/) or [R](http://www.r-project.org/) can do all of the above data manipulation and *so much more*. Why use `awk`ward and opaque shell commands? Because they are efficient, built-in, and fantastic for simple data exploration and manipulation.



___
