from flask import Flask, request, jsonify
import json

db = "./data.json"
app = Flask(__name__)


class PackageInfo:
    def __init__(self, PackageManager, PackageName, PackageVersion):
        self.PackageManager = PackageManager
        self.PackageName = PackageName
        self.PackageVersion: list = PackageVersion


def load_data() -> [PackageInfo]:
    try:
        with open(db, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data


def get_package(package_manager, package_name):
    loaded_data: [PackageInfo] = load_data()
    data = next((item for item in loaded_data
                if item["PackageManager"] == package_manager
                and item["PackageName"] == package_name), None)

    return data


def save_data(data):
    with open(db, "w") as file:
        json.dump(data, file, indent=4)


@app.route("/api/health/", methods=["GET"])
def health():
    return jsonify({"message": "Healthy"}), 200


@app.route("/api/data/", methods=["GET"])
def get_list():
    data = load_data()
    return jsonify(data), 200


def duplicate_exists(new_data, loaded_data):
    for item in loaded_data:
        if item["PackageManager"] == new_data["PackageManager"]\
                and item["PackageName"] == new_data["PackageName"]:
            return True
    return False


@app.route("/api/data/", methods=["POST"])
def add_package():
    new_data = request.get_json()
    if "PackageName" in new_data and "PackageManager" in new_data and "PackageVersion" in new_data:
        package_info = PackageInfo(
            new_data["PackageManager"], new_data["PackageName"], new_data["PackageVersion"])

        loaded_data = load_data()
        if duplicate_exists(new_data, loaded_data):
            return jsonify({'message': 'Package already exists'}), 409
        loaded_data.append(package_info.__dict__)
        save_data(loaded_data)
        return jsonify({'message': 'Data created successfully'}), 201
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
    # return a list of next versions
    data = get_package(package_manager, package_name)
    if data:
        versions = data["PackageVersion"]
        current_version_idx = versions.index(package_version)

        if len(versions) > (current_version_idx + 1):
            return jsonify(versions[current_version_idx + 1:]), 200
        return jsonify({'message': 'Next versions not found'}), 404
    return jsonify({'message': 'Invalid path'}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8000)
