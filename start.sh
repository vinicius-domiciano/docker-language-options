#!/bin/bash

### Insert new language
# python3 -m sources.main --option=new:language --language=node

### Insert new version with JSON_PATH
python3 -m sources.main --option=new:version --type=JSON_PATH \
    --file_path=./sources/insert_new_dockerfile_version.json
    # --file_path=./sources/insert_new_image_version.json

### Remove Language:
# python3 -m sources.main --option=rm:language --language=java

### Remove version
# python3 -m sources.main --option=rm:version --language=java --version=java11

### Change version 
# python3 -m sources.main --option=ch:version --language=java --version=java11

### Configure Project, create file aliases.sh and add to .bashrc
# python3 -m sources.main --option=conf:prepare

reload_aliases