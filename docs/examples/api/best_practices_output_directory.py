"""Write the generated files into a directory instead of returning them."""

import pathlib
import tempfile

from aerleon import api
from aerleon.lib import naming

# --8<-- [start:policy]
edge_inbound = {
    "filename": "edge-inbound",
    "filters": [
        {
            "header": {
                "targets": {"cisco": "edge-inbound", "juniper": "edge-inbound inet"},
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
    # --8<-- [start:write]
    with tempfile.TemporaryDirectory() as tmp:
        result = api.Generate([edge_inbound], definitions, output_directory=pathlib.Path(tmp))
        print(result)
        print(sorted(p.name for p in pathlib.Path(tmp).iterdir()))
    # --8<-- [end:write]


if __name__ == "__main__":
    main()
