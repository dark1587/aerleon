"""Nested tokens: forward references and the bare-string gotcha."""

from aerleon.lib import naming


def main() -> None:
    print("--- token names ---")
    # --8<-- [start:names]
    defs = naming.Naming()
    defs.ParseDefinitionsObject(
        {
            "networks": {
                "INTERNAL": {
                    "values": [
                        {"name": "MGMT"},
                        {"address": "172.16.0.0/12", "comment": "lab"},
                    ]
                },
                "MGMT": {
                    "values": [
                        {"address": "10.0.0.0/24"},
                        {"address": "192.168.10.0/24"},
                    ]
                },
            }
        },
        "inventory",
    )
    # --8<-- [end:names]
    print([str(a) for a in defs.GetNet("INTERNAL")])
    print(defs.unseen_networks)

    print("--- bare string ---")
    # --8<-- [start:bare]
    bare = naming.Naming()
    bare.ParseDefinitionsObject(
        {"networks": {"RESERVED": {"values": ["10.0.0.0/8"]}}}, "inventory"
    )
    # --8<-- [end:bare]
    print([str(a) for a in bare.GetNet("RESERVED")])
    print(bare.unseen_networks)


if __name__ == "__main__":
    main()
