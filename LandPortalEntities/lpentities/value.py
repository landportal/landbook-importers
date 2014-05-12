"""
Created on 02/02/2014

@author: Miguel Otero
"""


class Value(object):
    """
    classdocs
    """

    MISSING = "obsStatus-M"
    AVAILABLE = "obsStatus-A"
    FLOAT = "float"
    INTEGER = "int"


    def __init__(self, value=None, value_type=None, obs_status=None):
        """
        Constructor
        """
        self.value = value
        self.value_type = value_type
        self.obs_status = obs_status