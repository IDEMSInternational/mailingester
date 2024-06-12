def version():
    try:
        from ._version import version
    except ModuleNotFoundError:
        version = "dev"

    return version
