"""Per-target options: Cisco mixed and Juniper inet, not interface-specific."""

from aerleon import api
from aerleon.lib import naming

# --8<-- [start:policy]
edge_inbound = {
    "filename": "edge-inbound",
    "filters": [
        {
            "header": {
                "targets": {
                    "cisco": "edge-inbound mixed",
                    "juniper": "edge-inbound inet not-interface-specific",
                },
            },
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
# --8<-- [end:policy]


def main() -> None:
    definitions = naming.Naming("def")
    configs = api.Generate([edge_inbound], definitions)
    print(sorted(configs))
    for name in sorted(configs):
        print(f"=== {name} ===")
        print(configs[name])


if __name__ == "__main__":
    main()
