def setupgdal():
    GDAL_PATH = "C:\\Program Files (x86)\\GDAL"
    if not os.path.isdir(GDAL_PATH):
        print("GDAL not found on system at {0}".format(GDAL_PATH))
        return False
    _environ = dict(os.environ)
    _environ["PATH"] = "{0};{1}".format(GDAL_PATH, _environ["PATH"])
    _environ["GDAL_DATA"] = "{0}\\gdal-data".format(GDAL_PATH)
    _environ["GDAL_PLUGINS"] = "{0}\\gdalplugins".format(GDAL_PATH)
    os.environ.clear()
    os.environ.update(_environ)
    try:
        import gdal
    except ImportError:
        print("GDAL Import Failed")

