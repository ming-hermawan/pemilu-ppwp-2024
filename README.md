# Retrieve 2024 Indonesian Presidential Election Data

## 1. Introduction
This project gathers data result of 2024 Indonesian Presidential Election from the official institution, and save it to a database (only support SQLite now) or files.

**DISCLAIMER:**
This project retrieves *PUBLIC* (no confidential) data which provided by general elections commission (KPU), that can be accessed publicly at https://pemilu2024.kpu.go.id for *educational purposes ONLY*.

## 2. How to Run:
### 2.1. Using Docker
#### Steps:
1. Pull docker image from the repository.  
`docker pull minghermawan/pemilu-ppwp-2024:pre-alpha`  
2. Create a new folder for SQLite database and files output.  
3. Run docker with command format like below.  
`docker run -v (Output Folder):/opt/pemilu-ppwp-2024/out --env DB=(NO/sqlite) --env DB_FILENAME=(SQLite database filename) --env DEBUG=(YES/NO) --env SAVE_JSON_FILES=(YES/NO) --env SAVE_IMAGE_FILES=(YES/NO)`  
NOTE; Check and update an existing docker-compose.yml if you want to run with docker compose.
#### Example:
`docker run -v /home/test/out:/opt/pemilu-ppwp-2024/out --env DB=sqlite --env DB_FILENAME=ppwp2024.db --env DEBUG=NO --env SAVE_JSON_FILES=NO --env SAVE_IMAGE_FILES=NO minghermawan/pemilu-ppwp-2024:pre-alpha`  
or  
`docker run -v $PWD/out:/opt/pemilu-ppwp-2024/out --env DB=sqlite --env DB_FILENAME=ppwp2024.db --env DEBUG=NO --env SAVE_JSON_FILES=NO --env SAVE_IMAGE_FILES=NO minghermawan/pemilu-ppwp-2024:pre-alpha`
#### Explanation:
`-v` is to map your output folder with output folder inside Docker.  
For example, if your new output folder path is <ins>/home/test/out</ins> at step 2, write `-v /home/test/out:/opt/pemilu-ppwp-2024/out`, when script is running, database or file output will save at <ins>/home/test/out</ins>.  
`--env` is environment variable.
#### Environment Variables:
- DB
Set value is <ins>NO</ins> if you don't want to write output to the database.  
Set value is <ins>sqlite</ins> if you want to write output to SQLite database. (Only support SQLite database right now)  
If you set the value is <ins>sqlite</ins>, database file will be saved in the <ins>db</ins> folder inside output folder.
- DB_FILENAME (optional, effect only when you set the DB value is sqlite)
Set SQLite database filename.
- DEBUG
When the value is <ins>YES</ins>, debug files will be created in the <ins>log</ins> folder inside output folder.
- SAVE_JSON_FILES
Set value is <ins>YES</ins> if you want to write output to JSON files.  
JSON files will be created in the <ins>json</ins> folder inside output folder.
- SAVE_IMAGE_FILES
Set value is <ins>YES</ins> if you want to save images files.  
Image files will be created in the <ins>image</ins> folder inside output folder.
### 2.2. Using Python
#### Requirements:
1. Python (this project tested with Python 3.11.11)
2. Python Library:
   - aiohttp
   - aiofiles
   - python-dotenv
#### Steps:
1. `git clone https://github.com/ming-hermawan/pemilu-ppwp-2024.git`
2. `cd pemilu-ppwp-2024`
3. Edit `.env`, update <ins>OUTPUT_FOLDER_PATH</ins> into your output folder. (SQLite database file and other files result will be saved in output folder)
4. `python main.py --save-json-files=(YES/NO) --save-image-files=(YES/NO) --db=(NO/sqlite) --debug=$DEBUG --db-filename=(SQLite database filename);`
#### Example:
`python main.py --save-json-files=NO --save-image-files=NO --db=sqlite --debug=NO --db-filename=ppwp2024.db;`
#### Parameters:
- `--save-json-files`
Set value is YES if you want to write output to JSON files.
JSON files will be created in the <ins>json</ins> folder inside output folder.
- `--save-image-files`
Set value is YES if you want to save images files.
Image files will be created in the <ins>image</ins> folder inside output folder.
- `--db`
Set value is <ins>NO</ins> if you don't want to write output to the database.
Set value is <ins>sqlite</ins> if you want to write output to SQLite database. (Only support SQLite database right now)
If you set the value is <ins>sqlite</ins>, database file will be saved in the <ins>db</ins> folder inside output folder.
- `--debug`
When the value is <ins>YES</ins>, debug files will be created in the <ins>log</ins> folder inside output folder.
- `--db-filename--`
Set SQLite database filename.
