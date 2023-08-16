import json

from alfreds_init.init import get_alfred_dir, run_container, open_in_browser


def alfred_start():
    # read agent path and working dir from alfred_agent_dir/config.json
    alfred_agent_dir = get_alfred_dir()
    with open(alfred_agent_dir + "/config.json", "r") as f:
        config = json.load(f)
        agent_path = config["agent_path"]
        working_dir = config["working_dir"]
        seed_dir = config["seed_dir"]

    if not run_container("datafacade/alfred-backend", "alfred-backend", 3737, agent_path, working_dir, seed_dir):
        print("Failed to run alfreds-backend.")
        return

    print("Alfred Backend started.")
    # run alfred ui
    if not run_container("datafacade/alfred-ui", "alfred-ui", 5173):
        print("Failed to run alfreds-ui.")
        return

    print("Alfred UI started.")
    open_in_browser("http://localhost:5173/")
