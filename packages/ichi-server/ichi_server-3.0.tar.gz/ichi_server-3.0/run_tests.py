# ichi Server: An ichi server written in Python
# Copyright (C) 2022-present aveeryy

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import random
import shutil
import string

import pytest

ENVIRONMENT = f"""
authjwt_secret_key={''.join(random.choices(string.ascii_letters))}
database_path=sqlite:///test_data.db
enable_debug_capabilities=true
enable_registration=true
password_minimum_length=8
password_maximum_length=128
password_minimum_letters=1
password_minimum_numbers=1
password_minimum_symbols=1
profile_picture_storage_path=test_profiles
"""


def main():
    os.environ["ICHI_TEST_ENVIRONMENT"] = "1"
    os.environ["ICHI_ADMINISTRATION_PASSWORD"] = "MACARRONESCONTOMATICO"
    with open("test.env", "w") as fp:
        fp.write(ENVIRONMENT)
    pytest.main(args=["--verbose"])
    os.remove("test.env")
    os.remove("test_data.db")
    shutil.rmtree("test_profiles")


if __name__ == "__main__":
    main()
