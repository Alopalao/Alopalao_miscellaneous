import random
import httpx
import sys
import time
import threading
from copy import deepcopy

MEF_URL = "http://localhost:8181/api/kytos/mef_eline/v2/evc/"
api_response = ""
bool_conf = ""
my_vlans = ""

def create_evc(vlan:int, extra:str="") -> str:
    evc = {
        "name": "evc"+str(vlan)+extra,
        "dynamic_backup_path": True,
        "uni_a": {
            "interface_id": "00:00:00:00:00:00:00:01:1",
            "tag": {"tag_type": "vlan", "value": [[vlan,vlan]]}},
        "uni_z": {
            "interface_id": "00:00:00:00:00:00:00:02:1",
            "tag": {"tag_type": "vlan", "value": [[vlan,vlan]]}}
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

def toggle_evc(vlan:int, thread_n:int, iterations:int, thread_counter:dict):
    print(f"Iterating {iterations} times")
    deleted = True
    vlan_counter = vlan
    created_vlan = list()
    created_ids = list()
    deleted_vlans = list()
    restore_counter = 0
    for _ in range(iterations):
        # n0% chance to delete a created EVC
        if len(created_vlan) > len(deleted_vlans) and random.randrange(1, 2) == 1:
            deleted = False
            index = len(deleted_vlans)
            evc_id = created_ids[index]
            deleted_vlans.append(created_vlan[index])
            while not deleted:
                deleted = delete_evc(evc_id)
            thread_counter[thread_n]["add"] -= 1
        else:
            evc_id = create_evc(vlan_counter)
            created_vlan.append(vlan_counter)
            created_ids.append(evc_id)
            thread_counter[thread_n]["add"] += 1
            vlan_counter += random.randrange(1,3)

        # Additionaly every iteration has a n% chance to restore a deleted vlan
        if restore_counter < len(deleted_vlans) and random.randrange(1, 2) == 1:
            vlan = deleted_vlans[restore_counter]
            evc_id = create_evc(vlan)
            created_vlan.append(vlan)
            created_ids.append(evc_id)
            thread_counter[thread_n]["add"] += 1
            restore_counter += 1
    #print(f"THREAD {thread_n}: {vlan} - {i+vlan} ")
    print("FROM THREAD -> ", thread_n)
    print(created_vlan)
    print(deleted_vlans)
    print(restore_counter)
    for _ in range(restore_counter):
        deleted_vlans.pop(0)
    rest_add_vlans = set(created_vlan)
    rest_del_vlans = set(deleted_vlans)
    vlans_alive = rest_add_vlans - rest_del_vlans
    print("Enabled VLANS -> ", vlans_alive)
    thread_counter[thread_n]["vlans"] = sorted(list(vlans_alive))
    print("----------------------------------------------")
    

def start_toggle(threads:int, iterations:int, thread_counter:dict) -> None:
    th_list = list()
    extra = 0
    pack = iterations//threads
    for i in range(threads):
        if i + 1 == threads:
            extra = iterations - threads * pack
        t = threading.Thread(target=toggle_evc, args=(((int(i*1.7))*(pack))+1, i, pack+extra, thread_counter))
        th_list.append(t)   
    
    for thread in th_list:
        thread.start()
    for thread in th_list:
        thread.join()

def generate_range(total_vlans: list) -> list[list[int]]:
    range_count = 0
    ranges = list()
    vlan_sight = 0
    for vlan in total_vlans:
        if vlan_sight == 0:
            vlan_sight = vlan
            range_count = 0
        else:
            if vlan_sight + range_count + 1 == vlan:
                range_count += 1
            else:
                ranges.append([vlan_sight, vlan_sight+range_count])
                range_count = 0
                vlan_sight = vlan

    if range_count == 0:
        ranges.append([vlan, vlan])
    else:
        ranges.append([vlan_sight, vlan])
    return ranges

def range_difference(
    ranges_a: list[list[int]],
    ranges_b: list[list[int]]
) -> list[list[int]]:
    if not ranges_a:
        return []
    if not ranges_b:
        return deepcopy(ranges_a)
    result = []
    a_i, b_i = 0, 0
    update = True
    while a_i < len(ranges_a) and b_i < len(ranges_b):
        if update:
            start_a, end_a = ranges_a[a_i]
        else:
            update = True
        start_b, end_b = ranges_b[b_i]
        if end_a < start_b:
            result.append([start_a, end_a])
            a_i += 1
        elif end_b < start_a:
            b_i += 1
        else:
            # Intersection
            if start_a < start_b:
                result.append([start_a, start_b - 1])
            if end_a > end_b:
                start_a = end_b + 1
                update = False
                b_i += 1
            else:
                a_i += 1
    while a_i < len(ranges_a):
        if update:
            start_a, end_a = ranges_a[a_i]
        else:
            update = True
        result.append([start_a, end_a])
        a_i += 1
    return result

if __name__ == "__main__":
    threads = 7
    iterations = 2200
    try:
        threads = int(sys.argv[1])
        circuits = int(sys.argv[2])
    except IndexError:
        print(f"A number was not detected, {threads} threads will be deployed and {iterations} iterations will be run in total.")
    thread_counter = {}
    for i in range(7):
        thread_counter[i] = {"add": 0, "vlans": list()}

    start_toggle(threads, iterations, thread_counter)

    created = 0
    for i in range(threads):
        created += thread_counter[i]['add']
        #print(f"CREATED -> {thread_counter[i]['add']}")
    print(f"EVCs active -> {created}")

    total_vlans = list()
    for i in range(threads):
        for vlan in thread_counter[i]["vlans"]:
            total_vlans.append(vlan)
    print("USED VLANS -> ", total_vlans)

    ranges = generate_range(total_vlans)
    print("List of ranges?? -> ", ranges)

    ava_vlans = range_difference([[1, 4095]], ranges)
    print("Available vlans -> ", ava_vlans)

    
