"""Generate Cisco and Juniper ACLs for edge-inbound from Python dicts."""

from aerleon import api
from aerleon.lib import naming

# --8<-- [start:policy]
edge_inbound = {
    "filename": "edge-inbound",
    "filters": [
        {
            "header": {"targets": {"cisco": "edge-inbound"}},
            "terms": [
                {
                    "name": "allow-ssh",
                    "comment": "Allow SSH from the management network.",
                    "source-address": "MGMT",
                    "protocol": "tcp",
                    "destination-port": "SSH",
                    "action": "accept",
                },
                {"name": "default-deny", "action": "deny"},
            ],
        }
    ],
}

definitions_dict = {
    "networks": {
        "MGMT": {
            "values": [
                {"address": "10.0.0.0/24"},
                {"address": "192.168.10.0/24"},
            ]
        }
    },
    "services": {"SSH": [{"port": 22, "protocol": "tcp"}]},
}
# --8<-- [end:policy]


def main() -> None:
    # --8<-- [start:generate]
    definitions = naming.Naming()
    definitions.ParseDefinitionsObject(definitions_dict, "definitions")
    configs = api.Generate([edge_inbound], definitions)
    # --8<-- [end:generate]
    print(sorted(configs))
    print(configs["edge-inbound.acl"])


if __name__ == "__main__":
    main()
