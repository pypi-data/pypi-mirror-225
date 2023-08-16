from alfreds_init.init import stop_container


def stop_containers():
    stop_container("alfred-backend")
    stop_container("alfred-ui")
