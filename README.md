# REST Api using flask deployed on cloud
Web service api for serving weather data built using flask and flask_restful.

This repository contains code to implement a RESTful service to serve weather data of Cincinnati of past five years. The RESTful service is implemented using FLASK, FLASK_RESTFUL frameworks.

This is a markdown specification about the REST API developed to serve weather data of Cincinnati for past five years.

## Overview:
1. Schemes

* HTTP

2. Endpoints

* /historical

   * GET

   * POST

* /historical/'date'

    * GET

    * DELETE


## Schemes:

* HTTP

### historical
This endpoint has information about the historical weather data of Cincinnati.

#### GET
/historical 

Description: List of all dates for which weather information is available. 

Parameters: None. There are no parameters for this, we just need to use the endpoint('/historical').

Response: 

Code  | Description
----  | ---
**200** | *JSON array of dates in 'YYYYMMDD' format.*

#### GET
/historical/'date YYYYMMDD'

Description: This returns the weather information for the passed parameter date. If no information is available error is returned.

Parameter: The parameter value is a string of date in 'YYYYMMDD' format. 

Datatype: String
 
Response: 

Code  | Description
---   | ---
**200** | *JSON array of weather information containing data for DATE, TMAX, TMIN.*
**404** | *Error message in JSON format.*

#### POST
/historical

Description: Adds weather information for a particular date. The date is taken from the Request object body.

Parameters: None. There are no explicit parameters, the date is extracted from the request object body.

Response:

Code  | Description
--- | ---
**201** | *Successfully added the weather information in the request object's body to the data, and returns the date that is added. The date is returned in JSON format.*

#### DELETE
/historical/'date YYYYMMDD'

Description: Deletes the weather information for the date passed as parameter.

Parameter: The parameter value is a string of date in 'YYYYMMDD' format. 

Datatype: String.

Response:

Code  | Description
--- | ---
**204** | *Sucessfully deleted the weather information for specified date in the parameter.*

## Update: Forecast model coming up
I am working on a model, to forecast the weather information for future dates accounting to the observed trends and seasonality of the data. 

## About Forecast model
I came across this interesting tool developed by Facebook research team. I wrote a few pages about it. Head over to wiki of this repository to view those pages. The notebook 'forecasting model' is my first attempt to use this tool. I will soon use this tool to forecast and integrate it to the API.

I have pushed a PDF version of my notebook with an example of using Prophet. This goes with the wiki page 'More about Prophet'.
## Update: Forecast model built and integrated!!

### forecast
This endpoint has forecasting feature for the next seven days. 

#### GET
/forecast/'date YYYYMMDD'

Description: Forecasts the weather information for the next seven days starting with the date passed as parameter. The forecast is done using fbprophet.

Parameter: The parameter value is a string of date in 'YYYYMMDD' format.

Datatype: String.

Response:

Code  | Description
--- | ---
**200** | *Returns a JSON array containing weather information for the next seven days starting with the date passed as parameter.

## Update: Added View pages
I used Angular JS to bind the data from the API onto the View page. I have used Google Charts to plot the forecast for next seven days. 
