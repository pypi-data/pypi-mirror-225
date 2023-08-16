import json

from alfreds_init.init import get_alfred_dir, alfreds_init
from alfreds_stop.stop import stop_containers


def refresh():
    stop_containers()

    alfred_dir = get_alfred_dir()
    with open(alfred_dir + "/config.json", "r") as f:
        config = json.load(f)
        agent_path = config["agent_path"]
        working_dir = config["working_dir"]
        seed_dir = config["seed_dir"]

    alfreds_init(agent_path, working_dir, seed_dir)

    print("Alfred refreshed.")