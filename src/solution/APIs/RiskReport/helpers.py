import requests
import json


def get_package_info_api_url(PackageManager, PackageName, PackageVersion):
    return f"https://api-sca.checkmarx.net/public/packages/{PackageManager}/{PackageName}/versions/{PackageVersion}"


def create_package_info_api_call(PackageManager, PackageName, PackageVersion):
    try:
        url = get_package_info_api_url(
            PackageManager, PackageName, PackageVersion)
        payload = {}
        headers = {"User-agent":
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

        response = requests.request("GET", url, headers=headers, data=payload)

        full_response = response.json()

        filtered_fields = dict(packageId=full_response["packageId"],
                               type=full_response["type"],
                               name=full_response["name"],
                               version=full_response["version"],
                               releaseDate=full_response["releaseDate"])

        return filtered_fields

    except requests.exceptions.RequestException as e:
        return "error fetching metadata"


def get_metadata(params):
    return create_package_info_api_call(params["PackageManager"],
                                        params["PackageName"],
                                        params["PackageVersion"])


def validate_data(request_params):
    if "PackageName" in request_params and \
        "PackageManager" in request_params and \
            "PackageVersion" in request_params:

        return True

    return False


def get_vul_list(params):
    url, payload, headers = create_vul_request(params)

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return parse_vul_response(response)
    except requests.exceptions.RequestException as e:
        return "error fetching vulnerabilities"


def parse_vul_response(response):
    vul_list = response.json()[0]["vulnerabilities"]

    filtered_response = []
    for item in vul_list:
        filtered = {"cve": item["cve"],
                    "description": item["description"],
                    "cwe": item["cwe"],
                    "published": item["published"],
                    "severity": item["severity"]}
        filtered_response.append(filtered)
    return filtered_response


def create_vul_request(params):
    req_body = [{"PackageName": params["PackageName"],
                "PackageManager": params["PackageManager"],
                 "Version": params["PackageVersion"]}]

    url = "https://api-sca.checkmarx.net/public/vulnerabilities/packages"
    payload = json.dumps(req_body)
    headers = {"User-agent":
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

    return url, payload, headers


def build_response(package_details, package_metadata, vul_list, remediation):
    return {"packageId": package_metadata["packageId"],
            "packageName": package_details["PackageName"],
            "packageManager": package_details["PackageManager"],
            "version": package_metadata["version"],
            "releaseDate": package_metadata["releaseDate"],
            "vulnerabilities": vul_list,
            "Remediation": remediation
            }


def get_next_versions(package_details):
    url = f"http://localhost:8000/api/data/{package_details['PackageManager']}/{package_details['PackageName']}/{package_details['PackageVersion']}"
    try:
        response = requests.request("GET", url, headers={}, data={})
        if response.status_code != 200:
            return None
        return response.json()
    except requests.exceptions.RequestException as e:
        return "error fetching next version"


def find_remediation(package_details):
    next_versions = get_next_versions(package_details)
    remedy = {"RemediationStatus": "NoRemediationExist"}

    for version in next_versions:
        params = {'PackageManager': package_details['PackageManager'],
                  'PackageName': package_details['PackageName'],
                  'PackageVersion': version}
        if len(get_vul_list(params)) == 0 and version != 'e':
            remedy = {"FixVersion": version,
                      "RemediationStatus": "Remediated"}
            break
    return remedy
