import base64
import json
import os
import shutil
import tempfile
import time
import zipfile
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable

import click
import requests
from rich.console import Console
from rich.progress import Progress
from rich.tree import Tree

KORBIT_HOST = os.getenv("KORBIT_HOST", "https://mentor.korbit.ai:8000")
KORBIT_SCAN_REPORT_URL = f"{KORBIT_HOST}/database/v3/scans"
KORBIT_CODE_ANALYSIS_SERVICE = f"{KORBIT_HOST}/code-analysis/check"
KORBIT_CODE_ANALYSIS_CHECK = f"{KORBIT_CODE_ANALYSIS_SERVICE}/files"

KORBIT_CREDENTIAL_FILE = os.path.expanduser("~/.korbit/credentials")
KORBIT_LOCAL_FOLDER = ".korbit"

INTERFACE_WAITING_START_MSG = "Analysis requested is in the queue, it will start shortly..."
INTERFACE_WAITING_REPORT_MSG = "Analysis completed successfully! Report generation in progress..."

INTERFACE_SCAN_PATH_HELP = "Put the absolute or relative path of a local folder or file to scan."
INTERFACE_AUTH_MISSING_CREDENTIALS_MSG = "No user credentials found, please login first with `korbit login`!"
INTERFACE_AUTH_INPUT_SECRET_ID = "Please enter your secret ID: "
INTERFACE_AUTH_INPUT_SECRET_ID_HELP = "The secret_id value generated on Korbit app for you user."
INTERFACE_AUTH_INPUT_SECRET_KEY = "Please enter your secret key: "
INTERFACE_AUTH_INPUT_SECRET_KEY_HELP = "The secret_key key generated on Korbit app for you user."
INTERFACE_SLEEPING_REFRESH = 1
tick_rotation = False


class ProgressStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PROGRESS = "PROGRESS"


@click.group()
def cli():
    pass


@cli.command("login")
@click.option("--secret_id", default=None, help=INTERFACE_AUTH_INPUT_SECRET_ID_HELP)
@click.option("--secret_key", default=None, help=INTERFACE_AUTH_INPUT_SECRET_KEY_HELP)
@click.argument("client_secret_id", required=False, type=click.STRING)
@click.argument("client_secret_key", required=False, type=click.STRING)
def login(client_secret_id, client_secret_key, secret_id, secret_key):
    """
    Store user credentials for future usage of scan command.
    If you use environment variable you can ignore this command.
    """
    if not secret_id:
        if not client_secret_id:
            secret_id = input(INTERFACE_AUTH_INPUT_SECRET_ID)
        else:
            secret_id = client_secret_id
    if not secret_key:
        if not client_secret_key:
            secret_key = input(INTERFACE_AUTH_INPUT_SECRET_KEY)
        else:
            secret_key = client_secret_key
    os.makedirs(Path(KORBIT_CREDENTIAL_FILE).parent, exist_ok=True)
    with open(KORBIT_CREDENTIAL_FILE, "w+") as credential_file:
        json.dump({"secret_id": secret_id, "secret_key": secret_key}, credential_file)


@cli.command("scan")
@click.argument("path", type=click.Path(exists=True))
def scan(path):
    """
    Request a scan on a given path of a local file or folder.\n
    Example:\n\n
    `korbit scan /path/to/folder`\n
    `korbit scan path/to/folder`\n
    `korbit scan .`
    """
    os.makedirs(KORBIT_LOCAL_FOLDER, exist_ok=True)
    click.echo(f"Zipping: {path}")

    zip_file_path = zip_folder(path)
    click.echo(f"Zipping completed successfully {zip_file_path}")
    try:
        scan_id = upload_file(zip_file_path)
        click.echo(f"Starting analysis of {zip_file_path}")
        display_scan_status(scan_id)
        report_path = download_report(scan_id)
        click.echo(f"You can access the report at {report_path}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code in [401, 403]:
            click.echo(INTERFACE_AUTH_MISSING_CREDENTIALS_MSG)
            raise
        raise


def generate_zip_file_name(folder_path: str):
    if folder_path in [".", "./"]:
        return "current_dir.zip"
    elif folder_path in ["..", "../"]:
        return "parent_dir.zip"
    folder_path = folder_path.replace("../", "").replace("./", "").replace("/", "-")
    return folder_path + ".zip"


def zip_folder(folder_path: str):
    folder_path = folder_path[:-1] if folder_path.endswith("/") else folder_path
    zip_file_path = generate_zip_file_name(folder_path)
    top_folder_name = os.path.basename(folder_path).replace(".", "-")
    temp_folder_path = tempfile.mkdtemp()

    try:
        temp_top_folder_path = os.path.join(temp_folder_path, top_folder_name)
        if os.path.isfile(folder_path):
            fil_parent_temp_folder = f"{temp_top_folder_path}/temp"
            os.makedirs(fil_parent_temp_folder, exist_ok=True)
            shutil.copy(folder_path, fil_parent_temp_folder)
        else:
            shutil.copytree(folder_path, temp_top_folder_path)

        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            zipf.write(temp_top_folder_path, top_folder_name)
            for root, _, files in os.walk(temp_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_folder_path)
                    zipf.write(file_path, arcname)
    finally:
        shutil.rmtree(temp_folder_path)

    return zip_file_path


def compute_user_token():
    with open(KORBIT_CREDENTIAL_FILE, "r") as credential_file:
        credentials = json.loads(credential_file.read())
    secret_id = os.getenv("KORBIT_SECRET_ID", credentials.get("secret_id"))
    secret_key = os.getenv("KORBIT_SECRET_KEY", credentials.get("secret_key"))
    assert secret_id, INTERFACE_AUTH_MISSING_CREDENTIALS_MSG
    assert secret_key, INTERFACE_AUTH_MISSING_CREDENTIALS_MSG
    return base64.b64encode(f"{secret_id}:{secret_key}".encode()).decode()


def authenticate_request(method: Callable[[str], requests.Response], url: str, **kwargs) -> requests.Response:
    headers = kwargs.pop("headers", {})
    if not headers.get("Authorization"):
        headers["Authorization"] = f"Basic {compute_user_token()}"
    kwargs["headers"] = headers
    response = method(url, **kwargs)
    response.raise_for_status()
    return response


def upload_file(zip_file_path) -> str:
    with open(zip_file_path, "rb") as file:
        response = authenticate_request(requests.post, url=KORBIT_CODE_ANALYSIS_CHECK, files={"repository": file})
        if response.status_code == 200:
            return response.json()
        else:
            raise click.ClickException("File upload failed!")


def create_tree_node(name, status):
    if status == "PROGRESS":
        name_with_status = name + (" ⌛️" if tick_rotation else " ⏳")
    elif status == "FAILURE":
        name_with_status = name + " ❌"
    elif status == "SUCCESS":
        name_with_status = name + " ✅"
    else:
        name_with_status = name + " 👀"
    node = Tree(name_with_status)
    return node


def build_file_tree(file_list):
    file_tree = {}
    for file_info in file_list:
        file_name = file_info["name"]
        file_status = file_info.get("status", "Unknown")

        # Extract directory and filename from the file path
        directory, filename = os.path.split(file_name)

        # Traverse the file_tree to the appropriate directory node
        current_node = file_tree
        for folder in directory.split(os.sep):
            if folder not in current_node:
                current_node[folder] = {}
            current_node = current_node[folder]

        current_node[filename] = file_status

    return file_tree


def add_nodes_to_tree(tree_node, current_node):
    for name, value in current_node.items():
        if isinstance(value, dict):
            if name:
                node = tree_node.add(name)
            else:
                node = tree_node
            add_nodes_to_tree(node, value)
        else:
            tree_node.add(create_tree_node(name, value))


def display_scan_status(scan_id: str):
    console = Console()
    global tick_rotation
    while True:
        response = authenticate_request(requests.get, url=f"{KORBIT_CODE_ANALYSIS_SERVICE}/{scan_id}/progress")
        tick_rotation = not tick_rotation
        try:
            data = response.json()
            status = data.get("status")
            if not status:
                console.clear()
                console.print(INTERFACE_WAITING_START_MSG)
                time.sleep(INTERFACE_SLEEPING_REFRESH)
                continue
            if status == ProgressStatus.SUCCESS.value:
                console.clear()
                console.print(INTERFACE_WAITING_REPORT_MSG)
                break
            progress = data.get("progress", 0.0)
            total_progress = data.get("total_progress", 0.0)
            title = data.get("title", "File status")

            file_tree_data = data.get("files", [])
            file_tree = build_file_tree(file_tree_data)

            tree = Tree(title)
            add_nodes_to_tree(tree, file_tree)

            with Progress(console=console, auto_refresh=True) as progress_bar:
                task = progress_bar.add_task(f"Analyzing files ({len(file_tree_data)})...", total=100, spinner="⌛️")
                progress_bar.update(task, completed=progress)

            with Progress(console=console, auto_refresh=True) as progress_bar_total:
                task = progress_bar_total.add_task("Remaining analysis types...", total=100, spinner="⌛️")
                progress_bar_total.update(task, completed=total_progress)

            console.clear()
            console.print(tree)
            console.print(progress_bar)
            console.print(progress_bar_total)

        except Exception as e:
            console.print(f"Error processing response: {e}")
        time.sleep(INTERFACE_SLEEPING_REFRESH)


def issues_to_markdown(json_data) -> str:
    data = json.loads(json_data)
    issues_by_category = {}

    for item in data:
        issues = item["files"]
        for issue in issues:
            description = item["description"]
            category = issue["category"]
            full_file_path = issue["full_file_path"]
            line_start = issue["line_start"]
            priority = issue["priority"]
            confidence = issue["confidence"]

            if category not in issues_by_category:
                issues_by_category[category] = []

            issues_by_category[category].append(
                {
                    "description": description,
                    "full_file_path": full_file_path,
                    "line_start": line_start,
                    "priority": priority,
                    "confidence": confidence,
                }
            )
    output = []
    for category, issues in issues_by_category.items():
        output.append(f"## {category}")
        for i, issue in enumerate(issues, start=1):
            description = issue["description"]
            full_file_path = issue["full_file_path"]
            line_start = issue["line_start"]
            priority = issue["priority"]
            confidence = issue["confidence"]

            output.append(f"{i}. {description}")
            output.append(f"  - full_file_path:line_start: {full_file_path}:{line_start}")
            output.append(f"  - priority: {priority}")
            output.append(f"  - confidence: {confidence}")
            output.append("")
        output.append("")
        output.append("")
    return "\n".join(output)


def download_report(scan_id: str) -> str:
    response = authenticate_request(
        requests.get, url=f"{KORBIT_SCAN_REPORT_URL}/{scan_id}/issues?format=json&output_concept_embedding=false"
    )
    report_path = f"{KORBIT_LOCAL_FOLDER}/{scan_id}_{datetime.now().isoformat()}_report"
    os.makedirs(KORBIT_LOCAL_FOLDER, exist_ok=True)
    markdown_report_path = f"{report_path}.md"
    json_report_path = f"{report_path}.json"
    with open(json_report_path, "w+") as json_file, open(markdown_report_path, "w+") as md_file:
        issues = response.content.decode()
        json_file.write(issues)
        md_file.write(issues_to_markdown(issues))
    return markdown_report_path


if __name__ == "__main__":
    cli()
