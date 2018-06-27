# pyedid
for linux get EDID information and parsing.


e.g.

import pyedid

print pyedid.get_monitor_info()

------------------
$/usr/bin/python2.7 /home/local_script/1.local_test.py

$1: DELL U2410	DVI-I-1	primary	J257M9AM05DL	2009.10(Oct)	hostname	2018-06-27 09:30:21.645564

$2: DELL U2414H	DP-1	normal	4CWX759M99HS	2015.9(Sep) hostname 2018-06-27 09:30:21.645590

#num:model  port  connect SN  date_of_Mfg date
