"""Load services from a file and networks from a dictionary."""

from aerleon.lib import naming

networks = {
    "networks": {
        "MGMT": {
            "values": [
                {"address": "10.0.0.0/24"},
                {"address": "192.168.10.0/24"},
            ]
        }
    }
}


def main() -> None:
    # --8<-- [start:load]
    defs = naming.Naming("def", "services.yaml")
    defs.ParseDefinitionsObject(networks, "inventory")
    # --8<-- [end:load]
    print([str(a) for a in defs.GetNet("MGMT")])
    print(sorted(defs.GetServiceNames()))


if __name__ == "__main__":
    main()
