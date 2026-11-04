# Writing Policies

A policy file holds a list of `filters`. Each filter is a `header` plus `terms`: the header names the `targets` (the platforms to render for, each with its options), and the terms are the rules. See the _[Policy File Spec](../reference/policy_files.md)_ for every field, and the Usage Overview for where policy files go. This is the page that teaches `targets:` and files with more than one header.

The examples below are real files that `aclgen` runs in the docs test suite, so the output shown is exactly what you get.

=== "Single platform"

    One target, one output file. The output is named after the policy file (`edge-inbound.yaml`) plus the generator's suffix, here `.acl` for Cisco. See _[Generators](../reference/generators.md)_ for each generator's suffix. This tab also shows the definitions file the policy refers to.

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

    A second entry under `targets:` renders the same terms for another platform, giving one output file per target: `.acl` for Cisco and `.jcl` for Juniper. Each target line is the generator name followed by that generator's options.

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

    Options on a target line belong to that target alone. Here `noverbose` on the Juniper target drops the term comment from the `.jcl` file only; the `.acl` file still carries it. See _[Generators](../reference/generators.md)_ for the options each generator accepts.

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

## Validate as you write

Point your editor at the _[JSON Schema](../reference/policy_files.md#json-schema)_ for policy files to get completion and error checking while you type.

## Next

_[Writing Definitions](writing_definitions.md)_: name the networks and services your terms use.
