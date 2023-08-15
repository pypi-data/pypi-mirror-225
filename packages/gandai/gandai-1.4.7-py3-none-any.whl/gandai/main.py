from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from time import time

import pandas as pd
from dacite import from_dict

from gandai import query, models, gpt
from gandai.sources import GrataWrapper as grata
from gandai.sources import GoogleMapsWrapper as google


def enrich_company_by_domain(domain: str) -> None:
    company = query.find_company_by_domain(domain)
    if "company_uid" not in company.meta.keys():
        # company_uid is a grata specific field
        resp = grata.enrich(domain)
        # what happens when company is not found?
        company.description = resp.get("description")
        company.meta = {**company.meta, **resp}
        query.update_company(company)


def insert_similiar(search: models.Search, domain: str) -> None:
    grata_companies = grata.find_similar(domain=domain, search=search)
    query.insert_companies_as_targets(
        companies=grata_companies, search_uid=search.uid, actor_key="grata"
    )


def process_event(event_id: int) -> None:
    e: models.Event = query.find_event_by_id(event_id)
    search = query.find_search_by_uid(search_uid=e.search_uid)
    domain = e.domain
    if e.type == "create":
        pass
    elif e.type == "advance":
        enrich_company_by_domain(domain=domain)
    elif e.type == "validate":
        enrich_company_by_domain(domain=domain)
        insert_similiar(search=search, domain=domain)
    elif e.type == "send":
        pass
    elif e.type == "client_approve":
        pass
    elif e.type == "reject":
        pass
    elif e.type == "client_reject":
        pass
    elif e.type == "conflict":
        insert_similiar(search=search, domain=domain)
    elif e.type == "client_conflict":
        insert_similiar(search=search, domain=domain)

    elif e.type == "criteria":
        search.context["operator"] = e.data["operator"]
        search.context["result_count"] = e.data["result_count"]
        search.inclusion = e.data["inclusion"]
        search.exclusion = e.data["exclusion"]
        query.update_search(search)

        if len(search.inclusion["keywords"]) > 0:
            grata_companies = grata.find_by_criteria(search)
            query.insert_companies_as_targets(
                companies=grata_companies, search_uid=search.uid, actor_key="grata"
            )

    elif e.type == "maps":
        start = time()
        top_n = e.data.get("top_n", 5)
        
        def process_area(area):
            centroids = gpt.get_top_zip_codes(area=area, top_n=top_n)
            place_ids = google.fetch_unique_place_ids(search_phrase=e.data['phrase'], locations=centroids, radius_miles=25)
            print(f"{len(place_ids)} place_ids found in {area}")
            google.build_place_ids_async(place_ids=place_ids, search=search)
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(process_area, e.data['areas'])
        
        print(f"🗺  Maps took {time() - start} seconds")
        
        
    
    elif e.type == "reset":
        print("💣 Resetting Inbox...")
        query.reset_inbox(search_uid=search.uid)

    query.insert_checkpoint(models.Checkpoint(event_id=e.id))
    print(f"processed: {e}")


def process_events(search_uid: int) -> int:
    """
    Process all events for a given search
    """
    events = query.event(search_uid=search_uid)
    checkpoints = query.checkpoint(search_uid=search_uid)

    q = list(set(events["id"].tolist()) - set(checkpoints["event_id"].tolist()))

    # for event_id in q:
    #     print(event_id)
    #     process_event(event_id)

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_event, q)

    return len(q)
