from fedata.hub.fetch_data import load_data
from fedata.utils.load_from_json import load_from_json
from fedata.exceptions.generateexceptions import Missing_PathConfig

def generate_dataset(path: str = None, 
                     config:  dict = None,
                     **kwargs):
    """Generates the data as given in the provided config. Requires
    either config in form of python dictionary or a path to a json file
    that will be parsed as a config. If both are provided, json file
    will precede over python dictionary file.
    
    Parameters
    ----------
    path: str or Path like object
        Path to the json config containing all the settings required for
        generating data. Path to json config is required only is python dict.
        is not provided.
    config: dict
        Python dictionary containing all the settings required for generating 
        data. It is possible to provide a path directly to the json file containing
        the required metadata instead of passing the python dicitonary.
    """
    if not path and not config:
        raise Missing_PathConfig

    if path:
        configuration = load_from_json(path)
    else:
        configuration = config
    
    return load_data(settings=configuration)
