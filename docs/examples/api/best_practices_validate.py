"""Validate definitions and output names before generating, and wrap errors."""

from pathlib import Path

from aerleon import api
from aerleon.aclgen import ACLGeneratorError, ACLParserError
from aerleon.lib import naming
from aerleon.lib.policy_builder import PolicyDict


# --8<-- [start:checks]
def check_definitions(defs: naming.Naming) -> None:
    """Fail if a nested name in the definitions is not defined anywhere."""
    if defs.unseen_networks or defs.unseen_services:
        raise ValueError(
            f"undefined names: networks={defs.unseen_networks} services={defs.unseen_services}"
        )


def check_output_names(policies: list[PolicyDict]) -> None:
    """Fail if two policies share a filename stem, so one output would replace the other."""
    seen: set[str] = set()
    for policy in policies:
        stem = Path(policy.get("filename", "<unknown>")).stem
        if stem in seen:
            raise ValueError(f"duplicate output name: {stem}")
        seen.add(stem)


def generate(policies: list[PolicyDict], defs: naming.Naming) -> dict[str, str]:
    """Validate, generate, and report parser and generator errors as RuntimeError."""
    check_definitions(defs)
    check_output_names(policies)
    try:
        return dict(api.Generate(policies, defs))
    except (ACLParserError, ACLGeneratorError) as e:
        raise RuntimeError(str(e).splitlines()[0]) from e


# --8<-- [end:checks]


def make_policy(filename: str, source: str = "MGMT") -> PolicyDict:
    return {
        "filename": filename,
        "filters": [
            {
                "header": {"targets": {"cisco": "edge-inbound"}},
                "terms": [
                    {
                        "name": "allow-ssh",
                        "comment": "Allow SSH from the management network.",
                        "source-address": source,
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
    defs = naming.Naming("def")

    print("--- a good policy ---")
    print(sorted(generate([make_policy("edge-inbound")], defs)))

    print("--- undefined names in the definitions ---")
    try:
        generate([make_policy("edge-inbound")], naming.Naming("def_unseen", "networks.yaml"))
    except ValueError as e:
        print(f"ValueError: {e}")

    print("--- two policies with the same output name ---")
    try:
        generate([make_policy("edge-inbound"), make_policy("pol/edge-inbound")], defs)
    except ValueError as e:
        print(f"ValueError: {e}")

    print("--- a policy that uses an undefined name ---")
    try:
        generate([make_policy("bad-policy", source="NOPE")], defs)
    except RuntimeError as e:
        print(f"RuntimeError: {e}")


if __name__ == "__main__":
    main()
