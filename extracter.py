"""Extract nested values from a JSON tree."""
# Code taken from From: https://hackersandslackers.com/extract-data-from-complex-json-python/ on 22/03/2021.
def json_extract(obj, search):
    """Recursively fetch values from nested JSON."""
    arr = []
    def extract(obj, arr, search):

        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, search)
                elif k == search:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, search)
        return arr

    values = extract(obj, arr, search)
    return values
