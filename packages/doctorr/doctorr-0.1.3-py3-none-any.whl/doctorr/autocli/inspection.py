import sys


def get_parser(config):
    if config.module_source in sys.modules:
        del sys.modules[config.module_source]
    module = __import__(config.module_source, fromlist=[config.getter])
    getter = getattr(module, config.getter)
    parser = getter()
    return parser
