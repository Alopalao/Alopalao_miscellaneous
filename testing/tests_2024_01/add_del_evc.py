import random
import httpx
import sys
import time
import threading

MEF_URL = "http://localhost:8181/api/kytos/mef_eline/v2/evc/"
api_response = ""
bool_conf = ""
my_vlans = ""
thread_counter = {
    0: {"add": 0, "del": 0},
    1: {"add": 0, "del": 0},
    2: {"add": 0, "del": 0},
    3: {"add": 0, "del": 0},
    4: {"add": 0, "del": 0},
    5: {"add": 0, "del": 0}
}

def create_evc(vlan:int, extra:str="") -> str:
    evc = {
        "name": "evc"+str(vlan)+extra,
        "dynamic_backup_path": True,
        "uni_a": {
            "interface_id": "00:00:00:00:00:00:00:01:1",
            "tag": {"tag_type": "vlan", "value": vlan}},
        "uni_z": {
            "interface_id": "00:00:00:00:00:00:00:02:1",
            "tag": {"tag_type": "vlan", "value": vlan}}
    }
    response = httpx.post(MEF_URL, json=evc, timeout=120)
    if response.status_code//100 == 2:
        return response.json()["circuit_id"]
    print(response.text)
    return None

def delete_evc(evc_id:str=None) -> bool:
    if not evc_id:
        return False
    response = httpx.delete(MEF_URL+evc_id+"/", timeout=120)
    if response.status_code//100 == 2:
        return True
    return False

def toggle_evc(vlan:int, thread_n:int, iterations:int):
    print(f"Iterating {iterations} times")
    deleted = True
    created = set()
    vlan_counter = vlan
    for i in range(iterations):
        if created and random.randrange(1, 4) == 1:
            deleted = False
            evc_id = created.pop()
            while not deleted:
                deleted = delete_evc(evc_id)
            thread_counter[thread_n]["del"] += 1
        else:
            evc_id = None
            while not evc_id:
                evc_id = create_evc(vlan_counter)
            thread_counter[thread_n]["add"] += 1
            created.add(evc_id)
            vlan_counter += random.randrange(1,3)


def start_toggle(threads:int, iterations:int) -> None:
    th_list = list()
    extra = 0
    pack = iterations//threads
    for i in range(threads):
        if i + 1 == threads:
            extra = iterations - threads * pack
        t = threading.Thread(target=toggle_evc, args=(i*pack+extra, i, pack+extra))
        th_list.append(t)
    
    for thread in th_list:
        thread.start()
    for thread in th_list:
        thread.join()


if __name__ == "__main__":
    threads = 6
    iterations = 2000
    try:
        threads = int(sys.argv[1])
        circuits = int(sys.argv[2])
    except IndexError:
        print(f"A number was not detected, {threads} threads will be deployed and {iterations} iterations will be run in total.")
    start_toggle(threads, iterations)
    created = 0
    deleted = 0
    for i in range(threads):
        created += thread_counter[i]['add']
        deleted += thread_counter[i]['del']
        print(f"CREATED -> {thread_counter[i]['add']} - DELETED -> {thread_counter[i]['del']}")
    print(f"EVCs active -> {created - deleted}")