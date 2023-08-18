from os import system

class Attrib:
    """Change File/Directory Atrributes in Windows"""
    def __init__(self, path):
        self.path = f'"{path}"'

    def set_r(self):
        """ set read only """
        system(f"attrib +r {self.path}")

    def set_s(self):
        """ set system file """
        system(f"attrib +s {self.path}")
    
    def set_h(self):
        """ set hidden """
        system(f"attrib +h {self.path}")

    def set_all(self):
        """ set read only, system and hidden """
        self.set_h()
        self.set_s()
        self.set_r()

    def set_sh(self):
        """ set system and hidden
        very usefull for setting up desktop.ini
        """
        system(f"attrib +s +h {self.path}")

    def unset_r(self):
        """ unset read only """
        system(f"attrib -r {self.path}")
    
    def unset_s(self):
        """ unset system file """
        system(f"attrib -s {self.path}")

    def unset_h(self):
        """ unset hidden """
        system(f"attrib -h {self.path}")
    
    def unset_all(self):
        """ unset all attributes """
        self.unset_s()
        self.unset_h()
        self.unset_r()

    def unset_sh(self):
        system(f"attrib -s -h {self.path}")


