"""Check how a policy treats one packet with AclCheck."""

from aerleon import api
from aerleon.lib import naming

# --8<-- [start:policy]
example_policy = {
    "filename": "my_api_policy_check",
    "filters": [
        {
            "header": {
                "targets": {"cisco": "test-filter"},
                "comment": "Sample filter for AclCheck API demo",
            },
            "terms": [
                {
                    "name": "allow-web-traffic",
                    "source-address": "INTERNAL_NETWORK",
                    "destination-address": "WEB_SERVERS",
                    "destination-port": "HTTP",
                    "protocol": "tcp",
                    "action": "accept",
                },
                {"name": "deny-all-else", "action": "deny"},
            ],
        }
    ],
}

definitions_data = {
    "networks": {
        "INTERNAL_NETWORK": {"values": [{"address": "192.168.1.0/24"}]},
        "WEB_SERVERS": {"values": [{"address": "10.0.0.10/32"}, {"address": "10.0.0.11/32"}]},
    },
    "services": {"HTTP": [{"protocol": "tcp", "port": "80"}]},
}
# --8<-- [end:policy]


def main() -> None:
    defs = naming.Naming()
    defs.ParseDefinitionsObject(definitions_data, "definitions_data")

    # --8<-- [start:check]
    source_ip = "192.168.1.0/24"
    destination_ip = "10.0.0.10"
    protocol = "tcp"
    destination_port = "80"
    source_port = "49152"

    summary = api.AclCheck(
        input_policy=example_policy,
        definitions=defs,
        src=source_ip,
        dst=destination_ip,
        sport=source_port,
        dport=destination_port,
        proto=protocol,
    )

    if summary:
        for filter_name, terms in summary.items():
            print(f"  Filter: {filter_name}")
            for term_name, match_details in terms.items():
                print(match_details["message"])
    else:
        print(
            f"No matching terms found for traffic from {source_ip}:{source_port} "
            f"to {destination_ip}:{destination_port} ({protocol})."
        )
    # --8<-- [end:check]


if __name__ == "__main__":
    main()
