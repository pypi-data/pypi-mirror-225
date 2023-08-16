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
import sys

from alembic import command
from alembic.config import Config as AlembicConfig
from hypercorn.run import run
from hypercorn.config import Config

from ichi_server.dependencies import _h, _w, settings, get_argument_value
from ichi_server.manager import create_database_and_tables
from ichi_server.version import __version__

try:
    import black

    black_available = True
except ImportError:
    black_available = False


def main():
    root_directory = os.path.dirname(__file__)
    alembic_config = AlembicConfig(f"{root_directory}/alembic.ini")
    alembic_config.set_main_option("script_location", f"{root_directory}/migrations")
    alembic_config.set_main_option("sqlalchemy.url", settings.database_path)
    if not black_available:
        # Avoid an exception if black formatter is not installed
        alembic_config.set_section_option("post_write_hooks", "hooks", "")
    config = Config()
    config.application_path = "ichi_server:app"
    config.bind = settings.hypercorn_bind_address
    config.use_reloader = "--reload" in sys.argv
    config.websocket_ping_interval = 1
    if "--generate-migration" in sys.argv:
        message = get_argument_value("--generate-migration")
        if message is None:
            raise Exception("Message can't be empty")
        print(f"{_h('alembic')} Generating a migration file")
        command.revision(alembic_config, message, True)
        print(
            f"{_h('alembic')} Completed, make sure check the migration file and upgrade the database before generating another migration"
        )
        sys.exit(0)

    print(
        f"{_h('ichi')} Starting ichi Server version {__version__} with PID {os.getpid()}"
    )
    if config.use_reloader:
        print(f"{_w('ichi/warning')} Using reloader, not suitable for production usage")
    create_database_and_tables()
    # Run database migrations
    print(f"{_h('alembic')} Starting database migration routine")
    command.upgrade(alembic_config, "head")
    # asyncio.run(serve(app, config))
    run(config)


if __name__ == "__main__":
    main()
