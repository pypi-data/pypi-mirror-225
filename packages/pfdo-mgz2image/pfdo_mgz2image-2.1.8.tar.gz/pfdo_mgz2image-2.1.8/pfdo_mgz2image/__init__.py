from importlib.metadata import Distribution

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


try:
    from .pfdo_mgz2image    import pfdo_mgz2image
except:
    from pfdo_mgz2image     import pfdo_mgz2image
