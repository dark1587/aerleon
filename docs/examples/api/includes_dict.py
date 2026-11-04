"""Include terms from a dictionary with includes."""

from aerleon import api
from aerleon.lib import naming
from aerleon.lib.policy_builder import PolicyFilterTermsOnly

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

# --8<-- [start:bogons]
BOGONS: PolicyFilterTermsOnly = {
    "terms": [
        {"name": "deny-reserved", "destination-address": "RESERVED", "action": "deny"},
        {"name": "deny-bogons", "destination-address": "BOGON", "action": "deny"},
    ]
}
# --8<-- [end:bogons]


def main() -> None:
    definitions = naming.Naming("def")
    # --8<-- [start:generate]
    configs = api.Generate([edge_inbound], definitions, includes={"bogons.yaml": BOGONS})
    # --8<-- [end:generate]
    print(configs["edge-inbound.acl"])


if __name__ == "__main__":
    main()
