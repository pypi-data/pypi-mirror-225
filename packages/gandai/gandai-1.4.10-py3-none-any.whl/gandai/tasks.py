import os
from google.cloud import tasks_v2
from threading import Thread

from gandai import query, main

import json

from time import sleep


def process_event_local(event_id: int):
    # Simulate the processing time
    event = query.find_event_by_id(event_id=event_id)
    main.process_event(event_id=event.id)
    print(f"Processing event {event_id}")

def process_event_task(event_id: int) -> None:
    print(os.getenv("ENV"))
    if os.getenv("ENV") == "local":
        # this may be hard to debug
        process_event_local(event_id=event_id)
        # Thread(target=process_event_local, args=(event_id,)).start()
    else:
        print("omglol")
        client = tasks_v2.CloudTasksClient()
        project = os.getenv("PROJECT_ID", "targetselect-staging")
        queue = "phq"
        location = "us-central1"
        parent = client.queue_path(project, location, queue)
        task = {
            "app_engine_http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "app_engine_routing": {"service": "api"},
                "relative_uri": "/process_event",
                "headers": {"Content-type": "application/json"},
                "body": json.dumps({"event_id": event_id}).encode(),
            }
        }
        response = client.create_task(parent=parent, task=task)
        return response
