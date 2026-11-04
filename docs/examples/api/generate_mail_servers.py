"""Build a policy from variable data: two sets of mail server addresses."""

from aerleon import api
from aerleon.lib import naming

cisco_example_policy = {
    "filename": "cisco_example_policy",
    "filters": [
        {
            "header": {
                "targets": {"cisco": "test-filter"},
                "comment": "Sample comment",
            },
            "terms": [
                {
                    "name": "deny-to-reserved",
                    "destination-address": "RESERVED",
                    "action": "deny",
                },
                {
                    "name": "deny-to-bogons",
                    "destination-address": "BOGON",
                    "action": "deny",
                },
                {
                    "name": "allow-web-to-mail",
                    "destination-address": "MAIL_SERVERS",
                    "action": "accept",
                },
            ],
        }
    ],
}

mail_server_sets = [
    ["200.1.1.4/32", "200.1.1.5/32"],
    ["200.1.2.4/32", "200.1.2.5/32"],
]


def build_definitions(mail_servers: list[str]) -> naming.Naming:
    networks = {
        "networks": {
            "RESERVED": {
                "values": [{"address": "0.0.0.0/8"}, {"address": "10.0.0.0/8"}]
            },
            "BOGON": {
                "values": [{"address": "192.0.0.0/24"}, {"address": "192.0.2.0/24"}]
            },
            "MAIL_SERVERS": {"values": [{"address": ip} for ip in mail_servers]},
        }
    }
    definitions = naming.Naming()
    definitions.ParseDefinitionsObject(networks, "definitions")
    return definitions


def main() -> None:
    for number, mail_servers in enumerate(mail_server_sets):
        definitions = build_definitions(mail_servers)
        configs = api.Generate([cisco_example_policy], definitions)
        print(f"=== mail server set {number} ===")
        print(configs["cisco_example_policy.acl"])


if __name__ == "__main__":
    main()
