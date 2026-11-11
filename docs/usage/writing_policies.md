# Writing Policies

A policy file holds a list of `filters`. Each filter is a `header` plus `terms`: the header names the `targets` (the platforms to render for, each with its options), and the terms are the rules. See the _[Policy File Spec](../reference/policy_files.md)_ for every field, and the _[Usage Overview](index.md)_ for where policy files go.

The examples below are real files that `aclgen` runs in the docs test suite, so the output shown is exactly what you get.

=== "Single platform"

    One target, one output file. The output is named after the policy file (`edge-inbound.yaml`) plus the generator's suffix, here `.acl` for Cisco. See the File suffix column in the _[Generators Overview](../reference/generators.md#generators)_ for each generator's suffix. This tab also shows the definitions file the policy refers to.

    ```yaml title="def/definitions.yaml"
    --8<-- "docs/examples/cli/policy-single/def/definitions.yaml"
    ```

    ```yaml title="policies/pol/edge-inbound.yaml"
    --8<-- "docs/examples/cli/policy-single/policies/pol/edge-inbound.yaml"
    ```

    ??? example "Output"

        ```text title="edge-inbound.acl"
        --8<-- "docs/examples/cli/policy-single/expected/edge-inbound.acl"
        ```

=== "Two platforms"

    A second entry under `targets:` renders the same terms for another platform, giving one output file per target for most generators: `.acl` for Cisco and `.jcl` for Juniper. (Some generators write more than one file; `pcap`, for example, writes a separate accept and deny file.) Each target line is the generator name followed by that generator's options.

    ```yaml title="policies/pol/edge-inbound.yaml"
    --8<-- "docs/examples/cli/policy-two-platforms/policies/pol/edge-inbound.yaml"
    ```

    ??? example "Output"

        ```text title="edge-inbound.acl"
        --8<-- "docs/examples/cli/policy-two-platforms/expected/edge-inbound.acl"
        ```

        ```text title="edge-inbound.jcl"
        --8<-- "docs/examples/cli/policy-two-platforms/expected/edge-inbound.jcl"
        ```

=== "Per-platform options"

    Options on a target line belong to that target alone. Here `noverbose` on the Juniper target drops the term comment from the `.jcl` file only; the `.acl` file still carries it. See the _[Juniper](../reference/generators/juniper.md)_ and _[Cisco](../reference/generators/cisco.md)_ pages for the options each generator accepts.

    ```yaml title="policies/pol/edge-inbound.yaml"
    --8<-- "docs/examples/cli/policy-platform-options/policies/pol/edge-inbound.yaml"
    ```

    ??? example "Output"

        ```text title="edge-inbound.acl"
        --8<-- "docs/examples/cli/policy-platform-options/expected/edge-inbound.acl"
        ```

        ```text title="edge-inbound.jcl"
        --8<-- "docs/examples/cli/policy-platform-options/expected/edge-inbound.jcl"
        ```

=== "Separate filters"

    A file can hold several filters, each with its own header and terms. A platform's output file contains only the filters that list that platform: `edge-outbound` lists Cisco only, so it appears in the `.acl` file and not in the `.jcl` file.

    ```yaml title="policies/pol/edge-inbound.yaml"
    --8<-- "docs/examples/cli/policy-separate-filters/policies/pol/edge-inbound.yaml"
    ```

    ??? example "Output"

        ```text title="edge-inbound.acl"
        --8<-- "docs/examples/cli/policy-separate-filters/expected/edge-inbound.acl"
        ```

        ```text title="edge-inbound.jcl"
        --8<-- "docs/examples/cli/policy-separate-filters/expected/edge-inbound.jcl"
        ```

## Services with more than one protocol

A service such as `DNS` can span several protocols (port 53 over both `udp` and `tcp`). The term's `protocol` field decides which of the service's ports are used, so list the protocols you mean.

=== "Both protocols"

    `protocol: [tcp, udp]` keeps both of `DNS`'s ports. Cisco gets one line per protocol and Juniper gets one term with both protocols. The second filter shows the risk: with `protocol: udp` the term still reads as "allow DNS", but TCP 53 is dropped from the output, with no warning.

    ```yaml title="def/definitions.yaml"
    --8<-- "docs/examples/cli/multi-protocol-dns/def/definitions.yaml"
    ```

    ```yaml title="policies/pol/dns-policy.yaml"
    --8<-- "docs/examples/cli/multi-protocol-dns/policies/pol/dns-policy.yaml"
    ```

    ??? example "Output"

        ```text title="dns-policy.acl"
        --8<-- "docs/examples/cli/multi-protocol-dns/expected/dns-policy.acl"
        ```

        ```text title="dns-policy.jcl"
        --8<-- "docs/examples/cli/multi-protocol-dns/expected/dns-policy.jcl"
        ```

=== "GRE and HTTPS"

    GRE has no ports, so it can't share a term with a service that has them. Put `gre` in one term and `tcp` with `HTTPS` in another.

    ```yaml title="def/definitions.yaml"
    --8<-- "docs/examples/cli/multi-protocol-gre/def/definitions.yaml"
    ```

    ```yaml title="policies/pol/gre-policy.yaml"
    --8<-- "docs/examples/cli/multi-protocol-gre/policies/pol/gre-policy.yaml"
    ```

    ??? example "Output"

        ```text title="gre-policy.acl"
        --8<-- "docs/examples/cli/multi-protocol-gre/expected/gre-policy.acl"
        ```

        ```text title="gre-policy.jcl"
        --8<-- "docs/examples/cli/multi-protocol-gre/expected/gre-policy.jcl"
        ```

The rules:

- List every protocol explicitly. A term with ports and no `protocol`, or whose `protocol` has none of the service's protocols (for example `NTP`, which is `udp` only, with `protocol: tcp`), fails with `TermPortProtocolError` and `no destination ports of the correct protocol for term dns`.
- Keep protocols with ports and protocols without ports in separate terms. `protocol: [tcp, udp, icmp]` with ports, or `protocol: [gre, tcp]` with `destination-port: HTTPS`, fails with `MixedPortandNonPortProtos` and `Term dns contains mixed uses of protocols with and without port numbers`.
- Never list a port-based protocol without a port unless you mean any port. `protocol: [gre, tcp]` with no `destination-port` is accepted and allows all TCP to the peer: Cisco renders `permit tcp any host 192.0.2.1` and Juniper renders `protocol [ gre tcp ];`.

## Validate as you write

Point your editor at the _[JSON Schema](../reference/policy_files.md#json-schema)_ for policy files to get completion and error checking while you type.

## Next

_[Writing Definitions](writing_definitions.md)_: name the networks and services your terms use.

_[Includes](includes.md)_: share terms and filters between policies.
