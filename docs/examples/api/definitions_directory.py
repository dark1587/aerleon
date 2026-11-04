"""Load every definitions file in a directory."""

from aerleon.lib import naming


def main() -> None:
    # --8<-- [start:load]
    defs = naming.Naming("def")
    # --8<-- [end:load]
    print([str(a) for a in defs.GetNet("MGMT")])
    print(sorted(defs.GetServiceNames()))


if __name__ == "__main__":
    main()
