class Missing_PathConfig(Exception):
    """Generate dataset function was not provided with dictionary containing the data settings
    or path to the json file. The function call should contain either the python dicitonary containing
    all the settings or a path to the json file that could be transformed into python dictionary."""


class Invalid_SplitType(Exception):
    """Invalid split-type."""