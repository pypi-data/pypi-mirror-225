import json

import requests

from alfreds_init.init import get_alfred_dir, stop_container, run_container, wait_for_backend_and_load, sync_seed_data


def alfred_seed(csv_directory_path):
    print("Seeding Alfreds...")
    alfred_agent_dir = get_alfred_dir()
    # read agent path from alfred_agent_dir/config.json
    with open(alfred_agent_dir + "/config.json", "r") as f:
        config = json.load(f)

    config["seed_dir"] = csv_directory_path


    if not run_container("datafacade/alfred-backend", "alfred-backend", 3737, config["agent_path"], config["working_dir"], config["seed_dir"]):
        print("Failed to run alfreds-backend.")
        return
    print("Syncing seed data...")
    wait_for_backend_and_load(csv_directory_path, sync_seed_data)

    print("Seeding complete.")

    with open(alfred_agent_dir + "/config.json", "w") as f:
        f.write(json.dumps(config))
