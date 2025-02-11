import os
from dotenv import load_dotenv

load_dotenv()

DOMAIN = 'https://sirekap-obj-data.kpu.go.id'

# Folder-Path
OUTPUT_FOLDER_PATH = os.getenv('OUTPUT_FOLDER_PATH')
DB_FOLDER_PATH = "{0}/{1}".format(
  OUTPUT_FOLDER_PATH,
  os.getenv('DB_FOLDER_PATH'))
DB_FILENAME = os.getenv('DB_FILENAME')
JSON_FOLDER_PATH = "{0}/{1}".format(
  OUTPUT_FOLDER_PATH,
  os.getenv('JSON_FOLDER_PATH'))
LOG_FOLDER_PATH = "{0}/{1}".format(
  OUTPUT_FOLDER_PATH,
  os.getenv('LOG_FOLDER_PATH'))
IMAGE_FOLDER_PATH = "{0}/{1}".format(
  OUTPUT_FOLDER_PATH,
  os.getenv('IMAGE_FOLDER_PATH'))

CMD_DB_SQLITE = 'sqlite'

MAX_DOWNLOAD_IMAGE_PER_PROCESS = 50
