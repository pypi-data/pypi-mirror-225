import json

def load_from_json(path: 'str', 
                   convert_keys: bool = False) -> dict:
        """Helper function for loading the json file and returning
        its content as a python dictionary. 
            
        Parameters
        ----------
        path: str or path-like
            A path to the json file.
        convert_keys: bool, default to False
            If set to true, all the dictionary keys for transformations and for imbalanced 
            clients will be transformed to ints.
        Returns
        -------
        dictionary
        """
        with open(path, 'r') as json_file:
            data = json.load(json_file)
        if convert_keys == True:
            if data.get('transformations'):
                data['transformations'] = {int(key): value for key, value in data['transformations'].items()}
            if data.get('imbalanced_clients'):
                data['imbalanced_clients'] = {int(key): value for key, value in data['imbalanced_clients'].items()}
        return data