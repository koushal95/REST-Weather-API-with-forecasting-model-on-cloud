# REST Api using flask deployed on cloud
Web service api for serving weather data built using flask and flask_restful.

This repository contains code to implement a RESTful service to serve weather data of Cincinnati of past five years. The RESTful service is implemented using FLASK, FLASK_RESTFUL frameworks.

This is a markdown specification about the REST API developed to serve weather data of Cincinnati for past five years.

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
**201** | Successfully added the weather information in the request object's body to the data, and returns the date that is added. The date is returned in JSON format.
