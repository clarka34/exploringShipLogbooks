## Exploring Ship Logbooks

The Climatological Database for the World's Oceans (CLIWOC) contains a large collection of observational records of ship locations, weather, and interactions from 1750-1850. The goal of this project is to understand the effects of the slave trade on ship travel.

There are four main tasks necessary to accomplish this goal:

1. Scan logbook text for mentions of slaves and related phrases.
    - There is already a function on kaggle.com that searches for the word "slave"  in the logbooks, which will be helpful for finding references in different languages. However, we will expand the functionality of that script to link mentions of slaves to particular voyages and directions of travel.
2. Use GPS data to plot travel paths of individual voyages.
3. Link the mentions of slaves to the travel data.
    - We will determine if there are travel paths that are more common for trips involving slaves, and if trends change as the slave trade begins to end (mid 1800's).
4. Compare results with other historical indicators (i.e. number of battles a ship encounters).

