from flask import Flask, request, jsonify
from helpers import *


app = Flask(__name__)


class PackageInfo:
    def __init__(self, PackageManager, PackageName, PackageVersion):
        self.PackageManager = PackageManager
        self.PackageName = PackageName
        self.PackageVersion: list = PackageVersion


@app.route("/api/health/", methods=["GET"])
def health():
    return jsonify({"message": "Healthy"}), 200


@app.route("/api/data/", methods=["GET"])
def get_list():
    data = load_data()
    return jsonify(data), 200


@app.route("/api/data/", methods=["POST"])
def add_package():
    new_data = request.get_json()
    if "PackageName" in new_data and "PackageManager" in new_data and "PackageVersion" in new_data:
        package_info = PackageInfo(
            new_data["PackageManager"], new_data["PackageName"], new_data["PackageVersion"])

        msg, status = handle_new_data(package_info)
        return jsonify(msg), status
    else:
        return jsonify({'message': 'Invalid data'}), 400


@app.route("/api/data/<string:package_manager>/<string:package_name>/", methods=["GET"])
def get_specific_package(package_manager, package_name):
    data = get_package(package_manager, package_name)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'message': 'Package not found'}), 404


@app.route("/api/data/<string:package_manager>/<string:package_name>/<string:package_version>/", methods=["GET"])
def get_next_versions(package_manager, package_name, package_version):
    data = get_package(package_manager, package_name)

    if data:
        msg, status = find_next_versions(data, package_version)
        return jsonify(msg), status

    return jsonify({'message': 'Invalid path'}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8000)
