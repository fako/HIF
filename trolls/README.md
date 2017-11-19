Robo Roaster
============

Robots slowly take over our work, but now they also take on our favorite pass time. 
Insulting people on the internet! 

Installation
------------

Your environment should be setup with [minicoda](https://conda.io/miniconda.html).
You'll need to install opencv into your conda by activating the environment and then running

```bash
conda install -c menpo opencv
```

Downloads
---------

You'll need to download and unzip a special opencv.zip file. 
There is a XML training file that needs to be read from there.

You'll also need to download the trolls.sql data and load it into the database. 
Use the following command and specify the user and password if needed with your setup.

```bash
cat trolls.sql | mysql datascope
```

Configuration
-------------

There are a few variables in bootstrap.py that you need to set correctly

* ```PATH_TO_OPENCV``` should point to the path of the unzipped opencv.zip
* ```SERVER_IP``` should be an IP where the computer controlling the robots is listening
* ```VIDEO_DEVICE``` should be the video interface number that the webcam is connected to
