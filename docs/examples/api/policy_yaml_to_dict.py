"""Show that a YAML policy file and a PolicyDict are the same data."""

import yaml

from aerleon import api
from aerleon.lib import naming
from aerleon.lib.policy_builder import PolicyDict

# --8<-- [start:dict]
EDGE_INBOUND: PolicyDict = {
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
# --8<-- [end:dict]

DEFINITIONS = {
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


def main() -> None:
    with open("policies/edge-inbound.yaml") as f:
        loaded = yaml.safe_load(f)
    print("YAML == dict:", loaded == EDGE_INBOUND)

    definitions = naming.Naming()
    definitions.ParseDefinitionsObject(DEFINITIONS, "definitions")
    configs = api.Generate([{**loaded, "filename": "edge-inbound.yaml"}], definitions)
    print(sorted(configs))


if __name__ == "__main__":
    main()
