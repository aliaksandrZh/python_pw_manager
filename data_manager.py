from validations import is_required_field_valid, is_username_password_valid
import json


class SaveToJsonException(Exception):
    """Raised when saving to the json file is failed"""

    def __init__(self, file_name):
        self.file_name = file_name
        self.message = f"Wasn't able to save a json to the file {file_name}"
        super().__init__(self.message)


def search_username_password(website_name):
    website = website_name.lower()

    if not is_required_field_valid(website):
        return

    try:
        with open("data.json", "r") as data_file:
            json_data = json.load(data_file)
            website_data = json_data.get(website)
        if website_data is None:
            return
    except Exception:
        return
    else:
        username = website_data.get("username")
        password = website_data.get("password")

        if is_required_field_valid(username) and is_required_field_valid(password):
            return website_data


def save_username_password(username_password):
    website = list(username_password.keys())[0]

    if (not is_required_field_valid(website)
            or not is_username_password_valid(username_password.get(website))):
        return

    website = website.lower()

    pw_data = {
        website: username_password
    }

    try:
        with open("data.json", "r") as data_file:
            json_data = json.load(data_file)
    except FileNotFoundError:
        with open("data.json", "w") as data_file:
            json.dump(pw_data, data_file, indent=2)
    except json.decoder.JSONDecodeError:
        with open("data.json", "w") as data_file:
            json.dump(pw_data, data_file, indent=2)
    except Exception:
        pw_data = None
        raise SaveToJsonException(data_file.name)
    else:
        json_data.update(pw_data)

        with open("data.json", "w") as data_file:
            json.dump(json_data, data_file, indent=2)

    finally:
        return pw_data
