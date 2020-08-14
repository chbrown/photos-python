__version__ = None

try:
    import pkg_resources

    __version__ = pkg_resources.get_distribution("photos").version
except Exception:
    pass
