#!/bin/bash
cd /opt/pemilu-ppwp-2024/src;
python3 main.py --save-json-files=$SAVE_JSON_FILES --save-image-files=$SAVE_IMAGE_FILES --db=$DB --debug=$DEBUG --db-filename=$DB_FILENAME;
