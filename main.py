import json
import os

import requests
import typer

if not os.getenv("PC_USER") or not os.getenv("PC_PASS"):
    raise ValueError("No PC_USER or PC_PASS configurated")

TOKEN = None

app = typer.Typer()


def get_token(stack):
    """Get temporary token from prisma cloud"""
    global TOKEN
    url = f"https://{stack}.prismacloud.io/login"
    payload = json.dumps(
        {"username": os.environ["PC_USER"], "password": os.environ["PC_PASS"]}
    )
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()
    TOKEN = response.json()["token"]


def get_user(stack: str, user_email: str):
    """Get details of specific user"""
    url = f"https://{stack}.prismacloud.io/v2/user/{user_email}"

    payload = {}
    headers = {"Accept": "application/json", "x-redlock-auth": TOKEN}
    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()


def update_user(stack: str, user_email: str, user_dict: dict):
    """ Update specific user """
    url = f"https://{stack}.prismacloud.io/v2/user/{user_email}"

    # Update values
    payload = json.dumps(user_dict)
    headers = {"Content-Type": "application/json", "x-redlock-auth": TOKEN}

    # Update via REST API
    response = requests.request("PUT", url, headers=headers, data=payload)
    response.raise_for_status()
    print("Changed successful")


def update_user_old(stack: str, user_email: str, user_dict: dict, GID: str):
    """ Update specific user """
    # This is an example of how an update could be done automatically
    url = f"https://{stack}.prismacloud.io/v2/user/{user_email}"

    # Update values
    user_dict["firstName"] = f"{user_dict['firstName'] }.{user_dict['lastName'] }"
    user_dict["lastName"] = GID
    payload = json.dumps(user_dict)
    headers = {"Content-Type": "application/json", "x-redlock-auth": TOKEN}

    # Update via REST API
    response = requests.request("PUT", url, headers=headers, data=payload)
    response.raise_for_status()
    print("Changed successful")


@app.command()
def download(
    user_email: str = typer.Option(..., help="User email to be updated"),
    stack: str = typer.Option(
        "api", help="Prisma Cloud stack to be used: `api.prismacloud.com`"
    ),
):
    """ Download prisma_user based on email """
    # Get temporary
    get_token(stack)

    # Get the current data of the user
    user = get_user(stack, user_email)
    print(user)

    # user['ccgid'] = "123123"

    with open("prisma_user.json", "w") as f_obj:
        json.dump(user, f_obj)

    # Update the user
    #update_user(stack, user_email, user, gid)

@app.command()
def update(
    user_email: str = typer.Option(..., help="User email to be updated"),
    stack: str = typer.Option(
        "api", help="Prisma Cloud stack to be used: `api.prismacloud.com`"
    ),
):
    """ Update the user based on prisma_user.json """
    # Get temporary
    get_token(stack)

    # Read change from file system
    user = None
    with open("prisma_user.json", "r") as f_obj:
        user = json.load(f_obj)

    update_user(stack, user_email, user)

if __name__ == "__main__":
    app()
