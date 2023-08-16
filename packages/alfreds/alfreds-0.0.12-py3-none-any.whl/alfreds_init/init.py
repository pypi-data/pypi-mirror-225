import json
import os
import subprocess
import time
import webbrowser
from pathlib import Path

import requests as requests


def print_bold(text):
    print(f"\033[1m{text}\033[0m")


def sync_seed_data(csv_directory_path):
    response = requests.post("http://localhost:3737/seed?csv_files_dir=" + csv_directory_path)
    if response.status_code != 200:
        print_bold("Failed to sync seed data.")
        print_bold(response.text)
        return
    else:
        print("Seed data synced.")

def pull_image(image_name):
    try:
        print(f"Pulling {image_name}...")
        subprocess.check_call(["docker", "pull", image_name])
        return True
    except subprocess.CalledProcessError:
        return False


def stop_container(container_name):
    try:
        print(f"Stopping {container_name}...")
        subprocess.check_call(["docker", "stop", container_name], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        subprocess.check_call(["docker", "rm", container_name], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass


def run_container(image_name, container_name, port, agent_path=None, working_dir_path=None, seed_path=None):
    duck_db_env_variable = None
    seed_db_env_variable = None
    if image_name == "datafacade/alfred-backend":
        alfreds_dir = get_alfred_dir()
        duck_db_env_variable = f"DUCK_DB_PATH={alfreds_dir}/duck.db"
        seed_db_env_variable = f"SEED_DB_PATH={alfreds_dir}/seed.db"

    try:
        stop_container(container_name)
        if agent_path is not None and working_dir_path is not None:
            commands = ["docker",
                        "run",
                        "--name",
                        container_name,
                        "-v", f"{agent_path}:{agent_path}",
                        "-v", f"{working_dir_path}:{working_dir_path}",
                        "-v", f"{get_alfred_dir()}:{get_alfred_dir()}",
                        "-e", duck_db_env_variable,
                        "-e", seed_db_env_variable,
                        "-d",
                        "-p", f"127.0.0.1:{port}:{port}",
                        "-m", "150m",
                        "--cpus", "1"]
            if seed_path is not None:
                print("Mounting seed directory...")
                commands.append("-v")
                commands.append(f"{seed_path}:{seed_path}")

            commands.append(image_name)
            subprocess.run(commands, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, check=True)
        else:
            subprocess.run(
                ["docker",
                 "run",
                 "--name", container_name,
                 "-d",
                 "-p", f"127.0.0.1:{port}:{port}",
                 image_name],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_bold(e.stderr)
        return False


def get_alfred_dir():
    home = str(Path.home())
    alfreds_dir = os.path.join(home, ".alfreds")
    return alfreds_dir


def alfreds_init(agent_path: str, working_dir, seed_directory_path=None):
    print("Initializing Alfreds...")

    # check if agent_path is a valid aboslute path and exists
    if agent_path is not None and (not os.path.isabs(agent_path) or not os.path.exists(agent_path)):
        print_bold("Agent path must be a valid absolute path.")
        return

    # check if working_dir is a valid aboslute path
    if working_dir is not None and (not os.path.isabs(working_dir) or not os.path.exists(working_dir)):
        print_bold("Working directory must be a valid absolute path.")
        return

    # check if seed_directory_path is a valid aboslute path
    if seed_directory_path is not None and (not os.path.isabs(seed_directory_path) or not os.path.exists(seed_directory_path)):
        print_bold("Seed directory path must a valid absolute path.")
        return


    # Create a .alfred in user home directory
    alfreds_dir = get_alfred_dir()
    if not os.path.exists(alfreds_dir):
        os.mkdir(alfreds_dir)

    config = {
        "agent_path": agent_path,
        "working_dir": working_dir,
        "seed_dir": agent_path + "/seed_files" if seed_directory_path is None else seed_directory_path
    }

    # write config to alfreds_dir/config.json
    with open(alfreds_dir + "/config.json", "w") as f:
        f.write(json.dumps(config))

    if agent_path is None:
        # input agent path
        agent_path = input("Enter the path to the agent: ")

    if not pull_image("datafacade/alfred-backend"):
        print("Failed to pull alfred-backend image.")
        return

    if not pull_image("datafacade/alfred-ui"):
        print("Failed to pull alfred-ui image.")
        return

    print("Running alfreds-backend image...")
    if not run_container("datafacade/alfred-backend", "alfred-backend", 3737, agent_path, working_dir, seed_directory_path):
        print("Failed to run alfreds-backend.")
        return
    else:
        wait_for_backend(0)
        print("Alfreds-backend is running.")
        if seed_directory_path is not None:
            wait_for_backend_and_load(seed_directory_path, sync_seed_data)

    print("Bootstrapping Alfreds DB")
    if seed_directory_path is not None:
        response = requests.post("http://localhost:3737/bootstrap?agent_dir=" + agent_path + "&working_dir=" + working_dir + "&seed_dir=" + seed_directory_path)
    else:
        response = requests.post("http://localhost:3737/bootstrap?agent_dir=" + agent_path + "&working_dir=" + working_dir)

    if response.status_code != 200:
        print_bold("Failed to bootstrap Alfreds DB.")
        print_bold(response.text)
        return
    else:
        print("Alfreds DB bootstrapped successfully.")

    print("Running alfreds-ui image...")
    if not run_container("datafacade/alfred-ui", "alfred-ui", 5173):
        print_bold("Failed to run alfreds-ui.")
        return


    print("Alfreds UI is ready. Visit localhost:5173 to start using Alfred.")
    print("Opening Alfreds UI in browser...")
    time.sleep(2)
    open_in_browser("http://localhost:5173")


def open_in_browser(url):
    try:
        webbrowser.open(url, new=2)
    except webbrowser.Error:
        print("Failed to open browser. Please visit " + url + " to start using Alfred.")

def load_agents(agent_dir):
    response = requests.post("http://localhost:3737/agent?agent_config_path=" + agent_dir)
    if response.status_code != 200:
        print("Failed to load agent.")
        print(response.text)
        return
    else:
        print("Agent loaded successfully.")



def wait_for_backend(count=0):
    try:
        requests.get("http://localhost:3737/")
    except requests.exceptions.ConnectionError:
        # retry after 5 seconds
        time.sleep(5)
        if count < 3:
            wait_for_backend(count + 1)
            return
        else:
            print_bold("Failed to start alfreds-backend.")
            return

def wait_for_backend_and_load(agent_dir, func=load_agents, count=0):
    try:
        requests.get("http://localhost:3737/")
    except requests.exceptions.ConnectionError:
        # retry after 5 seconds
        time.sleep(5)
        if count < 3:
            wait_for_backend_and_load(agent_dir, func, count + 1)
            return
        else:
            print("Failed to start alfreds-backend.")
            return

    # make a call to alfreds-backend to load the agent
    func(agent_dir)
