"""Turn an AclCheck summary into one outcome per packet."""

from aerleon import api
from aerleon.lib import naming

# --8<-- [start:policy]
edge_inbound = {
    "filename": "edge-inbound",
    "filters": [
        {
            "header": {
                "targets": {"cisco": "edge-inbound", "juniper": "edge-in-j"},
            },
            "terms": [
                {
                    "name": "allow-established",
                    "protocol": "tcp",
                    "option": "tcp-established",
                    "action": "accept",
                },
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

definitions_data = {
    "networks": {
        "MGMT": {"values": [{"address": "10.0.0.0/24"}, {"address": "192.168.10.0/24"}]},
    },
    "services": {"SSH": [{"protocol": "tcp", "port": "22"}]},
}
# --8<-- [end:policy]


# --8<-- [start:outcome]
def outcome(summary, policy) -> str:
    """Describe what happens to the packet: the last exact match, plus earlier possible ones.

    The summary has no action field, so each term's action is looked up by name in the policy.
    """
    actions = {
        term["name"]: term["action"]
        for policy_filter in policy["filters"]
        for term in policy_filter["terms"]
        if "name" in term
    }
    conditions = []
    final = "no exact match"
    for terms in summary.values():
        for name, details in terms.items():
            if details["possibles"]:
                conditions.append(f"{actions[name]} if {details['possibles']}")
            else:
                final = actions[name]
    return "; ".join(conditions + [final])


# --8<-- [end:outcome]


def main() -> None:
    defs = naming.Naming()
    defs.ParseDefinitionsObject(definitions_data, "definitions_data")

    queries = [
        dict(src="10.0.0.5", dst="203.0.113.10", sport=40000, dport=22, proto="tcp"),
        dict(src="198.51.100.1", dport=22, proto="tcp"),
    ]
    # --8<-- [start:run]
    for query in queries:
        summary = api.AclCheck(edge_inbound, defs, **query)
        print(query)
        print({k: dict(v) for k, v in summary.items()})
        print(outcome(summary, edge_inbound))
    # --8<-- [end:run]

    try:
        api.AclCheck(edge_inbound, defs, dport="SSH")
    except Exception as e:
        print(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
