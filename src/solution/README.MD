# Risk Report Execrcise solution

The Project consists of two Flask servers, written in Python:
1. PublishPackage
2. RiskReport

## PublishPackage
Holds the records for packages and their version. 
The records are written to a file called data.json placed in the root dir, the path can be changed.

## How to run
In the PublishPackage folder, run the command ```python PublishPackageVersion.py```
The server will run on port 8000 on localhost

### Endpoints:

1. GET /api/health - API health check, should return status 200 on GET 
2. GET /api/data/ - returns the list of all packages listed in the memory
3. POST /api/data/ - is used to add packages. The request body should be in the following format:
    ```
    {'PackageManager': 'Nuget',
     'PackageName': 'Microsoft.AspNetCore.Mvc',
     'PackageVersion': ['1.0.0'....]}
    ```
4. GET /api/data/package_manager>/package_name>/ - returns a specific package info
5. GET /api/data/package_manager>/package_name>/package_version>/ - returns a list of the next version from the specified version 

## RiskReport
When passing the API a list of packages, it will return a report for each package with its metadata, vulnerabilities and the next package version that solve the vulnerabilities, if exists.
NOTE: in order for the API to work, the package posted should exist in the PublishPackage API.

The request body should be in the following format: 
```
[
  { "PackageManager": "Maven",
  "PackageName": "activemq:activemq-core",
  "PackageVersion": "1.4" }
  ]
```

## How to run
In the PublishPackage folder, run the command ```python PublishPackageVersion.py```
The server will run on port 8000 on localhost

## Endpoints
1. GET /api/health - API health check, should return status 200 on GET.
2. POST /api/report - will return the detailed report for the packages. 

