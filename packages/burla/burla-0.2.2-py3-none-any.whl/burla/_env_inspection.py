import subprocess
import warnings
import json

from burla._helpers import nopath_warning

warnings.formatwarning = nopath_warning

# cannot be pip installed without additional custom setup
BANNED_PACKAGES = ["GDAL", "python-apt", "PyGObject", "rpy2", "dlib", "dbus-python", "pycocotools"]
SWAPPED_PACKAGES = {"psycopg2": "psycopg2-binary"}


class EnvironmentInspectionError(Exception):
    def __init__(self, stdout):
        super().__init__(
            (
                "The following error occurred attempting to get list if packages to install in "
                f"remove execution environment's: {stdout}"
            )
        )


def get_pip_packages():
    result = subprocess.run(
        ["pip", "list", "--format=json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if result.returncode != 0:
        raise EnvironmentInspectionError(result.stderr)

    for pkg in json.loads(result.stdout):
        if pkg["name"] in SWAPPED_PACKAGES.keys():
            pkg["name"] = SWAPPED_PACKAGES[pkg["name"]]

        if pkg["name"] in BANNED_PACKAGES:
            warnings.warn(
                (
                    f"Burla is incompatiable with currently installed pkg: {pkg['name']}, "
                    "if you require this package please email jake@burla.dev!"
                )
            )
            continue

        if "+" in pkg["version"]:
            pkg["version"] = pkg["version"].split("+")[0]

        if not pkg.get("editable_project_location"):
            yield pkg
