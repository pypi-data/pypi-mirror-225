# pyutil_cfg

python utils for cfg

This package helps parse json-like configurations in .ini.


# Usage

    import pyutil_cfg as cfg

    logger, config = cfg.init(name, ini_filename)


# Example

Assume that you have the following `development.ini`:

    [demo:main]
    VAR_INT = 1
    VAR_BOOL = true
    VAR_DICT = {"A": 1, "B": "a"}
    VAR_LIST = [
        {"A": 2, "B": "b"},
        {"A": 3, "B": "c"},
        {"A": 4, "B": "d"}]
    VAR_SET_set = ["a", "b", "c", "a"]

Then with the following code:

    import pyutil_cfg as cfg

    logger, config = cfg.init('demo', 'development.ini')

`logger` is a [logger](https://docs.python.org/3/library/logging.html) with `name = 'demo'`

`config` ia as follow:

    config = {
        "VAR_INT": 1,
        "VAR_BOOL": true,
        "VAR_DICT": {"A": 1, "B": "a"},
        "VAR_LIST": [
            {"A": 2, "B": "b"},
            {"A": 3, "B": "c"},
            {"A": 4, "B": "d"}
        ],
        "VAR_SET_set": set(["a", "b", "c"])
    }

# Advanced Usage

## Separated Log ini filename

    import pyutil_cfg as cfg

    logger, config = cfg.init(name, ini_filename, log_ini_filename=log_ini_filename)

## Additional customized config parameters (specified as dict)

    import pyutil_cfg as cfg

    params = {}

    logger, config = cfg.init(name, ini_filename, params=params)
