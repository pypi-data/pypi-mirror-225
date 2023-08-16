<img src="https://codeberg.org/ichi/server/raw/branch/master/ichi_server/resources/static/logo.svg" width=150px>

## **ichi Server**

### Free and open source multiplayer card game

#### [Client](https://codeberg.org/ichi/client) | Server


## Features

* Account system:
    * Account recovery
    * Profile pictures
    * Per game mode statistics
* Administration tools:
    * Ban and mute players from the server
    * Report chat messages
* Basic chat system:
    * Send messages
    * Reply to other message
* Extensible: Create new game modes from scratch or expand existing ones

## Game modes

ichi Server currently has two game modes

|Name|Description|Player count|
|:-:|:-:|:-:|
<img src="https://codeberg.org/ichi/server/raw/branch/master/ichi_server/resources/game_mode_images/ichi.webp" width=30px><br>**ichi** | An UNO card game clone | 2-10 players
<img src="https://codeberg.org/ichi/server/raw/branch/master/ichi_server/resources/game_mode_images/ichi07.webp" width=30px><br>**ichi-0-7** | An alternative version of `ichi` where discarding a 0 card will swap everyone's cards and discarding a 7 card will let you swap cards with another player | 2-10 players

## Basic setup

> This section is very rough, Docker images and more proper documentation will be done in September

### Requirements
* [Python 3.10 or higher](https://www.python.org/downloads/)
* Git (optional)

### Installing from repository
1. Download (or clone) the repository
    * For the [latest release](https://codeberg.org/ichi/server/releases/latest) download the respective .zip or .tar.gz file
    * For the latest commit you can either:
        * Download the repo in [.zip](https://codeberg.org/ichi/server/archive/master.zip) or [.tar.gz](https://codeberg.org/ichi/server/archive/master.zip) format
        * Or using git to clone the repo: `git clone https://codeberg.org/ichi/server.git`
2. Open a terminal window on the downloaded (or cloned) repo
3. Create a virtual environment `python -m venv .venv`
4. Switch to the virtual environment: `source .venv/bin/activate` on Linux or `.venv/Scripts/Activate.ps1` on Windows (check [the Python documentantion](https://docs.python.org/3/library/venv.html#how-venvs-work) for more info)
5. Install requirements and ichi\_server using `pip install .`

### Installing from PyPi
1. Create a virtual environment `python -m venv .venv`
2. Switch to the virtual environment: `source .venv/bin/activate` on Linux or `.venv/Scripts/Activate.ps1` on Windows (check [the Python documentantion](https://docs.python.org/3/library/venv.html#how-venvs-work) for more info)

### Executing the server

Execute the server using `python -m ichi_server`, you will be asked to enter a password for the administrator account

## License

ichi Server is licensed under the GNU AGPL version 3

![GNU AGPL version 3 logo](resources/agpl-v3.svg)

For the full license text check the [LICENSE file](LICENSE)

### Libraries and other licenses

* FastAPI under the [MIT License](https://github.com/tiangolo/fastapi/blob/master/LICENSE)\: Copyright (c) 2018 Sebastián Ramírez
* hypercorn under the [MIT License](https://gitlab.com/pgjones/hypercorn/-/blob/main/LICENSE)\: Copyright (c) 2018 P G Jones
* python-multipart under the [Apache-2.0 License](https://github.com/andrew-d/python-multipart/blob/master/LICENSE.txt)\: Copyright (c) 2012 Andrew Dunham
* sqlmodel under the [MIT License](https://github.com/tiangolo/sqlmodel/blob/main/LICENSE)\: Copyright (c) 2021 Sebastián Ramírez
* SQLAlchemy under the [MIT License](https://github.com/sqlalchemy/sqlalchemy/blob/main/LICENSE)\: Copyright (c) 2005-2023 SQLAlchemy authors and contributors
* pydantic under the [MIT License](https://github.com/pydantic/pydantic/blob/main/LICENSE)\: Copyright (c) 2017 to present Pydantic Services Inc. and individual contributors
* passlib under the [BSD License](https://foss.heptapod.net/python-libs/passlib/-/blob/branch/stable/LICENSE)\: Copyright (c) 2008-2020 Assurance Technologies, LCC
* aiofiles under the [Apache-2.0 License](https://github.com/Tinche/aiofiles/blob/main/LICENSE)
* colorama under the [BSD 3-Clause License](https://github.com/tartley/colorama/blob/master/LICENSE.txt)\: Copyright (c) 2010 Jonathan Hartley
* Pillow under the [HPND License](https://github.com/python-pillow/Pillow/blob/main/LICENSE)\:
    * Copyright (c) 1997-2011 by Secret Labs AB
    * Copyright (c) 1995-2011 by Fredrik Lundh
    * Copyright (c) 2010-2023 by Jeffrey A. Clark (Alex) and contributors
* ichi-auth under the [MIT License](https://codeberg.org/ichi/auth/src/branch/master/LICENSE)\:
    * Copyright (c) 2020 Nyoman Pradipta Dewantara
    * Copyright (c) 2022-present aveeryy
* alembic under the [MIT License](https://github.com/sqlalchemy/alembic/blob/main/LICENSE)\: Copyright (c) 2009-2023 Michael Bayer
* python-dotenv under the [BSD 3-Clause License](https://github.com/theskumar/python-dotenv/blob/main/LICENSE)\: Copyright (c) 2014, Saurabh Kumar (python-dotenv), 2013, Ted Tieken (django-dotenv-rw), 2013, Jacob Kaplan-Moss (django-dotenv)
* The [ichi Cards (alt) logo](ichi_server/resources/static/logo.svg) is licensed under the [CC BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)
