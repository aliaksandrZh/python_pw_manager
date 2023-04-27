def is_required_field_valid(field_value):
    return field_value is not None and len(field_value) > 0


def is_username_password_valid(name_password):
    return (name_password is not None
            and is_required_field_valid(name_password.get("username"))
            and is_required_field_valid(name_password.get("password")))
