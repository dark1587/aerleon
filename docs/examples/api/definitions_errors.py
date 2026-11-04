"""Collisions and undefined nested names."""

from aerleon import api
from aerleon.lib import naming

MGMT = {"networks": {"MGMT": {"values": [{"address": "10.0.0.0/24"}]}}}
SSH = {"services": {"SSH": [{"port": 22, "protocol": "tcp"}]}}
UNSEEN = {
    "networks": {
        "MGMT": {"values": [{"address": "10.0.0.0/24"}]},
        "INTERNAL": {"values": [{"name": "MGMT"}, {"name": "NOT_DEFINED"}]},
    }
}
POLICY = {
    "filename": "edge-inbound",
    "filters": [
        {
            "header": {"targets": {"cisco": "edge-inbound"}},
            "terms": [
                {"name": "allow-internal", "source-address": "INTERNAL", "action": "accept"}
            ],
        }
    ],
}


def report(e: Exception) -> None:
    print(f"{type(e).__name__}: {str(e).strip()}")


def main() -> None:
    print("--- collision between two dictionaries ---")
    # --8<-- [start:collision]
    defs = naming.Naming()
    defs.ParseDefinitionsObject(MGMT, "inventory")
    try:
        defs.ParseDefinitionsObject(MGMT, "inventory-copy")
    except naming.Error as e:
        report(e)
    # --8<-- [end:collision]

    print("--- collision between a file and a dictionary ---")
    defs = naming.Naming("def", "services.yaml")
    try:
        defs.ParseDefinitionsObject(SSH, "extra-services")
    except naming.Error as e:
        report(e)

    print("--- undefined name, directory ---")
    # --8<-- [start:directory]
    try:
        naming.Naming("def_unseen")
    except naming.Error as e:
        report(e)
    # --8<-- [end:directory]

    print("--- undefined name, single file ---")
    # --8<-- [start:single]
    defs = naming.Naming("def_unseen", "networks.yaml")
    print(defs.unseen_networks)
    # --8<-- [end:single]

    print("--- undefined name, used by Generate ---")
    # --8<-- [start:generate]
    defs = naming.Naming()
    defs.ParseDefinitionsObject(UNSEEN, "inventory")
    try:
        api.Generate([POLICY], defs)
    except Exception as e:
        lines = str(e).strip().splitlines()
        print(type(e).__name__)
        print(lines[0])
        print(lines[-1])
    # --8<-- [end:generate]


if __name__ == "__main__":
    main()
