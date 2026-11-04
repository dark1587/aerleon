# Includes

An include replaces one item in a `terms:` or `filters:` list with the contents of another file. Use includes to keep a block of terms, such as the bogon denies or a final default-deny, in one place and share it between policies. See the _[Policy File Spec](../reference/policy_files.md#includes)_ for the exact field rules.

The diagram colours each term by the file it came from. The policy `edge-inbound.yaml` lists one term and two includes. `aclgen` expands the includes in place, then renders the result once per target.

```mermaid
flowchart LR
    subgraph SRC [" "]
        direction TB
        P["edge-inbound.yaml<br/>- allow-ssh<br/>- include: includes/bogons.yaml<br/>- include: includes/default-deny.yaml"]:::policy
        B["includes/bogons.yaml<br/>- deny-reserved<br/>- deny-bogons"]:::incA
        D["includes/default-deny.yaml<br/>- default-deny"]:::incB
        P ~~~ B
        B ~~~ D
    end
    subgraph E ["edge-inbound (expanded)"]
        direction TB
        T1["1. allow-ssh"]:::policy
        T2["<b>2. deny-reserved</b>"]:::incA
        T3["<b>3. deny-bogons</b>"]:::incA
        T4["<b>4. default-deny</b>"]:::incB
        T1 ~~~ T2 ~~~ T3 ~~~ T4
    end
    O1["edge-inbound.acl"]:::out
    O2["edge-inbound.jcl"]:::out
    SRC -- aclgen --> E
    E --> O1
    E --> O2
    style SRC fill:none,stroke:none
    style E fill:#f7f7f7,stroke:#777
    --8<-- "docs/snippets/mermaid-classes.mmd"
```

All three examples below use the same definitions file.

??? note "def/definitions.yaml"

    ```yaml
    --8<-- "docs/examples/cli/includes-term/def/definitions.yaml"
    ```

The examples are real files that `aclgen` runs in the docs test suite, so the output shown is exactly what you get.

=== "Term includes"

    In a `terms:` list, the item `- include: <path>` is replaced, in place, by the `terms:` list of that file. The include files sit in `policies/includes/`, and the path is written relative to the base directory.

    ```yaml title="policies/pol/edge-inbound.yaml"
    --8<-- "docs/examples/cli/includes-term/policies/pol/edge-inbound.yaml"
    ```

    ```yaml title="policies/includes/bogons.yaml"
    --8<-- "docs/examples/cli/includes-term/policies/includes/bogons.yaml"
    ```

    ```yaml title="policies/includes/default-deny.yaml"
    --8<-- "docs/examples/cli/includes-term/policies/includes/default-deny.yaml"
    ```

    ??? example "Output"

        ```text title="edge-inbound.acl"
        --8<-- "docs/examples/cli/includes-term/expected/edge-inbound.acl"
        ```

        ```text title="edge-inbound.jcl"
        --8<-- "docs/examples/cli/includes-term/expected/edge-inbound.jcl"
        ```

=== "Filter includes"

    In a `filters:` list, `- include:` inserts the filters of another file. A file that holds only filters to be included starts with `filters_include_only:` instead of `filters:`. That key marks it as a filter library: it is never a policy on its own and produces no output by itself.

    ```yaml title="policies/includes/mgmt-filters.yaml"
    --8<-- "docs/examples/cli/includes-filter/policies/includes/mgmt-filters.yaml"
    ```

    ```yaml title="policies/pol/edge-inbound.yaml"
    --8<-- "docs/examples/cli/includes-filter/policies/pol/edge-inbound.yaml"
    ```

    The included filter comes first, so `mgmt-inbound` is rendered before `edge-inbound` in each output file.

    ```mermaid
    flowchart LR
        L["includes/mgmt-filters.yaml<br/>filters_include_only:<br/>- mgmt-inbound"]:::incA
        P["pol/edge-inbound.yaml<br/>- include: includes/mgmt-filters.yaml<br/>- edge-inbound"]:::policy
        subgraph F ["edge-inbound.yaml (expanded)"]
            direction TB
            F1["<b>1. mgmt-inbound</b>"]:::incA
            F2["2. edge-inbound"]:::policy
            F1 ~~~ F2
        end
        O1["edge-inbound.acl"]:::out
        O2["edge-inbound.jcl"]:::out
        X["(no output)"]:::neutral
        L -.->|included| P
        P --> F
        F --> O1
        F --> O2
        L -. not rendered by itself .-> X
        style F fill:#f7f7f7,stroke:#777
        --8<-- "docs/snippets/mermaid-classes.mmd"
    ```

    ??? example "Output"

        ```text title="edge-inbound.acl"
        --8<-- "docs/examples/cli/includes-filter/expected/edge-inbound.acl"
        ```

        ```text title="edge-inbound.jcl"
        --8<-- "docs/examples/cli/includes-filter/expected/edge-inbound.jcl"
        ```

=== "Nested includes"

    An included file can include other files. Here `includes/bogons.yaml` includes `includes/reserved.yaml`. The output is identical to the Term includes tab. The nested path is still written relative to the base directory, not to the file that contains it.

    ```yaml title="policies/includes/bogons.yaml"
    --8<-- "docs/examples/cli/includes-nested/policies/includes/bogons.yaml"
    ```

    ```yaml title="policies/includes/reserved.yaml"
    --8<-- "docs/examples/cli/includes-nested/policies/includes/reserved.yaml"
    ```

    ??? example "Output"

        ```text title="edge-inbound.acl"
        --8<-- "docs/examples/cli/includes-nested/expected/edge-inbound.acl"
        ```

        ```text title="edge-inbound.jcl"
        --8<-- "docs/examples/cli/includes-nested/expected/edge-inbound.jcl"
        ```

## Rules

- The include path is relative to the base directory (`--base_directory`, default `./policies`), not to the file that contains the include. A nested include writes `includes/x.yaml` as well.
- The file name must end in `.yaml` or `.yml`. Anything else stops `aclgen` with `Policy include source includes/bogons.txt must end in ".yaml" or ".yml". File=policies/pol/edge.yaml, Line=11.`
- The file must be inside the base directory. Otherwise `aclgen` reports `Include file cannot be loaded from outside the base directory. File=policies/../outside.yaml base_directory=policies`.
- Give an include item no other keys: `aclgen` drops them without a warning, and the JSON Schema reports them as an error.
- Includes can be nested 5 deep. A chain of 5 include files works. A 6th stops `aclgen` with this message and a list of the files involved:

    ```text
    Excessive recursion: include depth limit of 5 reached. File=policies/includes/c5.yaml, Line=2.
    Include stack:
    > File='policies/pol/edge-inbound.yaml', Line=14 (Top Level)
    > File='policies/includes/c1.yaml', Line=2
    > File='policies/includes/c2.yaml', Line=2
    > File='policies/includes/c3.yaml', Line=2
    > File='policies/includes/c4.yaml', Line=2
    > File='policies/includes/c5.yaml', Line=2
    ```

- An empty include file is skipped with a warning, and the output is still written: `Ignoring empty policy include source. File=policies/includes/empty.yaml.`
- A missing include file stops `aclgen`: `[Errno 2] No such file or directory: 'policies/includes/nope.yaml'`.

!!! warning "Keep include files out of pol directories"

    `aclgen` treats every YAML file under a `pol` directory as a policy. A file that holds only `terms:` or `filters_include_only:` is not a policy, and when it sits in `pol/` the run stops with `AttributeError: 'NoneType' object has no attribute 'headers'`. Put include files in a separate directory, such as `policies/includes/` as every example here does.

## Patterns

### Shared bogon denies

Put the terms that deny reserved and bogon ranges in `includes/bogons.yaml`, and include that file from every policy that faces an untrusted network. Fixing a range in one place fixes it in every policy. See the Term includes tab.

### A common default-deny

Put the closing `default-deny` term in `includes/default-deny.yaml` and include it last. Every policy then ends the same way. See the Term includes tab.

### A shared filter library

Put filters that several policies need, such as a management-access filter, in `includes/mgmt-filters.yaml` under `filters_include_only:`, and include the file from each policy's `filters:` list. See the Filter includes tab.

## Legacy .pol files

Policies written in the older `.pol` format include other files with `#include 'file.inc'`, and the included file must end in `.inc`. The two formats cannot include each other: YAML policies include only `.yaml` or `.yml` files, and `.pol` policies include only `.inc` files. To move a `.pol` policy to YAML, see _[pol2yaml](cli/pol2yaml.md)_.

## Includes in the API

When you build policies from Python, pass `include_path` (a directory to read include files from) or `includes` (a dictionary mapping include names to policy dictionaries) to `Generate`. The two are mutually exclusive, and passing both raises `TypeError("include_path and includes are mutually exclusive.")`. See _[API Overview](../api/index.md)_.
