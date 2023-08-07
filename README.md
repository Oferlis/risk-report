# Risk Report

A Checkmarx SCA coding exercise.
SCA is the name of our product (Software Composition Analysis) and we provide the users with information on what third party open source packages they use in their code, if these package have any vulnerabilities and how to fix those vulnerabilities.

This exercise simulates a very basic flow of finding out what vulnerabilities the packages we found in the code have and how should the user fix them.


## Requirements

1. **We prefer C#, but other languages are also fine**

   If you prefer to implement it in a different language, let us know beforehand.

2. **It's not a riddle**

   If something isn't clear, ask us. Don't waste time on figuring out or guess our intentions when they're not obvious.
   We appreciate feedback.

3. **The code should be clean and readable**

   There's no need for over-engineering but we do wish to see a good separation of concerns. The code should be simple, clean and testable. It should align with the SOLID principles.

4. **It needs to work**

   We want to see a working solution, even if it's not complete. A compiled and running code with missing features is
   better than a solution that doesn't compile or errors out.

5. **Use in-memory storage**

   Do not setup a real database. Use static members or any in-memory storage library. Still, adding a persistancy solution shouldn't require a complete refactor of your project.



## Specifications

We want to build a **REST API** to get SCA risk report. Users will be able to send a list of packages that they use and receive back information on those packages and the vulnerabilities in them.

For this purpose you will have available two public APIs that we provide (package information and package vulnerabilities) and will need to provide two new APIs to your service (Publish package versions and Get risk report).

### Desired logic and flow
1. The user publish package/versions info using Publish package versions API that should be created.
   1. Example of a Nuget packages and its versions:
      * PackageManager: Nuget 
      * PackageName:  Microsoft.AspNetCore.Mvc 
      * PackageVersion: 1.0.0, 1.0.2, 1.0.3, 1.0.4, 1.0.5, 1.0.6, 1.1.0, 1.1.1, 1.1.2, 1.1.3, 1.1.4
2. User call RiskReport API with Package Manager, Name and Version. 
   1. Example: Nuget, Microsoft.AspNetCore.Mvc, 1.0.2
3. The required response:
   1. Metadata about the package taken from the given the package information API
   2. Package vulnerabilities taken from the given package vulnerabilities API
   3. Remediation – the next version that has ZERO vulnerabilities
      1. List of known versions should be extract from in-memory data which was populated earlier by you using the publish API
      2. This list can be used to check with the package vulnerabilities API if they have a vulnerability or not

### Publish Package Versions

A user should be able to publish to the service the known versions of a package.
You should save the information in your data storage for use in the Get Risk Report API
Publish request should include the package manager, package name, and a list of its versions. 

### Get Risk Report

A user should be able to ask for a risk report for a list of packages.
Each package is defined by three fields:
1. Package Manager - one of the following: Python, Npm, Nuget, Maven, Ios, Php, Ios, Go, Cpp, Ruby
2. Package Name - string
3. Package Version - string

You can get the package information from the following API:

    GET https://api-sca.checkmarx.net/public/packages/{PackageManager}/{PackageName}/versions/{PackageVersion}

For instance:

    GET https://api-sca.checkmarx.net/public/packages/Python/requests/versions/1.0.0


This API returns information about the package. For instance, the above package will return:

```json
{
   "packageId": "Python#-#requests#-#1.0.0",
   "legacyPackageId": "Python-requests-1.0.0",
   "type": "Python",
   "name": "requests",
   "version": "1.0.0",
   "projectHomePage": "https://requests.readthedocs.io",
   "releaseDate": "2012-12-17T15:00:05.11+00:00",
   "keywords": [],
   "authors": "Kenneth Reitz",
   "projectUrl": "https://pypi.org/project/requests/",
   "authorEmail": "me@kennethreitz.org",
   "sourceRepository": "https://requests.readthedocs.io",
   "preRelease": false,
   "requirements": [],
   "packageFiles": "[{\"Id\":\"requests-1.0.0.tar.gz\",\"PackageType\":null,\"PythonVersion\":null,\"Size\":335548,\"Url\":\"https://files.pythonhosted.org/packages/46/da/94c0fd6ff79b85befc3b528cf3771700def274c52b347bf12eeaa466f34c/requests-1.0.0.tar.gz\",\"UploadTime\":\"2012-12-17T15:00:05.110522Z\",\"PackageId\":{\"Identifier\":\"Python-requests-1.0.0\"},\"PrioritizationId\":null,\"PrioritizationTime\":null}]"
}
```
For this exercise purposes you should use only these fields from the response:
packageId, type, name, version, releaseDate

You can get the vulnerabilities information from the following API:


    POST https://api-sca.checkmarx.net/public/vulnerabilities/packages

with the following body structure as request:

```json
[
   {
      "PackageName": "activemq:activemq-core",
      "PackageManager": "Maven",
      "Version": "1.4"
   }
]
```

and receive the following response:

```json
[
   {
      "packageName": "activemq:activemq-core",
      "packageManager": "Maven",
      "version": "1.4",
      "vulnerabilities": [
         {
            "cve": "CVE-2018-11775",
            "vulnerabilityVersion": 3,
            "description": "TLS hostname verification when using the Apache ActiveMQ Client before 5.15.6 was missing which could make the client vulnerable to a MITM attack between a Java application using the ActiveMQ client and the ActiveMQ server. This is now enabled by default.",
            "type": "Regular",
            "cvss2": {
               "authentication": "NONE",
               "collateralDamagePotential": null,
               "targetDistribution": null,
               "integrityImpact": "PARTIAL",
               "baseScore": "5.8",
               "attackVector": "NETWORK",
               "attackComplexity": "MEDIUM",
               "confidentiality": "PARTIAL",
               "availability": "NONE",
               "exploitCodeMaturity": "8.6",
               "remediationLevel": null,
               "reportConfidence": null,
               "confidentialityRequirement": null,
               "integrityRequirement": null,
               "availabilityRequirement": null,
               "severity": "Medium"
            },
            "cvss3": {
               "privilegesRequired": "NONE",
               "userInteraction": "NONE",
               "scope": "UNCHANGED",
               "integrity": "HIGH",
               "baseScore": "7.4",
               "attackVector": "NETWORK",
               "attackComplexity": "HIGH",
               "confidentiality": "HIGH",
               "availability": "NONE",
               "exploitCodeMaturity": null,
               "remediationLevel": null,
               "reportConfidence": null,
               "confidentialityRequirement": null,
               "integrityRequirement": null,
               "availabilityRequirement": null,
               "severity": "High"
            },
            "cwe": "CWE-295",
            "published": "2018-09-10T20:29:00Z",
            "updateTime": "2022-07-06T06:46:41Z",
            "severity": "High",
            "affectedOss": null,
            "references": [
               {
                  "comment": "",
                  "type": "Advisory",
                  "url": "https://activemq.apache.org/security-advisories.data/CVE-2018-11775-announcement.txt"
               }
            ],
            "created": "2019-06-25T10:16:39Z",
            "credit": null,
            "creditGuid": null,
            "kev": null,
            "exploitDb": null
         }
      ]
   }
]
```

From this json you can take the following vulnerability fields for the report:
cve, description, cwe, published, severity

### Notice
Some had issue with working with this REST API and it turned out to be a missing User-Agent header.
If you also have the same issue, add the following value to that header: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

#### Remediation
Calculate remediation for each package. What is the first next version of the package that doesn't have a vulnerability.
Remediation includes two fields:
1. FixVersion (if such exist)
2. RemediationStatus: Remediated - If a remediation was found, NoRemediationExists - If all known next versions are vulnerable.

You can assume all versions are in proper semver format 

#### Response
The response json should be in the following format:

```json
[
   {
      "packageId": "Maven#-#activemq:activemq-core#-#1.4",
      "packageName": "activemq:activemq-core",
      "packageManager": "Maven",
      "version": "1.4",
      "releaseDate": "2012-12-17T15:00:05.11+00:00",
      "vulnerabilities": [
         {
            "cve": "CVE-2018-11775",
            "description": "TLS hostname verification when using the Apache ActiveMQ Client before 5.15.6 was missing which could make the client vulnerable to a MITM attack between a Java application using the ActiveMQ client and the ActiveMQ server. This is now enabled by default.",
            "cwe": "CWE-295",
            "published": "2018-09-10T20:29:00Z",
            "severity": "High"
         }
      ],
      "Remediation":
      {
         "FixVersion": "1.6",
         "RemediationStatus": "Remediated"
      }
   }
]
```

### Write unit tests

Cover your code with unit tests as you see fit.

### How to test your code
You can use the following package and versions:
* PackageManager: Nuget
* PackageName:  Microsoft.AspNetCore.Mvc
* PackageVersion: 1.0.0, 1.0.2, 1.0.3, 1.0.4, 1.0.5, 1.0.6, 1.1.0, 1.1.1, 1.1.2, 1.1.3, 1.1.4

last time this was updated, 1.04, 1.0.5, 1.0.6, 1.1.3, 1.1.4 were without vulnerabilities.
If the data changed and you are having problems finding versions for your test, feel free to contact us and we'll provide them for you.
