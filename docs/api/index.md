# API Overview

Aerleon has two Python entry points, `Generate()` and `AclCheck()`. Both take plain Python dictionaries and lists, so you don't need any YAML files. `Generate()` does what `aclgen` does: it turns a list of policies and a set of definitions into platform-specific ACLs. `AclCheck()` does what `aclcheck` does: it tells you how a policy treats a packet.

Use the API when your policies depend on data that lives somewhere else, such as an inventory, a CSV file or NetBox, or when you want ACLs as strings in your own program instead of files on disk.

## How data flows

```mermaid
flowchart LR
    DATA["Your data (inventory, CSV, NetBox…)"]:::neutral
    POL["policy dicts (PolicyDict)"]:::policy
    DEFS["definitions dicts"]:::policy
    NAMING["Naming"]:::policy
    GEN["Generate()"]:::neutral
    ACL["edge-inbound.acl"]:::out
    JCL["edge-inbound.jcl"]:::out
    DISK["files on disk"]:::out
    DATA --> POL
    DATA --> DEFS
    DEFS --> NAMING
    POL --> GEN
    NAMING --> GEN
    GEN --> ACL
    GEN --> JCL
    GEN -. output_directory .-> DISK
    --8<-- "docs/snippets/mermaid-classes.mmd"
```

A policy with both Cisco and Juniper targets returns the `.jcl` file as well as the `.acl` file; the Quick start below uses Cisco only.

You build the policy dictionaries and the definitions yourself. Definitions go into a `Naming` object. `Generate()` returns a dictionary that maps each output file name to its text. If you pass `output_directory`, it writes the files there instead.

## Quick start

This generates a Cisco ACL for the running `edge-inbound` policy. The policy is a dictionary with the same structure as a YAML policy file. The definitions are a second dictionary that follows the YAML definitions format.

```python title="Policy and definitions"
--8<-- "docs/examples/api/generate_edge_inbound.py:policy"
```

Load the definitions into a `Naming` object and pass both to `Generate()`.

```python title="Generate"
--8<-- "docs/examples/api/generate_edge_inbound.py:generate"
```

The result is keyed by output file name. The policy `filename` and the generator's suffix form the name, so `edge-inbound` with a Cisco target produces `edge-inbound.acl`.

Examples run from `docs/examples/api/`. The complete module is `generate_edge_inbound.py` in that directory.

??? example "Output"

    ```text title="generate_edge_inbound.stdout.ref"
    --8<-- "docs/examples/api/generate_edge_inbound.stdout.ref"
    ```

## Policies from variable data

Because the policy and the definitions are Python objects, you can compute them. This example builds the definitions for two alternative sets of mail server addresses and generates one ACL for each. It uses a fresh `Naming` object for every set, because a token can only be defined once in a `Naming`.

```python title="generate_mail_servers.py"
--8<-- "docs/examples/api/generate_mail_servers.py"
```

??? example "Output"

    ```text title="generate_mail_servers.stdout.ref"
    --8<-- "docs/examples/api/generate_mail_servers.stdout.ref"
    ```

## API vs aclgen

`Generate()` renders the same policies as `aclgen`. What differs is where data comes from and where results go.

| | `aclgen` | `Generate()` |
|---|---|---|
| Input | YAML and `.pol` files found under `--base_directory` | A list of `PolicyDict` dictionaries |
| Definitions | Files under `--definitions_directory` | A `Naming` object that you build |
| Includes | Resolved relative to `--base_directory` | Resolved from `include_path`, or taken from the `includes` dictionary |
| Output | Files in `--output_directory` | A returned dictionary of file name to text, or files when you pass `output_directory` as a `Path` |
| Options | `--optimize`, `--shade_check`, `--exp_info` | `optimize`, `shade_check`, `expiration_weeks` |
| Config file | `aerleon.yml`, or `--config_file` | None |
| Parallelism | `--max_renderers` | A single process |

Choose `aclgen` when your policies are files in a repository and you want a command to run. Choose the API when your program builds the policies, or needs the output in memory. See _[aclgen](../usage/cli/aclgen.md)_ for the command line.

## Next

- _[Policy Objects](policy_objects.md)_: the shape of a `PolicyDict`.
- _[Definitions (Naming)](definitions.md)_: build a `Naming` from files or dictionaries.
- _[Multi-Platform Headers](multi_platform_headers.md)_: several targets and options in one filter.
- _[Includes in the API](includes.md)_: share terms with `include_path` or `includes`.
- Best Practices: validate input and choose an output mode.
- AclCheck API: decide how a policy treats a packet.
- _[Includes](../usage/includes.md)_: the same feature for YAML files.
