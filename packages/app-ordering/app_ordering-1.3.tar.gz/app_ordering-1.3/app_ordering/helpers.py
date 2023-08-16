from os import path
from importlib.util import find_spec


def get_package_template_dir(module_name: str) -> str:
    spec = find_spec(module_name)

    if not spec or len(spec.submodule_search_locations) == 0:
        return ""
    module_dir = spec.submodule_search_locations[0]
    return path.join(module_dir, "templates")
