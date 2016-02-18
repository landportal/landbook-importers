__author__ = 'Miguel Otero'


class UnknownCountryError(RuntimeError):

    def __init__(self, msg):
      # Call the base class constructor with the parameters it needs
      super(UnknownCountryError, self).__init__(msg)
