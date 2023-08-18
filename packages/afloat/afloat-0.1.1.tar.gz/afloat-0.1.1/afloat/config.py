import os

# Windows (should be os naive now)
try:
    HOME = os.environ['USERPROFILE']
except:
    HOME = os.path.expanduser('~')
    # HOME = os.environ['HOME']

def parse_config_file(home_dir=None):
    """
    Parses the .afloatconfig file into a dictionary.
    """
    if home_dir is None:
        home_dir = HOME
        
    afloatconfig_file = os.path.join(HOME, '.afloatconfig')
    
    if os.path.exists(afloatconfig_file):
        # raise(Exception("{} does not exist".format(afloatconfig_file)))
    
        with open(afloatconfig_file) as f:
            lines = f.readlines()

        config_dict = {}
        for line in lines:
            line = line.split(': ')
            config_dict[line[0].strip()] = line[1].strip()
    
    else:
        config_dict = {}
        print('No .afloatconfig config file found!')

    return config_dict

def get(key, home_dir=None):
    """
    Returns a key from the .afloatconfig file.

    Example:

        import afloat.config as config

        extras_folder = config.get('afloat-extras', home_dir=None)

    """
    
    config_dict = parse_config_file(home_dir=home_dir)
    
    if key in config_dict: 
        return config_dict[key]
    else: 
        return None
