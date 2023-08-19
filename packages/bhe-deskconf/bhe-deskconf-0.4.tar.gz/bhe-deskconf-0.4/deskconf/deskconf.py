from pathlib import Path
from deskconf.attrib import Attrib
from shutil import copy

def syntax(icofilename,
                   info="IdhinBhe OJO DI UTAK-ATIK SU......"):
    shellsyntax = f"""[.ShellClassInfo]
ConfirmFileOp=0
NoSharing=1
IconFile={icofilename}
IconIndex=0
InfoTip={info}"""
    return shellsyntax


def attrib_rmall(path):
    """ Removing all Attributes of desktop.ini in subfolder

    param:
    path(Path): Path Object
    """
    for dir in path.glob("*.ini"):
        Attrib(dir).unset_s()
        Attrib(dir).unset_h()
        Attrib(dir).unset_r()
        Attrib(dir).unset_all()


def renameall_ico(path):
    """ Renaming all ico file in subfolder to "icon.ico"
    
    param:
    path(Path): Path Object"""
    for folder in path.iterdir():
        for ico in folder.glob("*.ico"):
            try:
                ico.rename(folder / f"icon{ico.suffix}")
            except FileExistsError:
                pass


def rmall_conf(path):
    """ Removing all desktop.ini in all child path
    
    param:
    path(Path): Path Object
    """
    for folder in path.iterdir():
        for conf in folder.glob("*.ini"):
            print(conf)
            Attrib(conf).unset_r
            Attrib(conf).unset_s
            Attrib(conf).unset_sh()
            conf.unlink()


def set_all(path=Path(), info="IdhinBhe OJO DI UTAK-ATIK SU......"):
    """Setting up all desktop.ini, if in all subdir already have ico files
    
    1 - removing all config
    2 - renaming all ico files
    3 - creating desktop.ini
    
    param:
    path(Path): Path Object"""

    rmall_conf(path)
    renameall_ico(path)
    for folder in path.iterdir():
        for ico in folder.glob("*.ico"):
            desktop_conf = folder / "desktop.ini"
            desktop_conf.write_text(syntax(ico.name, info=info))
            Attrib(folder).set_s()
            Attrib(ico).set_h()
            Attrib(desktop_conf).set_sh()


ico = [ico for ico in Path().glob("*.ico")][0]
def one_for_all(ico=ico, path=Path(), info="IdhinBhe OJO DI UTAK-ATIK SU......"):
    """set all icon for all """
    folders = [folder for folder in path.iterdir() if folder.is_dir()]
    for folder in folders:
        copy(ico, f"{folder.name}\icon.ico")
    
    set_all(path, info=info)