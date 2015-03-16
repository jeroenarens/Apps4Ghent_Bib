
Apps4Ghent_Bib
---------------

This project focuses on the need of the library to have a handy and well-designed tool/website which visualizes the library data and interacts with the user to make up queries to find out interesting things about this information.<br />
The website consists of four parts: <br />
<ul>
<li> <b> FrontEnd </b>: here, the rendering and visualisation of the processed/queried library data will be fulfilled. Highmaps is used for these functions </li>
<li> <b> BackEnd </b>: Here we use Django to process the incoming requests from the frontend and get the requested results from the database. </li>
<li> <b> Non-Relational Database </b>: To store the data, MongoDB is used to store the library data. </li>
<li> <b> Import & Mapping </b>: To import the data, the API from the Open Datatank will be used. Before importing the data, a mapping will be done from csv to json linked data (json LD) </li>
</ul>
Coding style
---------------
Before you want to help us coding, make sure to follow the coding conventions from Django (see [Django coding style](https://docs.djangoproject.com/en/1.7/internals/contributing/writing-code/coding-style/)). <br />
Besides these coding conventions, please make sure your editor removes whitespace at the end of a line and let the tabs be changed to 4 spaces instead.

Documentation
--------------
To 

