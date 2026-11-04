# Usage Overview

`aclgen` reads definition files and policy files from a project directory and writes one ACL file per policy and target, such as `edge-inbound.acl` for Cisco and `edge-inbound.jcl` for Juniper. This page shows how a project is laid out and how `aclgen` finds its files and chooses where to write output.

```
project/
  aerleon.yml                  (optional)
  def/
    definitions.yaml
  policies/
    includes/
      bogons.yaml
    pol/
      edge-inbound.yaml
```

```mermaid
flowchart LR
    subgraph PROJ ["project/"]
        direction TB
        CFG["aerleon.yml (optional)"]:::neutral
        DEF["def/<br/>*.yaml *.yml"]:::neutral
        POL["policies/pol/<br/>edge-inbound.yaml"]:::policy
        INC["policies/includes/<br/>bogons.yaml"]:::incA
        INC -. include .-> POL
    end
    O1["edge-inbound.acl"]:::out
    O2["edge-inbound.jcl"]:::out
    PROJ -- aclgen --> O1
    PROJ -- aclgen --> O2
    style PROJ fill:#f7f7f7,stroke:#777
    --8<-- "docs/snippets/mermaid-classes.mmd"
```

## How aclgen finds files

By default `aclgen` reads policies from `./policies` and definitions from `./def`, relative to the directory you run it in. A config file named `aerleon.yml` in the current directory, or command line flags, change these locations. See _[Command Line Usage](cli/index.md)_ for the options and _[aclgen](cli/aclgen.md)_ for the full flag list.

`aclgen` renders the `*.pol`, `*.yaml` and `*.yml` files found directly inside every directory named `pol` under the policies directory. Files in subdirectories of a `pol` directory aren't rendered. The `ignore_directories` option skips `DEPRECATED` and `def` by default.

`aclgen` reads every `.yaml`, `.yml`, `.net` or `.svc` file directly in the definitions directory. Subdirectories aren't read.

## Where output goes

Each output file is written to the output directory, then the path of the `pol` directory's parent relative to the policies directory, then the policy file name without its extension plus the generator's suffix. The output directory is `./` unless you set `--output_directory`. For example, `policies/site-a/pol/core.yaml` becomes `out/site-a/core.acl` for the Cisco target and `out/site-a/core.jcl` for the Juniper target. See _[Generators](../reference/generators.md)_ for each platform's suffix.

## Include files

Include files live outside `pol/`, so `aclgen` doesn't render them as policies of their own. A policy refers to them with `include:`, as `bogons.yaml` does in the diagram. See _[Includes](includes.md#rules)_.

## Next

_[Writing Policies](writing_policies.md)_: write the filters and terms.

_[Writing Definitions](writing_definitions.md)_: name the networks and services your terms use.

_[Includes](includes.md)_: share terms and filters between policies.

_[Command Line Usage](cli/index.md)_: run `aclgen` and the other programs.
