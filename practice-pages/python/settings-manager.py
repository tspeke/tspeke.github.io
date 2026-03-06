# Expects T_key_value to be a tuple containing two strings
def add_setting(D_settings, T_key_value):

    new_key, new_value = lowercase_T(T_key_value)

    if key_in_D(D_settings, new_key):
        return "Setting '" + new_key + "' already exists! Cannot add a new setting with this name."
    else:
        # Updating dictionary with new key-value pair
        D_settings[new_key] = new_value

        return "Setting '" + new_key + "' added with value '" + new_value + "' successfully!"

def update_setting(D_settings, T_key_value):

    update_key, update_value = lowercase_T(T_key_value)

    if key_in_D(D_settings, update_key):
        # Updating existing dictionary key-value
        D_settings[update_key] = update_value
        return "Setting '" + update_key + "' updated to '" + update_value + "' successfully!"
    else:
        return "Setting '" + update_key + "' does not exist! Cannot update a non-existing setting."

def delete_setting(D_settings, del_key):

    del_key = del_key.lower()

    if key_in_D(D_settings, del_key):
        # Deleting dictionary key-value pair
        del D_settings[del_key]
        return "Setting '" + del_key + "' deleted successfully!"
    else:
        return "Setting not found!"

def view_settings(D_settings):
    if D_settings == {}:
        return "No settings available."
    
    # Using "f strings" to insert variable values frequently within string
    full_formatted_str = "Current User Settings:\n"
    for key in D_settings:
        # Capitalising first letter in key str
        cap_key = key[0].upper() + key[1:]

        full_formatted_str = full_formatted_str + f"{cap_key}: {D_settings[key]}\n"
    
    return full_formatted_str

# Takes a Tuple of two strings and returns a Tuple of the two strings made lowercase
def lowercase_T(T_str):
    str1, str2 = T_str
    str1 = str1.lower()
    str2 = str2.lower()

    return (str1, str2)

def key_in_D(D, ref_key):
    
    for key in D:
        if ref_key == key:
            return True
    
    return False

test_settings = {
    "setting1" : "on",
    "setting2" : "off",
    "setting3" : "on",
}

print(add_setting(test_settings, ("Setting1", "on")))

print(view_settings(test_settings))