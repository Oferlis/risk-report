import json
import requests
import unittest

expected_response = [
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


class IntegrationTests(unittest.TestCase):

    def setUp(self) -> None:
        self.pusblishAPI = "http://localhost:8000"

        self.sample_data = [
            {"PackageManager": "Maven",
             "PackageName": "activemq:activemq-core",
             "PackageVersion": "1.4"},
        ]

        self.riskReportAPI = "http://localhost:8001"

    def tearDown(self) -> None:
        path = "./data.json"

    def test_health_check(self):
        publish_response = requests.request(
            "GET", f'{self.pusblishAPI}/api/health/')
        assert (publish_response.status_code == 200)
        risk_response = requests.request("GET",
                                         f'{self.riskReportAPI}/api/health/')
        assert (risk_response.status_code == 200)

    def test_report1(self):
        url = f"{self.pusblishAPI}/api/data"
        publish_payload = json.dumps({
            "PackageManager": "Maven",
            "PackageName": "activemq:activemq-core",
            "PackageVersion": [
                "1.4",
                "1.6"
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST", url, headers=headers, data=publish_payload)
        self.assertEqual(response.status_code, 201)

        risk_url = f"{self.riskReportAPI}/api/report"

        risk_payload = json.dumps([
            {
                "PackageManager": "Maven",
                "PackageName": "activemq:activemq-core",
                "PackageVersion": "1.4"
            }
        ])

        response = requests.request(
            "POST", risk_url, headers=headers, data=risk_payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.text)

        for data_item in data:
            self.assertEqual(data_item["packageId"],
                             expected_response[0]["packageId"])
            self.assertEqual(data_item["packageName"],
                             expected_response[0]["packageName"])
            self.assertEqual(data_item["packageManager"],
                             expected_response[0]["packageManager"])
            self.assertEqual(data_item["version"],
                             expected_response[0]["version"])
            self.assertEqual(data_item["vulnerabilities"],
                             expected_response[0]["vulnerabilities"])
            self.assertEqual(data_item["Remediation"],
                             expected_response[0]["Remediation"])

    def test_report2(self):
        url = f"{self.pusblishAPI}/api/data/"
        publish_payload = json.dumps({
            "PackageManager": "Nuget",
            "PackageName": "Microsoft.AspNetCore.Mvc",
            "PackageVersion": [
                "1.0.0", "1.0.2", "1.0.3", "1.0.4", "1.0.5", "1.0.6", "1.1.0", "1.1.1", "1.1.2", "1.1.3", "1.1.4"
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST", url, headers=headers, data=publish_payload)
        self.assertEqual(response.status_code, 201)

        risk_url = f"{self.riskReportAPI}/api/report"

        risk_payload = json.dumps([
            {
                "PackageManager": "Nuget",
                "PackageName": "Microsoft.AspNetCore.Mvc",
                "PackageVersion": "1.0.0"
            }
        ])

        response = requests.request(
            "POST", risk_url, headers=headers, data=risk_payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.text)

        for data_item in data:
            self.assertEqual(data_item["Remediation"]["FixVersion"],
                             "1.0.4")
            self.assertEqual(data_item["Remediation"]["RemediationStatus"],
                             "Remediated")

    def test_report3(self):
        headers = {
            'Content-Type': 'application/json'
        }
        risk_url = f"{self.riskReportAPI}/api/report"

        risk_payload = json.dumps([
            {
                "PackageManager": "Nuget",
                "PackageName": "Microsoft.AspNetCore.Mvc",
                "PackageVersion": "1.1.1"
            }
        ])

        response = requests.request(
            "POST", risk_url, headers=headers, data=risk_payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.text)

        for data_item in data:
            self.assertEqual(data_item["Remediation"]["FixVersion"],
                             "1.1.3")
            self.assertEqual(data_item["Remediation"]["RemediationStatus"],
                             "Remediated")
