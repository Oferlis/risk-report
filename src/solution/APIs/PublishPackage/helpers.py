import json

db = "./data.json"


def duplicate_exists(new_data, loaded_data):
    for item in loaded_data:
        if item["PackageManager"] == new_data.PackageManager\
                and item["PackageName"] == new_data.PackageName:
            return True
    return False


def load_data():
    try:
        with open(db, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data


def save_data(data):
    with open(db, "w") as file:
        json.dump(data, file, indent=4)


def get_package(package_manager, package_name):
    loaded_data = load_data()
    data = next((item for item in loaded_data
                if item["PackageManager"] == package_manager
                and item["PackageName"] == package_name), None)

    return data


def handle_new_data(package_info):
    loaded_data = load_data()
    if duplicate_exists(package_info, loaded_data):
        return ({'message': 'Package already exists'}), 409

    loaded_data.append(package_info.__dict__)
    save_data(loaded_data)

    return ({'message': 'Data created successfully'}), 201


def find_next_versions(data, package_version):
    versions = data["PackageVersion"]
    current_version_idx = versions.index(package_version)

    if len(versions) > (current_version_idx + 1):
        return (versions[current_version_idx + 1:]), 200
    return ({'message': 'Next versions not found'}), 404
