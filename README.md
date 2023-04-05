# User Updater
This script allows to update Firstname/Lastname attribute of a specific user inside Prisma Cloud

## Setup dependencies
```bash
pip3 install -r requirements.txt
```

## Run Script
Important: please add PC_USER & PC_PASS environment variables (Example in .env.template)

```bash
python3 main.py --stack "api2.eu" --user-email "njannasch@<domain>.com" --gid "NewLastname"
```
