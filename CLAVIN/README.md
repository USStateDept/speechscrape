Speech Scrape from eDiplomacy's Geo Team
=============

Geotagging the public speeches of the US State Department


Install
--------------

Requires
- [MongoDB](https://www.mongodb.org/downloads)
- [CLAVIN Server](http://clavin.bericotechnologies.com/site/tutorials/installation.html)
- Python with or without virtualenv

Set environment variables (maybe just subdir in the future)

```
export/set SPEECH_DATADIR=/some/dir/
export/set SPEECH_PROCESSEDDIR=/some/dir/
```

Install requirements

```
pip install -r requirements.txt
```

Current Status
-----------------
Currently not working due to the difference between some of the pages linked from the speeches.  
Also, there were memory issues with hitting CLAVIN too fast.

Future
--------------------
TBD.  Ideas are welcome.


