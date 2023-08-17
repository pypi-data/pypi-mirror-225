#  Copyright 2023 Nyria
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.

import os

from pathlib import Path
from setuptools import setup, find_packages

# Gets the root path of the project
ROOT = Path(__file__).parent.absolute()

NAME = "nyria-ory"
VERSION = os.environ["CI_COMMIT_TAG"]
DESCRIPTION = "Service Management System"
LONG_DESCRIPTION = "Service Management System"
AUTHOR = "Nyria"
URL = "https://gitlab.nyria.net/nyria/libaries/ory"
LICENSE = "GPL-3.0"
PYTHON = "<=3.10"

# Get the requirements from the requirements.txt file
with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

# Run the setup
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    url=URL,
    license=LICENSE,
    python_requires=PYTHON,
    packages=find_packages(),
    install_requires=install_requires,
    long_description_content_type="text/markdown"
)
