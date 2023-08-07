import json
import unittest
from RiskReport import app, get_metadata, get_vul_list

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
        # "Remediation":
        # {
        #     "FixVersion": "1.6",
        #     "RemediationStatus": "Remediated"
        # }
    }
]


class TestRiskReportAPI(unittest.TestCase):

    def setUp(self):
        # Create a test client for the app
        self.app = app.test_client()
        self.app.testing = True

    def test_get_metadata(self):
        params = {"PackageManager": "Python",
                  "PackageName": "requests", "PackageVersion": "1.0.0"}
        response = get_metadata(params)

        print(response)
        assert response["packageId"] == 'Python#-#requests#-#1.0.0'
        assert response["type"] == 'Python'
        assert response["name"] == 'requests'

    def test_vul_api_call(self):
        params = {"PackageManager": "Maven",
                  "PackageName": "activemq:activemq-core",
                  "PackageVersion": "1.4"}

        response = get_vul_list(params)
        assert len(response) == 1
        for item in response:
            assert item["cve"] and \
                item["description"] and \
                item["cwe"] and \
                item["published"] and \
                item["severity"]

    def test_risk_report_post(self):
        json_data = [{"PackageManager": "Maven",
                      "PackageName": "activemq:activemq-core",
                      "PackageVersion": "1.4"}]
        response = self.app.post('/api/', json=json_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(data[0]["packageId"],
                         expected_response[0]["packageId"])
        self.assertEqual(data[0]["packageName"],
                         expected_response[0]["packageName"])
        self.assertEqual(data[0]["packageManager"],
                         expected_response[0]["packageManager"])
        self.assertEqual(data[0]["version"],
                         expected_response[0]["version"])
        self.assertEqual(data[0]["vulnerabilities"],
                         expected_response[0]["vulnerabilities"])
