import phonenumbers


def prefix(phone_number):
    try:
        parsed_number = phonenumbers.parse(f'+{phone_number}', None)
        if phonenumbers.is_valid_number(parsed_number):
            prefix = str(parsed_number.country_code)
            number = str(parsed_number.national_number)
            return prefix, number
        else:
            return None, None
    except phonenumbers.phonenumberutil.NumberParseException:
        return None, None


def code(phone_number):
    try:
        parsed_number = phonenumbers.parse(f'+{phone_number}', None)
        country_code = phonenumbers.region_code_for_number(parsed_number)
        number = str(parsed_number.national_number)
        return country_code, number
    except phonenumbers.phonenumberutil.NumberParseException:
        return None, None
