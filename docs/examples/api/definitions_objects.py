"""Load definitions from Python dictionaries."""

from aerleon.lib import naming

# --8<-- [start:data]
networks = {
    "networks": {
        "MGMT": {
            "values": [
                {"address": "10.0.0.0/24"},
                {"address": "192.168.10.0/24"},
            ]
        },
        "RESERVED": {
            "values": [
                {"address": "0.0.0.0/8"},
                {"address": "10.0.0.0/8"},
            ]
        },
        "BOGON": {
            "values": [
                {"address": "192.0.0.0/24"},
                {"address": "192.0.2.0/24"},
            ]
        },
    }
}
services = {"services": {"SSH": [{"port": 22, "protocol": "tcp"}]}}
# --8<-- [end:data]


def main() -> None:
    # --8<-- [start:load]
    defs = naming.Naming()
    defs.ParseDefinitionsObject(networks, "inventory")
    defs.ParseDefinitionsObject(services, "services")
    # --8<-- [end:load]
    print([str(a) for a in defs.GetNet("MGMT")])
    print(sorted(defs.GetServiceNames()))


if __name__ == "__main__":
    main()
