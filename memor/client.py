from sys import exit, stderr

import requests

from .settings import (
    COLLECTION,
    LOCAL_DATA_FILE,
    MEMOR_URL,
    SUBSCRIPTIONS_DATA_FILE,
    SUBSCRIPTIONS_FILE,
    TOKEN
)


def add(term, *tags):
    max_id = 0
    with LOCAL_DATA_FILE.open() as f:
        for line in f:
            try:
                item_id = int(line.split(" %%% ")[0])
            except ValueError:
                continue
            else:
                max_id = max(max_id, item_id)
    item_id = max_id + 1

    response = requests.put(
        f"{MEMOR_URL}/collections/{COLLECTION}/{item_id}",
        headers={"Authorization": TOKEN},
        json={
            "term": term,
            "tags": tags
        }
    )
    response.raise_for_status()

    # If everything went okay, update local file:
    tags_str = " ".join(tags)
    with LOCAL_DATA_FILE.open("a") as f:
        f.write(f"{item_id} %%% {term} %%% {tags_str}\n")


def edit(item_id, new_term, *tags):
    response = requests.put(
        f"{MEMOR_URL}/collections/{COLLECTION}/{item_id}",
        headers={"Authorization": TOKEN},
        json={
            "term": new_term,
            "tags": tags
        }
    )
    response.raise_for_status()

    # Update local copy:
    with LOCAL_DATA_FILE.open("wb") as f:
        f.write(response.content)


def delete(item_id):
    response = requests.delete(
        f"{MEMOR_URL}/collections/{COLLECTION}/{item_id}",
        headers={"Authorization": TOKEN}
    )
    response.raise_for_status()

    # Update local copy:
    with LOCAL_DATA_FILE.open("wb") as f:
        f.write(response.content)


# SYNC
def sync():
    # Own collection:
    response = requests.get(f"{MEMOR_URL}/collections/{COLLECTION}")
    response.raise_for_status()

    with LOCAL_DATA_FILE.open("wb") as f:
        f.write(response.content)

    # Subscriptions:
    with SUBSCRIPTIONS_FILE.open() as f:
        subscriptions = set(f.read().split("\n"))

    with SUBSCRIPTIONS_DATA_FILE.open("wb") as f:
        for slug in subscriptions:
            if not slug:
                continue

            response = requests.get(f"{MEMOR_URL}/collections/{slug}")
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                print(f"Error {response.status_code} while retrieving {slug}", file=stderr)
                continue
            else:
                for line in response.content.split(b"\n"):
                    if not line:
                        continue
                    f.write(line)
                    f.write(f" source={slug}".encode())
                    f.write(b"\n")


# SEARCH
def do_search(data_file, args):
    and_groups = []

    and_group = []
    for tag in args:
        if tag == "/" and and_group:
            and_groups.append(and_group)
            and_group = []
        else:
            and_group.append(tag)

    if and_group:
        and_groups.append(and_group)

    results = []

    if not and_group:
        with data_file.open() as f:
            for line in f:
                item_id, term, tags_str = line.strip().split(" %%% ")
                results.append((item_id, term, tags_str.split()))
    else:
        with data_file.open() as f:
            for line in f:
                item_id, term, tags_str = line.strip().split(" %%% ")
                tags = tags_str.split()

                for group in and_groups:
                    for search_tag in group:
                        if search_tag not in tags:
                            break
                    else:
                        results.append((item_id, term, tags))
                        break

    return results


def do_search_local(args):
    return do_search(LOCAL_DATA_FILE, args)


def do_search_subscriptions(args):
    return do_search(SUBSCRIPTIONS_DATA_FILE, args)


def search(*args, show_subscriptions=True):
    for item_id, term, tags in do_search_local(args):
        tags_str = " ".join(tags)
        print(f"{item_id} %%% {term} %%% {tags_str}")

    if show_subscriptions:
        for item_id, term, tags in do_search_subscriptions(args):
            tags_str = " ".join(tags)
            print(f"SUB %%% {term} %%% {tags_str}")


def local_search(*args):
    return search(*args, show_subscriptions=False)


def jsearch(*args, show_subscriptions=True):
    import json

    for item_id, term, tags in do_search_local(args):
        print(json.dumps({
            "id": item_id,
            "origin": "local",
            "term": term,
            "tags": tags
        }))

    if show_subscriptions:
        for item_id, term, tags in do_search_subscriptions(args):
            print(json.dumps({
                "origin": "subscription",
                "term": term,
                "tags": tags
            }))


def local_jsearch(*args):
    return jsearch(*args, show_subscriptions=False)


# SUBSCRIPTIONS
def subscribe(slug):
    if slug == COLLECTION:
        print("You already subscribe to your own collection!", file=stderr)
        exit(10)

    response = requests.get(f"{MEMOR_URL}/collections/{slug}")
    if response.status_code == 404:
        print("Collection does not exist", file=stderr)
        exit(11)

    with SUBSCRIPTIONS_FILE.open() as f:
        subscriptions = set(x for x in f.read().split("\n") if x)

    subscriptions.add(slug)

    with SUBSCRIPTIONS_FILE.open("w") as f:
        f.write("\n".join(subscriptions))

    sync()


def unsubscribe(slug):
    with SUBSCRIPTIONS_FILE.open() as f:
        subscriptions = set(x for x in f.read().split("\n") if x)

    try:
        subscriptions.remove(slug)
    except KeyError:
        pass
    else:
        with SUBSCRIPTIONS_FILE.open("w") as f:
            f.write("\n".join(subscriptions))

    sync()
