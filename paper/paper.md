---
title: 'DAPT: A system to '
tags:
  - Python
  - parameter
  - testing
authors:
  - name: Ben S. Duggan
    orcid: 0000-0002-1819-2130
    affiliation: 1
  - name: John Metzcar
    orcid: 0000-0002-0142-0387
    affiliation: 1
  - name: Paul Macklin
    orcid: 0000-0002-9925-0151
    affiliation: 1
affiliations:
 - name: Indiana University Luddy School of Informatics, Computing and Engineering
   index: 1
date: Febuary 2020
bibliography: paper.bib
---

# Summary

Modern agent based models (ABM) and other models require a large amount of parameter testing to determine which parameter make the model perform as desired.  It can be difficult to run a parameter set or develope a testing pipeline.  Additionally, testing a model is normally only conducted by one member of the team using a personal computer or high performance computer (HPC).  These issues can make parameter testing frustrating and burdensome.  To address these issues the Distributed Automated Parameter Testing (DAPT) library was created.  

DAPT allows parameters to be stored in a database (eg. Google Sheets or Firebase), run the parameter test in Python, and then save the data in the cloud.  Parameters are run sequentially in the database, and DAPT will move on to the next parameter set after successfully completing the previous one.  One of the best features of DAPT is that it allows for ad hoc. crowd sourcing of compute power.  The database allows for easier management of parameter sets and multiple people accessing the same set.  This allows anyone with the credentials and python script to run the parameters.  This allows for parameters to be distributed across a team or multiple HPCs.

# Usage

- Show flow chart
- Param input
- computation
- off-load data
- Other places for stuff?

# Example

- Basic examples in repo
- PhysiCell ECM usage


# Future plans

- Slack
- Logging
- cwl
- command line

# Acknowledgements

Grants.

We would like to thank Randy Heiland, Daniel Murphy, Brandon Fischer and the rest of the MathCancer lab.  They feedback and support through the development process was critical in the development of this tool.

# References
