# Python Interview Task
A real Python based interview task that I was asked to complete during an interview with a Fortune 500 company.

Given a very poor (very real) list of requirements, make a Python console program that fulfills them.

Here is the actual task requirements. They are very informal, but from my experience, is typical of lazy analyst lol.

---

### Details

There is an API (http://api.open-notify.org/) that provides information on the International Space Station. Documentation is provided via the website, along with sample request/response.


### Task

Implement a Python script that will accept the following command line arguments, along with any required information, and print the expected results

loc
```
print the current location of the ISS
Example: “The ISS current location at {time} is {LAT, LONG}”
```

pass
```
print the passing details of the ISS for a given location
Example: “The ISS will be overhead {LAT, LONG} at {time} for {duration}”
```

people
```
for each craft print the details of those people that are currently in space
```

---

# Interpretation
To really sum up what they want:
```
Create an HTTP client that hits the three endpoints (as described in the link) and processes and prints the returned JSON.

The endpoint you hit is based on console arguments, where some will need additional arguments (i.e pass)
```

The task is pretty open ended, so you can print what you please as long as it gives relevant information as described in the task.

In addition, you'll notice a lot of little caveats in the JSON payloadds, and it's really up to you to decide what parts you include or exclude in your output.

# My Submission
The following was used for the submission:

1. Python 3.7.3
2. [requests v2.22.0](https://2.python-requests.org/en/master/)

I attempted to showcase my understanding of the following:

1. Use of an HTTP library 
2. Data Validation
3. Exception handling for various situations (e.g `IndexError`, error check after hitting endpoint)
4. Processing JSON data into organized structures (e.g dictionaries)
5. Use of time functions
6. String formatting

To emphasize data validation, [latitude and longitude](http://www.geomidpoint.com/latlon.html) are in a range of `[-90, 90]` and `[-180, 180]`, respetively.

Validation will then be checking for the inputs existence, if they are numeric, and lastly ensuring that the inputs are within their intervals (inputs are the coordinates when using `pass`).

### Executing Script

```
Usage: poc_wh ['loc', 'people', 'pass'] [latitude: float] [longitude: float]
```

# Links

1. [requests](https://2.python-requests.org/en/master/)
2. [Latitude and Longitude math cheat sheet](http://www.geomidpoint.com/latlon.html)
3. [datetime](https://docs.python.org/3.3/library/datetime.html#datetime.datetime.utcfromtimestamp)
4. [exceptions](https://docs.python.org/2/library/exceptions.html)
