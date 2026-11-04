"""Include terms from a YAML file with include_path."""

from aerleon import api
from aerleon.lib import naming

# --8<-- [start:policy]
edge_inbound = {
    "filename": "edge-inbound",
    "filters": [
        {
            "header": {"targets": {"cisco": "edge-inbound"}},
            "terms": [
                {"include": "bogons.yaml"},
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
    # --8<-- [start:generate]
    configs = api.Generate([edge_inbound], definitions, include_path="policies/includes")
    # --8<-- [end:generate]
    print(configs["edge-inbound.acl"])


if __name__ == "__main__":
    main()
