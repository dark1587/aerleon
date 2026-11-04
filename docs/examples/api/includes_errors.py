"""Include errors and the silent failure for a mistyped dictionary key."""

from aerleon import api
from aerleon.lib import naming

BOGONS = {
    "terms": [
        {"name": "deny-reserved", "destination-address": "RESERVED", "action": "deny"},
        {"name": "deny-bogons", "destination-address": "BOGON", "action": "deny"},
    ]
}


def make_policy(include: str) -> dict:
    return {
        "filename": "edge-inbound",
        "filters": [
            {
                "header": {"targets": {"cisco": "edge-inbound"}},
                "terms": [
                    {"include": include},
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


def main() -> None:
    definitions = naming.Naming("def")

    print("--- both arguments ---")
    # --8<-- [start:both]
    try:
        api.Generate(
            [make_policy("bogons.yaml")],
            definitions,
            include_path="policies/includes",
            includes={"bogons.yaml": BOGONS},
        )
    except TypeError as e:
        print(f"{type(e).__name__}: {e}")
    # --8<-- [end:both]

    print("--- mistyped dictionary key ---")
    # --8<-- [start:typo]
    configs = api.Generate(
        [make_policy("bogons.yaml")], definitions, includes={"bogon.yaml": BOGONS}
    )
    for line in configs["edge-inbound.acl"].splitlines():
        if "remark" in line:
            print(line.strip())
    # --8<-- [end:typo]

    print("--- missing suffix ---")
    # --8<-- [start:suffix]
    try:
        api.Generate([make_policy("bogons")], definitions, include_path="policies/includes")
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
    # --8<-- [end:suffix]

    print("--- path outside include_path ---")
    # --8<-- [start:outside]
    try:
        api.Generate(
            [make_policy("../edge-inbound.yaml")],
            definitions,
            include_path="policies/includes",
        )
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
    # --8<-- [end:outside]


if __name__ == "__main__":
    main()
