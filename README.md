# rpki-adoption
Code used by RPKI adoption studies

Measuring RPKI ROV

1- Downloading BGP data and extracting Prefix-origin pairs
$ python pybgpstream_getRIBs.py 20240430
$ python extractingPOs.py 20240430

2-Download and merge RPKI data
$ python getRPKIhistdata.py 20240430
$ python mergingROAs.py 20240430

3-Compute RPKI statut and cleaning bogons and long prefixes (>/24 or >/64)
$ python addingPO_RPKIstatus.py 20240430
$ python cleaningPOs.py 202404

4-Compute RPKI-invalids counts per direct peer to collector
$ python getting_dp_RPKIviu.py

5-Graph: dates need to be adjusted on the code depending on dates for which the data was processed with the same workflow)
5.1 AS per prefix origin count and RPKI invalid count (one date)
$ python plottingRPKIvalidity.py 
5.2 RPKI filtering over time (needs list of dates to include in the figure)
$ python plottingROVoverTime.py
5.3 RPKI invalid count per AS (needs lists of dates and ASes to consider)
$ python plotting_invalids_perASN.py
