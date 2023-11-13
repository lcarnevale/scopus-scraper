import logging

class ScopusLoad:
    
    __instance = None

    def __new__(self) -> __instance:
        """Implement Singleton class.
				
        Returns
		    (ScopusLoad) singleton instance of the class.
        """
        if self.__instance is None:
            print('creating the %s object ...' % (self.__name__))
            self.__instance = super(ScopusLoad, self).__new__(self)
        return self.__instance
    

    def build(self) -> __instance:
        """
        Returns:
            (ScopusLoad) the implemented class
        """
        return self.__instance
    

    def load(self):
        print("load it!")