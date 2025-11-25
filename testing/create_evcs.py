import threading
import os
import sys

def execute(circuit_n: int):
    tags_a = []
    tags_b = []
    def create_evc(tag_a, tag_b, n):
        b = "curl -H 'Content-type: application/json' -X POST http://localhost:8181/api/kytos/mef_eline/v2/evc/ -d "
        a = '{"name": "my evc' + str(n)
        a += '", "dynamic_backup_path": true, "enabled": true, "uni_a": {"tag": {"value": '
        a += str(tag_a)
        a += ', "tag_type": 1}, "interface_id": "00:00:00:00:00:00:00:01:1"}, "uni_z": {"tag": {"value": '
        a += str(tag_b)
        a += ', "tag_type": 1}, "interface_id": "00:00:00:00:00:00:00:02:1"}}'
        a = b + "'" + a + "'"
        os.system(a)
        print()

    def set_tag_ranges(tag_ranges):
        a = "curl -H 'Content-type: application/json' -X POST "
        a += "http://localhost:8181/api/kytos/topology/v3/interfaces/00:00:00:00:00:00:00:01:1/tag_ranges -d "
        b = '{"tag_type": "vlan", "tag_ranges": ' + str(tag_ranges) + '}'
        c = a + "'" + b + "'"
        print("Setting tag ranges in 00:00:00:00:00:00:00:01:1 switch")
        os.system(c)
        print()
        a = "curl -H 'Content-type: application/json' -X POST "
        a += "http://localhost:8181/api/kytos/topology/v3/interfaces/00:00:00:00:00:00:00:02:1/tag_ranges -d "
        b = '{"tag_type": "vlan", "tag_ranges": ' + str(tag_ranges) + '}'
        c = a + "'" + b + "'"
        print("Setting tag ranges in 00:00:00:00:00:00:00:02:1 switch")
        os.system(c)
        print()

    tag_ranges = []
    last_tag = 0
    for (i, j) in zip(range(1, 4096, (circuit_n*2-1)*2), range(circuit_n*2, 4096, (circuit_n*2-1)*2)):
        tag_ranges.append([i, j])
    last_tag = j
    #set_tag_ranges(tag_ranges)
    print(f"Tag ranges applied, {len(tag_ranges)} items: [{tag_ranges[:3]}, ..., {tag_ranges[-3:]}]")

    print("\nCreating EVCs")
    threads = list()
    counter = 0
    for i in range(1, circuit_n*2, 2):
        tags = []
        for q in range(i, last_tag, (circuit_n*2-1)*2):
            tags.append([q, q+1])
        tags_a.append(tags)
        tags_b.append(tags)
        counter += 1
        t = threading.Thread(target=create_evc, args=(tags, tags, counter))
        threads.append(t)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print()


if __name__ == "__main__":
    circuit_n = 100
    try:
        n = sys.argv[1]
        try:
            circuit_n = int(n)
            print(f"{circuit_n} circuits will be created.")
        except ValueError:
            print("The argument should be an integer")
            sys.exit(1)
    except IndexError:
        print(f"No number detected, {circuit_n} circuits will be created.")
    execute(circuit_n)