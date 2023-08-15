import os
from google.cloud import tasks_v2

import json


def process_event_task(event_id: int) -> None:
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
