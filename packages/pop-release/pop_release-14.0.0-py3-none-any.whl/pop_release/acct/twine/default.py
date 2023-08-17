import os

from twine.utils import get_config


def gather(hub, profiles):
    new_profiles = {}

    if not profiles.get("twine", {}):
        pypirc = os.path.expanduser("~/.pypirc")
        if os.path.exists(pypirc):
            twine_profiles = get_config(pypirc)
            new_profiles.update(twine_profiles)

    return new_profiles
