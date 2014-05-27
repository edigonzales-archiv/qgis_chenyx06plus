from chenyx06plus import Chenyx06plus

def name():
    return "Chenyx06+"

def description():
    return "Plugin zum Verdichten der Dreiecksvermaschung."

def version():
    return "0.0.1"

def qgisMinimumVersion():
    return "1.7"

def authorName():
    return "Stefan Ziegler"

def classFactory(iface):
    return Chenyx06plus( iface, version() )
