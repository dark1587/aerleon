# Getting Started with Aerleon

This page takes you from nothing to a generated Cisco ACL in a few minutes. You will write a definitions file and a policy file, run `aclgen`, and read the output.

It assumes Aerleon is already installed; see _[Install and Configure](install.md)_ if not.

## Create the directories

Make a scratch directory with a `def` directory for definitions and a `policies/pol` directory for policies.

```bash
mkdir -p aerleon_test/def aerleon_test/policies/pol
cd aerleon_test
```

The rest of this page assumes you are inside `aerleon_test`.

## Write a definitions file

Definitions give names to networks and services, so policies can say `MGMT` instead of a list of addresses. Save this as `def/definitions.yaml`.

```yaml title="def/definitions.yaml"
--8<-- "docs/examples/cli/policy-single/def/definitions.yaml"
```

`MGMT` is a network made of two subnets. `SSH` is a service: TCP port 22.

## Write a policy

Save this as `policies/pol/edge-inbound.yaml`.

```yaml title="policies/pol/edge-inbound.yaml"
--8<-- "docs/examples/cli/policy-single/policies/pol/edge-inbound.yaml"
```

A policy file is a list of `filters`. Each filter has a `header`, which names the `targets` (the platforms to generate for), and `terms`, the rules. Here one term accepts SSH from `MGMT`, and a final term denies everything else. See _[Writing Policies](usage/writing_policies.md)_ for the details.

## Run aclgen

From the `aerleon_test` directory, run:

```bash
aclgen
```

No flags are needed: `aclgen` looks for policies in `./policies` and definitions in `./def` by default, and writes its output to the current directory. It logs its progress and writes `edge-inbound.acl`.

## Look at the output

```text title="edge-inbound.acl"
--8<-- "docs/examples/cli/policy-single/expected/edge-inbound.acl"
```

## Next steps

- _[Writing Policies](usage/writing_policies.md)_: add more platforms and more filters.
- Writing Definitions: more on networks and services.
- Includes: share terms between policies.
- _[API](api.md)_: generate policies from Python.
- _[Command Line Usage](usage/cli/index.md)_: every `aclgen` option.
