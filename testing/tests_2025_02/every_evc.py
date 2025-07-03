"""Script to create every possible (but same VLAN for UNIs) EVC to test scripts for filtering the database.
 This script uses Amlight topology.
"""
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

def create_evc(vlan_a, vlan_z, uni_a, uni_z, extra:str="") -> str:
    evc = {
        "name": "evc"+str(vlan_a)+"-"+str(vlan_z)+extra,
        "dynamic_backup_path": True,
        "uni_a": {
            "interface_id": uni_a,
        },
        "uni_z": {
            "interface_id": uni_z,
        }
    }
    if vlan_a:
        evc["uni_a"]["tag"] = {"tag_type": "vlan", "value": vlan_a}
    if vlan_z:
        evc["uni_z"]["tag"] = {"tag_type": "vlan", "value": vlan_z}

    response = httpx.post(MEF_URL, json=evc, timeout=120)
    if response.status_code//100 == 2:
        data = response.json()
        if data["deployed"] is False:
            return False, data["circuit_id"]
        print(f"DEPLOYED -> {uni_a}***{vlan_a} - {uni_z}***{vlan_z}")
        return True, data["circuit_id"]

    return False, None

def delete_evc(evc_id:str=None) -> bool:
    if not evc_id:
        return False
    response = httpx.delete(MEF_URL+evc_id+"/", timeout=120)
    if response.status_code//100 == 2:
        return True

    print("COULD NOT DELETE WARNING :O")
    return False

if __name__ == "__main__":
    possible_VLAN_a = [1, "untagged", "any", None]
    possible_VLAN_z = [1, "untagged", "any", None]
    possible_num = 100
    interfaces = {'00:00:00:00:00:00:00:18': ['00:00:00:00:00:00:00:18:14',
              '00:00:00:00:00:00:00:18:11',
              '00:00:00:00:00:00:00:18:13',
              '00:00:00:00:00:00:00:18:16',
              '00:00:00:00:00:00:00:18:57'],
             '00:00:00:00:00:00:00:13': ['00:00:00:00:00:00:00:13:52',
              '00:00:00:00:00:00:00:13:17',
              '00:00:00:00:00:00:00:13:5',
              '00:00:00:00:00:00:00:13:2',
              '00:00:00:00:00:00:00:13:3'],
             '00:00:00:00:00:00:00:20': ['00:00:00:00:00:00:00:20:16',
              '00:00:00:00:00:00:00:20:59',
              '00:00:00:00:00:00:00:20:17'],
             '00:00:00:00:00:00:00:22': ['00:00:00:00:00:00:00:22:15',
              '00:00:00:00:00:00:00:22:61',
              '00:00:00:00:00:00:00:22:18'],
             '00:00:00:00:00:00:00:15': ['00:00:00:00:00:00:00:15:54',
              '00:00:00:00:00:00:00:15:64',
              '00:00:00:00:00:00:00:15:4',
              '00:00:00:00:00:00:00:15:7',
              '00:00:00:00:00:00:00:15:6'],
             '00:00:00:00:00:00:00:17': ['00:00:00:00:00:00:00:17:10',
              '00:00:00:00:00:00:00:17:56',
              '00:00:00:00:00:00:00:17:9'],
             '00:00:00:00:00:00:00:19': ['00:00:00:00:00:00:00:19:15',
              '00:00:00:00:00:00:00:19:13',
              '00:00:00:00:00:00:00:19:58',
              '00:00:00:00:00:00:00:19:12'],
             '00:00:00:00:00:00:00:21': ['00:00:00:00:00:00:00:21:14',
              '00:00:00:00:00:00:00:21:18',
              '00:00:00:00:00:00:00:21:60'],
             '00:00:00:00:00:00:00:14': ['00:00:00:00:00:00:00:14:8',
              '00:00:00:00:00:00:00:14:7',
              '00:00:00:00:00:00:00:14:53'],
             '00:00:00:00:00:00:00:16': ['00:00:00:00:00:00:00:16:6',
              '00:00:00:00:00:00:00:16:5',
              '00:00:00:00:00:00:00:16:55'],
             '00:00:00:00:00:00:00:12': ['00:00:00:00:00:00:00:12:8',
              '00:00:00:00:00:00:00:12:10',
              '00:00:00:00:00:00:00:12:51',
              '00:00:00:00:00:00:00:12:12',
              '00:00:00:00:00:00:00:12:4',
              '00:00:00:00:00:00:00:12:1',
              '00:00:00:00:00:00:00:12:63'],
             '00:00:00:00:00:00:00:11': ['00:00:00:00:00:00:00:11:11',
              '00:00:00:00:00:00:00:11:9',
              '00:00:00:00:00:00:00:11:1',
              '00:00:00:00:00:00:00:11:2',
              '00:00:00:00:00:00:00:11:50',
              '00:00:00:00:00:00:00:11:62',
              '00:00:00:00:00:00:00:11:3']}
    switches = [
        '00:00:00:00:00:00:00:18',
        '00:00:00:00:00:00:00:13',
        '00:00:00:00:00:00:00:20',
        '00:00:00:00:00:00:00:22',
        '00:00:00:00:00:00:00:15',
        '00:00:00:00:00:00:00:17',
        '00:00:00:00:00:00:00:19',
        '00:00:00:00:00:00:00:21',
        '00:00:00:00:00:00:00:14',
        '00:00:00:00:00:00:00:16',
        '00:00:00:00:00:00:00:12',
        '00:00:00:00:00:00:00:11'
    ]
    sw_index = 0
    for poss_a in possible_VLAN_a:
        for poss_z in possible_VLAN_z:
            vlan_a = poss_a
            vlan_z = poss_z
            if poss_a == 1:
                possible_num += 1
                vlan_a = possible_num
            if poss_z == 1:
                possible_num += 1
                vlan_z = possible_num

            deployed = False

            while not deployed:
                try:
                    uni_a = interfaces[switches[sw_index]].pop()
                except Exception:
                    sw_index += 1
                    continue

                try:
                    uni_z = interfaces[switches[sw_index+1]].pop()
                except Exception:
                    sw_index += 1
                    continue
                deployed, id_ = create_evc(vlan_a, vlan_z, uni_a, uni_z)

                if not deployed:
                    if id_:
                        delete_evc(id_)

