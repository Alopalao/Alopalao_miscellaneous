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
    6: {0: 0, 1: 0}, 1: {0: 0, 1: 0}, 2: {0: 0, 1: 0}, 3: {0: 0, 1: 0}, 4: {0: 0, 1: 0}, 5: {0: 0, 1: 0}
}


def create_evc(vlan:int, extra:str="") -> str:
    evc = {
        "name": "evc"+str(vlan)+extra,
        "dynamic_backup_path": True,
        "uni_a": {
            "interface_id": "00:00:00:00:00:00:00:01:1",
            "tag": {"tag_type": "vlan", "value": [[vlan, vlan+2]]}},
        "uni_z": {
            "interface_id": "00:00:00:00:00:00:00:02:1",
            "tag": {"tag_type": "vlan", "value": [[vlan, vlan+2]]}}
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

def toggle_evc(vlan:int, thread_n:int):
    deleted = True
    for i in range(1, 301):
        if deleted:
            thread_counter[thread_n][0] += 1
            evc_id = create_evc(vlan) 
            if not evc_id:
                continue
        thread_counter[thread_n][1] += 1
        deleted = delete_evc(evc_id)

def start_toggle(threads:int) -> None:
    th_list = list()
    for i in range(1, threads+1):
        t = threading.Thread(target=toggle_evc, args=(i*10, i))
        th_list.append(t)
    
    for thread in th_list:
        thread.start()
    for thread in th_list:
        thread.join()


if __name__ == "__main__":
    threads = 6
    circuits = 2000
    try:
        threads = int(sys.argv[1])
        circuits = int(sys.argv[2])
    except IndexError:
        #print(f"A number was not detected, {threads} threads will be deployed and {circuits} circuits will be created.")
        x = 0
    start_toggle(threads)
    for i in range(1, threads+1):
        print(f"CREATED -> {thread_counter[i][0]} - DELETED -> {thread_counter[i][1]}")