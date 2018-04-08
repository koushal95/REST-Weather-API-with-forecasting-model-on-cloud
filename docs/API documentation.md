# Endpoints and Usage of the API

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
