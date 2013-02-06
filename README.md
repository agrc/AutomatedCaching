Automated Caching
================

agrc's auto update continuous caching library.

##Running from source##

Change `agrc\caching\secrets.cfg.sample` to `agrc\caching\secrets.cfg` and update the username and password settings

If importing of modules is not working you will need to update your 
[PYTHONPATH](http://greeennotebook.com/2010/06/how-to-change-pythonpath-in-windows-and-ubuntu/ "see this blog for more information"). On windows, put the `path` to the `AutomatedCaching` folder inside the `automated_caching.pth` folder with escaped forward slashes. 

eg: `C:\\Projects\\AutomatedCaching`

Then move the file into your site packages folder. For arcgis users it will be something like

`C:\Python27\ArcGISx6410.1\Lib\site-packages`

running 

`for i in sys.path:`
`     print i`

should verify that your location has been added.