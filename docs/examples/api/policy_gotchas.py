"""Policy dictionary gotchas: file names, typos and list or string values."""

from aerleon import api
from aerleon.lib import naming

DEFINITIONS = {
    "networks": {
        "MGMT": {
            "values": [
                {"address": "10.0.0.0/24"},
                {"address": "192.168.10.0/24"},
            ]
        },
        "BOGON": {
            "values": [
                {"address": "192.0.0.0/24"},
                {"address": "192.0.2.0/24"},
            ]
        },
    },
    "services": {"SSH": [{"port": 22, "protocol": "tcp"}]},
}


def make_naming() -> naming.Naming:
    definitions = naming.Naming()
    definitions.ParseDefinitionsObject(DEFINITIONS, "definitions")
    return definitions


def make_policy(target: str = "edge-inbound", **term_overrides) -> dict:
    allow_ssh = {
        "name": "allow-ssh",
        "source-address": "MGMT",
        "protocol": "tcp",
        "destination-port": "SSH",
        "action": "accept",
    }
    allow_ssh.update(term_overrides)
    return {
        "filters": [
            {
                "header": {"targets": {"cisco": target}},
                "terms": [allow_ssh, {"name": "default-deny", "action": "deny"}],
            }
        ]
    }


def main() -> None:
    print("--- no filename ---")
    configs = api.Generate([make_policy()], make_naming())
    print(sorted(configs))

    print("--- filename with a directory ---")
    policy = {**make_policy(), "filename": "pol/edge-inbound"}
    configs = api.Generate([policy], make_naming())
    print(sorted(configs))

    print("--- same filename twice ---")
    first = {**make_policy("first"), "filename": "edge-inbound"}
    second = {**make_policy("second"), "filename": "edge-inbound"}
    configs = api.Generate([first, second], make_naming())
    print(len(configs))
    print("extended second" in configs["edge-inbound.acl"])

    print("--- misspelled key ---")
    # "destination_address" should be "destination-address".
    policy = {
        "filename": "typo",
        "filters": [
            {
                "header": {"targets": {"cisco": "typo"}},
                "terms": [
                    {
                        "name": "allow-to-mgmt",
                        "destination_address": "MGMT",
                        "action": "accept",
                    }
                ],
            }
        ],
    }
    configs = api.Generate([policy], make_naming())
    for line in configs["typo.acl"].splitlines():
        if "permit" in line:
            print(line)

    print("--- list or string ---")
    as_list = {**make_policy(**{"source-address": ["MGMT", "BOGON"]}), "filename": "same"}
    as_string = {**make_policy(**{"source-address": "MGMT BOGON"}), "filename": "same"}
    acl_list = api.Generate([as_list], make_naming())["same.acl"]
    acl_string = api.Generate([as_string], make_naming())["same.acl"]
    print(acl_list == acl_string)


if __name__ == "__main__":
    main()
