# Multi-Platform Headers

One policy can generate ACLs for several platforms at once. The `targets` dictionary in a filter header maps each platform name to a target value, and `Generate()` renders one output file for each entry. The exception is `pcap`, which writes two files, such as `p-accept.pcap` and `p-deny.pcap`. This page shows how to use one filter for several platforms, how to pass options to each platform, and when to use separate filters instead. For the header fields, see _[Policy File Spec](../reference/policy_files.md)_.

Examples run from `docs/examples/api/`, because they load definitions with the relative path `def/`. Run them from that directory if you try them yourself.

```mermaid
flowchart LR
    POL["policy dict edge-inbound"]:::policy
    FILTER["filter"]:::policy
    CISCO["cisco"]:::neutral
    JUNIPER["juniper"]:::neutral
    ACL["edge-inbound.acl"]:::out
    JCL["edge-inbound.jcl"]:::out
    POL --> FILTER
    FILTER --> CISCO
    FILTER --> JUNIPER
    CISCO --> ACL
    JUNIPER --> JCL
    --8<-- "docs/snippets/mermaid-classes.mmd"
```

## One filter, many targets

Give the header one entry in `targets` for each platform. The terms are written once and rendered for every platform. Each example prints the sorted file names first, then every file under `=== <name> ===`.

```python title="multi_platform_one_filter.py"
--8<-- "docs/examples/api/multi_platform_one_filter.py"
```

??? example "Output"

    ```text title="multi_platform_one_filter.stdout.ref"
    --8<-- "docs/examples/api/multi_platform_one_filter.stdout.ref"
    ```

The policy's `filename` is `edge-inbound`, and each platform adds its own suffix: `.acl` for Cisco and `.jcl` for Juniper.

## Per-target options

The value of a target is a string of the form `<filter-name> <options>`. The first word is the filter name. Everything after it is a list of options for that platform, and each platform defines its own. The Header Format section of each platform's page in _[Generators](../reference/generators.md)_ lists them.

Here _[Cisco](../reference/generators/cisco.md)_ gets `mixed`, which renders both an IPv4 and an IPv6 access list in the same file. _[Juniper](../reference/generators/juniper.md)_ gets `inet not-interface-specific`, which renders an IPv4 filter and leaves out the `interface-specific` statement.

```python title="multi_platform_options.py"
--8<-- "docs/examples/api/multi_platform_options.py"
```

??? example "Output"

    ```text title="multi_platform_options.stdout.ref"
    --8<-- "docs/examples/api/multi_platform_options.stdout.ref"
    ```

The Cisco file now ends with an IPv6 access list that holds only the `default-deny` term, because `allow-ssh` has IPv4 addresses only.

Cisco's `object-group` option is a poor fit here. Aerleon renders duplicate permit lines for it today, so check the output before you use it.

## Separate filters per platform

When the terms differ by platform, use one filter for each target. Both filters belong to the same policy dictionary, and each has its own `targets` and `terms`. Here Juniper counts the SSH traffic and Cisco does not, and the Cisco filter leaves out the `counter` keyword.

```python title="multi_platform_split_filters.py"
--8<-- "docs/examples/api/multi_platform_split_filters.py"
```

??? example "Output"

    ```text title="multi_platform_split_filters.stdout.ref"
    --8<-- "docs/examples/api/multi_platform_split_filters.stdout.ref"
    ```

The output file names still come from `filename`, so the result has the same two files as before.

The YAML equivalent of these policies is taught on _[Writing Policies](../usage/writing_policies.md)_.
