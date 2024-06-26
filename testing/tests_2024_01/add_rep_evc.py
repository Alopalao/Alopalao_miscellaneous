import random
import httpx
import sys
import time
import threading

MEF_URL = "http://localhost:8181/api/kytos/mef_eline/v2/evc/"
api_response = ""
bool_conf = ""
my_vlans = ""
TRIED = list() # VLANS TRIED TO CREATE, inside thread
CREATED = list() # VLANS CREATED SUCCESS
FAILS = list() # VLANS FAILED TO CREATE
VLANS = set() # VLANS TRIED TO CREATE, outside thread
FAILS_V = list() # VLANS FAILED INFO, verbose
DUPP = set() # DUPLICATED VLANS

def start_process(threads: int, circuits: int) -> None:
    def create_evc(vlan: int, extra:str):
        TRIED.append(vlan)
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
        #time.sleep(1)
        response = httpx.post(MEF_URL, json=evc, timeout=120)
        if response.status_code//100 == 2:
            CREATED.append(vlan)
        else:
            FAILS.append(vlan)
            FAILS_V.append(f"EVC: {evc['name']}, VLAN: {vlan}, STATUS: EVC created, RESPONSE: {response.text}")
        


    th_list = list()
    extra = 0
    pack = circuits//threads
    for i in range(threads):
        if i + 1 == threads:
            extra = circuits - threads * pack
        print("CREATING -> ", pack+extra)
        for _ in range(pack+extra):
            vlan = random.randrange(1, 3000)
            dupp = ""
            if vlan in VLANS:
                dupp = "-dup"
                DUPP.add(vlan)
            else:
                VLANS.add(vlan)
            t = threading.Thread(target=create_evc, args=(vlan,dupp))
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
        print(f"A number was not detected, {threads} threads will be deployed and {circuits} circuits will be created.")
    start_process(threads, circuits)

    if FAILS_V:
        print("Rejected: ", len(FAILS_V))
        for fail in FAILS_V:
            print(fail)
    else:
        print("No rejected")

    print("Looking for erros: ")
    unique = set(TRIED)
    if len(TRIED) - len(FAILS) != len(CREATED):
        print("Tried - unique != Created")
    else:
        print("NO ERRORS")


    print(f'Created EVCs -> {len(CREATED)}')
    print(f"TRIED -> {TRIED}")
    print(f"CREATED -> {CREATED}")
    print(f"FAILS -> {FAILS}")
    print(f"DUPLICATED -> {DUPP}")