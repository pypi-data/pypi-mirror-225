import json

from alfreds_init.init import get_alfred_dir, stop_container, pull_image, run_container, wait_for_backend_and_load


def update_agent(new_agent_file_path):
    print("Updating agent...")
    alfred_agent_dir = get_alfred_dir()
    # read working dir from alfred_agent_dir/config.json
    with open(alfred_agent_dir + "/config.json", "r") as f:
        config = json.load(f)
        working_dir = config["working_dir"]
        seed_dir = config["seed_dir"]

    if working_dir is None:
        print("Error: working directory not found")
        return


    if not run_container("datafacade/alfred-backend", "alfred-backend", 3737, new_agent_file_path, working_dir, seed_dir):
        print("Failed to run alfreds-backend.")
        return
    else:
        wait_for_backend_and_load(new_agent_file_path)

    # write new agent path to alfred_agent_dir/config.json
    config["agent_path"] = new_agent_file_path
    with open(alfred_agent_dir + "/config.json", "w") as f:
        f.write(json.dumps(config))

