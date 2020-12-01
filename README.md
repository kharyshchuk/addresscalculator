# Overview

The project is intended for calculating distances between destinations in csv file.
File must contains next columns: Point(destination name), Latitude, Longitude (float)

## Running
For command line options invoke:

    $ docker-compose up

    
Notes: You also can stop addresscalculator container by `docker stop id_addresscalculator `and debug it from IDE. connection to Mongo possible outside using localhost:21017

## Scope

The library provides the following methods:

*   /getAddresses [POST]. Uploading file with addresses data and obtaining result data with distances and addresses descriptions. Example of use: 

    `$ curl -X Gi -X POST -H "Content-Type: multipart/form-data" -F "file=@/path/to/file.csv" -F 'client_type=http' http://localhost:5000/getAddresses`
    
    where the client_type can be: http or gis. This is a type of data processing.

*   /getResult [GET]. Obtaining the result of calculations by result_id Example of use: 
    
    `$ curl -X GET "http://localhost:5000/getResult?result_id=uuid"`

Dependencies

*   flask
*   flask-restful
*   arcgis
*   pandas
*   Flask-PyMongo