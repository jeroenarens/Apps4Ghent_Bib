
Apps4Ghent_Bib
---------------

This project focuses on the need of the library to have a handy and well-designed tool/website which visualizes the library data and interacts with the user to make up queries to find out interesting things about this information.<br />
The website consists of four parts: <br />
<ul>
<li> <b> FrontEnd </b>: here, the rendering and visualisation of the processed/queried library data will be fulfilled. Highmaps is used for these functions </li>
<li> <b> BackEnd </b>: Here we use Django to process the incoming requests from the frontend and get the requested results from the database. </li>
<li> <b> Non-Relational Database </b>: To store the data, Postgresql is used to store the library data. </li>
<li> <b> Import & Mapping </b>: To import the data, an R script is written to import and clean the data </li>
</ul>
Coding style
---------------
Before you want to help us coding, make sure to follow the coding conventions from Django (see [Django coding style](https://docs.djangoproject.com/en/1.7/internals/contributing/writing-code/coding-style/)). <br />
Besides these coding convenmetions, please make sure your editor removes whitespace at the end of a line and let the tabs be changed to 4 spaces instead.
Also javascript conventions should be used for the visualisation part(see [Javascript Convention tools](https://google-styleguide.googlecode.com/svn/trunk/javascriptguide.xml)).
For cleaning the data with R, please use the conventions found in the following link: [R Convention tools](https://google-styleguide.googlecode.com/svn/trunk/Rguide.xml)

Progress Report Documentation
--------------
In the documents/report folder, you can find the documentation related to the progress of this project. To make a pdf output file, please make a map called 'output' in the same directory. <br />
Afterwards, execute the following command: <code> make </code>. You will see the pdf file in the output folder.
For the developers under you of our code, please check our wiki 

Apps4Ghent_Libary
------------------
In the apps4ghent library, you can find following directories:
<ul>
<li> <b> templates </b>: Here, the html files are pushed for the frontend of the website. </li>
<li> <b> static </b>: The javascript, css and image files will be put here to style the website and to make it interactive. </li>
<li> <b> Apps4Ghent_Library </b> When wanting to add some url subdirectories (e.g. /api) or to edit the settings of the webserver, you need to be in this directory. </li>
<li> <b> apps4ghent </b> The app/tool itself is situated here and can be used to set up json serializers, to set up models, tests, views,.... </li>
</ul>
Besides these directories, also a manage.py file is present which will be used to run the project and a requirements.txt file to specify which packages need to be installed to let the webserver run.

How to run?
-------------
before running the project itself, please install python3.4 ([Link](https://www.python.org/downloads/)) and Django 1.7 ([Link](https://docs.djangoproject.com/en/1.7/topics/install/)), Pip ([link](https://pypi.python.org/pypi/pip)) and Postgresql ([link](http://www.postgresql.org/)).
Also be sure to have a postgresql server locally installed.
To set up the django project, first install the packages from the requirements file with the following command: 
<br />
 <code> pip3 install -r requirements.txt </code>
<br/>
Then, import the database onto your postgresql server using the fullimport.sql file in the database folder<br>
Afterwards, set up the database with in python
<br />
 <code> python3 manage.py syncdb </code>
<br />
Now you can start the server by typing: 
<br />
<code> python3 manage.py runserver </code>
<br/>
For a more detailed documentation about cleaning/importing the data or using the API, please read our [Wiki](https://github.com/jeroenarens/Apps4Ghent_Bib/wiki)
<br/> <br/>
Be aware that you do not need to change any settings, you should be able to run this project locally without changing anything to these settings!
