import asyncio
import os
import socket
import requests
import urllib3
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyromod.exceptions import ListenerTimeout
from config import OWNERS
from AnieXEricaMusic import app
from AnieXEricaMusic.misc import SUDOERS
from AnieXEricaMusic.utils.database import save_app_info
from AnieXEricaMusic.utils.pastebin import AMBOTBin
import config
from strings import get_string, helpers


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEROKU_API_URL = "https://api.heroku.com"
HEROKU_API_KEY = config.HEROKU_API_KEY
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
REPO_URL = "https://github.com/AbhiModszYT/AnieXEricaMusic"  
BUILDPACK_URL = "https://github.com/heroku/heroku-buildpack-python"
UPSTREAM_REPO = "https://github.com/AbhiModszYT/AnieXEricaMusic"  
UPSTREAM_BRANCH = "main"  

async def is_heroku():
    return "heroku" in socket.getfqdn()


async def paste_neko(code: str):
    return await AMBOTBin(code)


def fetch_app_json(repo_url):
    app_json_url = f"{repo_url}/raw/master/app.json"
    response = requests.get(app_json_url)
    return response.json() if response.status_code == 200 else None


def make_heroku_request(endpoint, api_key, method="get", payload=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.heroku+json; version=3",
        "Content-Type": "application/json",
    }
    url = f"{HEROKU_API_URL}/{endpoint}"
    response = getattr(requests, method)(url, headers=headers, json=payload)
    if method == "get":
        return response.status_code, response.json()
    else:
        return response.status_code, (
            response.json() if response.status_code == 200 else response.text
        )


def make_heroku_request(endpoint, api_key, method="get", payload=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.heroku+json; version=3",
        "Content-Type": "application/json",
    }
    url = f"{HEROKU_API_URL}/{endpoint}"
    response = getattr(requests, method)(url, headers=headers, json=payload)
    return response.status_code, (
        response.json() if response.status_code == 200 else None
    )


def make_heroku_requesta(endpoint, api_key, method="get", payload=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.heroku+json; version=3",
        "Content-Type": "application/json",
    }
    url = f"{HEROKU_API_URL}/{endpoint}"
    response = getattr(requests, method)(url, headers=headers, json=payload)

    if method == "get":
        return response.status_code, response.json()
    else:
        return response.status_code, (
            response.json() if response.status_code == 200 else response.text
        )


def make_heroku_requestb(endpoint, api_key, method="get", payload=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.heroku+json; version=3",
        "Content-Type": "application/json",
    }
    url = f"{HEROKU_API_URL}/{endpoint}"
    response = getattr(requests, method)(url, headers=headers, json=payload)
    return response.status_code, response.json() if method != "get" else response


def make_heroku_requestc(endpoint, api_key, method="get", payload=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.heroku+json; version=3",
        "Content-Type": "application/json",
    }
    url = f"{HEROKU_API_URL}/{endpoint}"
    response = getattr(requests, method)(url, headers=headers, json=payload)
    return response.status_code, (
        response.json() if response.status_code == 200 else None
    )


async def fetch_apps():
    status, apps = make_heroku_requestc("apps", HEROKU_API_KEY)
    return apps if status == 200 else None


async def get_owner_id(app_name):
    status, config_vars = make_heroku_request(
        f"apps/{app_name}/config-vars", HEROKU_API_KEY
    )
    if status == 200 and config_vars:
        return config_vars.get("OWNER_ID")
    return None


async def collect_env_variables(message, env_vars):
    user_inputs = {}
    await message.reply_text(
        "Provide the values for the required environment variables. Type /cancel at any time to cancel the deployment."
    )

    for var_name, var_info in env_vars.items():
        if var_name in [
            "HEROKU_APP_NAME",
            "HEROKU_API_KEY",
            "UPSTREAM_REPO",
            "UPSTREAM_BRANCH",
            "API_ID",
            "API_HASH",
        ]:
            continue  
        description = var_info.get("description", "No description provided.")

        try:
            response = await app.ask(
                message.chat.id,
                f"Provide a value for {var_name}\n\nAbout: {description}\n\nType /cancel to stop hosting.",
                timeout=300,
            )
            if response.text == "/cancel":
                await message.reply_text("Deployment canceled.")
                return None
            user_inputs[var_name] = response.text
        except ListenerTimeout:
            await message.reply_text(
                "Timeout! You must provide the variables within 5 Minutes. Restart the process to deploy."
            )
            return None

    user_inputs["HEROKU_APP_NAME"] = app_name
    user_inputs["HEROKU_API_KEY"] = HEROKU_API_KEY
    user_inputs["UPSTREAM_REPO"] = UPSTREAM_REPO
    user_inputs["UPSTREAM_BRANCH"] = UPSTREAM_BRANCH
    user_inputs["API_ID"] = API_ID
    user_inputs["API_HASH"] = API_HASH

    return user_inputs

    if status == 200:
        await callback_query.message.edit_text(
            f"Dynos for app `{app_name}` turned on successfully.",
            reply_markup=reply_markup,
        )
    else:
        await callback_query.message.edit_text(
            f"Failed to turn on dynos: {result}", reply_markup=reply_markup
        )


async def check_app_name_availability(app_name):
    status, result = make_heroku_request(
        "apps",
        HEROKU_API_KEY,
        method="post",
        payload={"name": app_name, "region": "us", "stack": "container"},
    )
    if status == 201:
        delete_status, delete_result = make_heroku_request(
            f"apps/{app_name}",
            HEROKU_API_KEY,
            method="delete",
        )
        if delete_status == 200:
            return True  
    else:
        return False  


@app.on_message(
    filters.command(["heroku", "hosts", "hosted", "mybots", "myhost"]) & filters.user(OWNERS)
)
async def get_deployed_apps(client, message):
    apps = await fetch_apps()

    if not apps:
        await message.reply_text("No apps found on Heroku.")
        return

    buttons = [
        [InlineKeyboardButton(app["name"], callback_data=f"app:{app['name']}")]
        for app in apps
    ]

    buttons.append([InlineKeyboardButton("Back", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_text("Select an app:", reply_markup=reply_markup)

@app.on_message(filters.command("deletehost") & filters.private & filters.user(OWNERS))
async def delete_deployed_app(client, message):
    user_apps = await fetch_apps()
    if not user_apps:
        await message.reply_text("You have no deployed bots")
        return
    buttons = [
        [InlineKeyboardButton(app_name, callback_data=f"delete_app:{app_name}")]
        for app_name in user_apps
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        "Please select the app you want to delete:", reply_markup=reply_markup
    )
