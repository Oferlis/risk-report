import json

db = "./data.json"


def duplicate_exists(new_data, loaded_data):
    for item in loaded_data:
        if item["PackageManager"] == new_data["PackageManager"]\
                and item["PackageName"] == new_data["PackageName"]:
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
