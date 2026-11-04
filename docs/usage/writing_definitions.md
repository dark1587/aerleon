# Writing Definitions

Definitions give names, called tokens, to networks and services. A policy refers to a token such as `MGMT` or `SSH` instead of repeating addresses and ports, and `aclgen` expands the token when it renders the output. See the _[Definitions Spec](../reference/definitions.md)_ for every field.

`aclgen` reads every `.yaml`, `.yml`, `.net` or `.svc` file directly in the definitions directory (`./def` by default). Subdirectories aren't read. Tokens from all of those files share one namespace.

The examples below are real files that `aclgen` runs in the docs test suite, so the output shown is exactly what you get.

=== "Flat token"

    A network token lists its addresses under `values`, and a service token lists `port` and `protocol` pairs. The policy refers to them by name: `MGMT` expands to both networks, and `SSH` to TCP port 22.

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

=== "Nested token"

    A network token can include other network tokens. Under `values`, an entry of the form `- name: TOKEN` pulls in everything that token defines. Here `MGMT` is built from `JUMP_HOSTS` and `OPS_NET`, and the policy is unchanged: it still says `source-address: MGMT`, which now expands to all three addresses.

    ```yaml title="def/definitions.yaml"
    --8<-- "docs/examples/cli/definitions-nested/def/definitions.yaml"
    ```

    ```yaml title="policies/pol/edge-inbound.yaml"
    --8<-- "docs/examples/cli/definitions-nested/policies/pol/edge-inbound.yaml"
    ```

    ??? example "Output"

        ```text title="edge-inbound.acl"
        --8<-- "docs/examples/cli/definitions-nested/expected/edge-inbound.acl"
        ```

=== "Services"

    A service token can include other service tokens too. In the service list, an entry of the form `- name: TOKEN` pulls in that service. `ADMIN_SERVICES` includes `SSH` and `HTTPS`, so one `destination-port` line in the policy covers both ports. The term renders one `permit` line per source and port: three sources and two ports give six lines.

    ```yaml title="def/definitions.yaml"
    --8<-- "docs/examples/cli/definitions-services/def/definitions.yaml"
    ```

    ```yaml title="policies/pol/edge-inbound.yaml"
    --8<-- "docs/examples/cli/definitions-services/policies/pol/edge-inbound.yaml"
    ```

    ??? example "Output"

        ```text title="edge-inbound.acl"
        --8<-- "docs/examples/cli/definitions-services/expected/edge-inbound.acl"
        ```

## Common errors

A token name can be defined only once, and every token a policy or another token refers to must be defined. These are the errors you see when that isn't so.

- `Multiple definitions found for network: MGMT`: the token `MGMT` is defined in two different files in the definitions directory, and `aclgen` stops. Repeating a key twice inside one file does not raise this error: YAML keeps the later one and silently drops the earlier, so keep each token in one place.
- `The following tokens were nested as a values, but not defined {'JUMP_HOSTS': True}`: a token lists `- name: JUMP_HOSTS` under `values`, but no token with that name exists.
- `Error parsing policy file …` with `UNDEFINED: NOPE`: a policy uses the token `NOPE`, which no definitions file defines.

## From Python

The API can load definitions from dicts instead of files. See the _[Definitions (Naming)](../api/definitions.md)_ page.
