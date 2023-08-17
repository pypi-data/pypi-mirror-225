# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

"""
Module to host some utility functions, which are exposed at the top-level.
"""
import sys
from pathlib import Path
from types import ModuleType

import tomli
from importlib_metadata import packages_distributions

__all__ = ["print_package_versions"]


def print_package_versions() -> None:
    """
    Print a Markdown-formatted table showing the Python version being used,
    as well as the versions of some loaded packages that are relevant to the Fire Opal
    client package.
    """

    # packages_distributions returns a map between the top-level module names and package names.
    # However, it doesn't understand packages installed in editable mode,
    # which are handled in _get_package_name.
    _package_names_mapping = packages_distributions()

    def _get_package_name(module: ModuleType) -> str:
        if module.__name__ in _package_names_mapping:
            return _package_names_mapping[module.__name__][0]

        # The package is in editable mode: look in pyproject.toml to get the package name.
        with open(
            Path.joinpath(Path(module.__path__[0]).parent, "pyproject.toml"), "rb"
        ) as file:
            config = tomli.load(file)
            return config["tool"]["poetry"]["name"]

    top_level_module_names = [
        # External packages.
        "matplotlib",
        "networkx",
        "numpy",
        "qiskit",
        "qiskit-ibm-provider",
        "sympy",
        # Q-CTRL packages.
        "fireopal",
        "qctrlvisualizer",
    ]

    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

    # List containing the items in the different rows.
    table_items = [
        (
            _get_package_name(sys.modules[module_name]),
            sys.modules[module_name].__version__,
        )
        for module_name in top_level_module_names
        if module_name in sys.modules
    ]

    # Widths of the table columns.
    package_width = max(max(len(item[0]) for item in table_items), 7)
    version_width = max(max(len(item[1]) for item in table_items), 7)

    # Add headers and Python version at top of table.
    table_items = [
        ("Package", "Version"),
        ("-" * package_width, "-" * version_width),
        ("Python", python_version),
    ] + table_items

    # Print table.
    for name, version_ in table_items:
        print(f"| {name:{package_width}s} | {version_:{version_width}s} |")
