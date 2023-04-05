# User Updater
This script allows to download user data, modify it locally and apply the changes back to Prisma Cloud.

## Setup dependencies
```bash
pip3 install -r requirements.txt
```

## Run Script
Important: please add PC_USER & PC_PASS environment variables (Example in .env.template)

Read from api to file system
```bash
python3 main.py download --stack "api2.eu" --user-email "njannasch@<domain>.com"
```

Update based on file system json
```bash
python3 main.py update --stack "api2.eu" --user-email "njannasch@<domain>.com"
```
