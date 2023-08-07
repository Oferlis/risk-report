from flask import Flask, request, jsonify
from .helpers import *

app = Flask(__name__)


@app.route("/api/health/", methods=["GET"])
def health():
    return jsonify({"message": "Healthy"}), 200


@app.route("/api/report", methods=["POST"])
def get_risk_report():
    parsed_request = request.get_json()
    response = []
    return_status = 404
    for package_details in parsed_request:
        if validate_data(package_details):
            package_metadata = get_metadata(package_details)
            package_vul_list = get_vul_list(package_details)

            if len(package_vul_list) > 0:
                remediation = find_remediation(package_details)

            response.append(build_response(package_details,
                            package_metadata, package_vul_list, remediation))
            return_status = 200
        else:
            response.append("Invalid request")

    return jsonify(response), return_status


if __name__ == "__main__":
    app.run(debug=True, port=8001)
