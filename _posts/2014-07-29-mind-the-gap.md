---
layout: page
permalink: /mind-the-gap/
---
## Zipfian Capstone Project

___
<iframe src="/projects/mind-the-gap/" marginwidth="0" marginheight="0" scrolling="no" width="810px" height="630px" frameborder="0"></iframe>
___

## Gap in the Supply of Projects

[DonorsChoose](http://donorschoose.org) is an organization that enables educators to crowd-source funds for classroom projects, realizing educational opportunities that would not have otherwise been possible.

DonorsChoose.org asked Zipfian Academy to provide data-driven insights into why they see a gap in the supply of classroom projects on their platform. My approach to solving this problem was to seek out potential school districts based on their economic and financial similarity to the most active DonorsChoose.org districts.

## District Similarity

District recommendations are based on the [cosine-similarity](http://en.wikipedia.org/wiki/Cosine_similarity) between the recommended district and active DonorsChoose districts that have more than 3 projects per year. 

Python scripts for the analysis and data wrangling are available on Github at [github.com/abshinn/mind-the-gap](http://github.com/abshinn/mind-the-gap). Code for the interactive d3.js visualization is [available here](https://github.com/abshinn/abshinn.github.io/tree/master/projects/mind-the-gap).
