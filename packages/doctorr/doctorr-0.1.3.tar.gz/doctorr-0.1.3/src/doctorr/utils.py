def _get(key, obj, default=None):
    # bad design:
    # config["include"] in autodoc
    # config.include in autocli
    # (same for "watch")
    # this works around this bad design
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)
