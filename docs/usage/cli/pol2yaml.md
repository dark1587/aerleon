# pol2yaml

`pol2yaml` converts .pol, .inc, .svc, and .net files to equivalent YAML files. It is a separate Node.js tool, not part of the Aerleon Python package. It lives in [its own repository](https://github.com/aerleon/pol2yaml) and is documented here. Run it with `npx`, which downloads and runs it without a permanent install.

Tested with pol2yaml 1.2.1.

## Flags

```
pol2yaml: Convert .pol, .inc policy files and .svc, .net definitions into equivalent YAML files.

Usage: pol2yaml [--base_directory DIRECTORY] [-c|--config_file FILE] [--definitions_directory DIRECTORY]
    [-h|--help] [--no-fix-include] [--output_directory DIRECTORY] [-s|--sanity_check]

Examples:

* Recursively convert all .pol and .inc files in base_directory.
  Original files are left in place. Each YAML files is placed in the same
  directory as the original file. Run sanity_check after (-s).

    npx pol2yaml -s --base_directory policies/


Options:

--base_directory    Convert .pol and .inc files found in this directory to
                    YAML. Original files are left in place. Can be set in
                    the 'aerleon.yml' config file.

--config_file | -c  Defaults to 'aerleon.yml'. Can set base_directory and
                    definitions_directory.

--definitions_directory
                    Convert .net and .svc files found in this directory to
                    YAML. Original files are left in place. Can be set in
                    the 'aerleon.yml' config file.

--help | -h         Display this message and exit.

--no_collapse       By default, lists will be formatted as space-separated
                    values on the same line as much as possible. This option
                    disables this behavior and causes lists to always appear
                    with one item per line.

--no_fix_include    By default, if an #include directive references a file
                    name with the .inc extension, the file name will appear
                    in the YAML output with the extension changed to
                    ".yaml". This flag leaves the file name unchanged.

--output_directory  Default: current directory. Sets the output directory
                    where YAML files will be placed.

--sanity_check | -s Run 'aclgen' on both the original and YAML files and
                    ensure the results are identical.

                    Sanity check requires that either Aerleon or pipx
                    are available. To run 'aclgen' it will try each of
                    the following commands in order:

                        python3 -m aerleon

                        python3 -m pipx run aerleon

                        aclgen
```

Options shared with other tools: _[Common Options](index.md#common-options)_.

## Migrating a Capirca project

This walkthrough converts a small Capirca-style project to YAML and checks that the output is unchanged. Every output block below was pasted from a real run.

1. **Starting layout.** The project has two definitions files, one policy and one include:

    ```
    def/NETWORK.net
    def/SERVICES.svc
    policies/includes/default-deny.inc
    policies/pol/edge-inbound.pol
    aerleon.yml
    ```

    `def/NETWORK.net`:

    ```
    MGMT = 10.0.0.0/24
           192.168.10.0/24
    ```

    `def/SERVICES.svc`:

    ```
    SSH = 22/tcp
    ```

    `policies/includes/default-deny.inc`:

    ```
    term default-deny {
      action:: deny
    }
    ```

    `policies/pol/edge-inbound.pol`:

    ```
    header {
      target:: cisco edge-inbound extended
      target:: juniper edge-inbound inet
    }

    term allow-ssh {
      comment:: "Allow SSH from management."
      source-address:: MGMT
      protocol:: tcp
      destination-port:: SSH
      action:: accept
    }

    #include 'includes/default-deny.inc'
    ```

2. **Configure the directories.** `aerleon.yml` tells both `pol2yaml` and `aclgen` where to look:

    ```yaml
    base_directory: ./policies
    definitions_directory: ./def
    ```

3. **Convert and sanity-check.** `-s` runs `aclgen` on the original files and on the YAML files and compares the results. To do this it tries `python3 -m aerleon`, then `python3 -m pipx run aerleon`, then `aclgen`, and uses the first that works.

    ```
    $ npx --yes pol2yaml@1.2.1 -s
    Converting policies/pol/edge-inbound.pol
    Converting policies/includes/default-deny.inc
    Converting def/SERVICES.svc
    Converting def/NETWORK.net
    Running sanity check...
    Running original files through aclgen...
    Running YAML files through aclgen...
    Comparing aclgen outputs...
    Sanity check passed
    ```

    The original files are left in place, and each YAML file is written next to its source.

4. **Review the generated YAML.** The `.inc` include became `include: includes/default-deny.yaml`: the file name now ends in `.yaml`. See _[Policy File Spec](../../reference/policy_files.md#includes)_ and _[Definitions Spec](../../reference/definitions.md)_ for the formats.

    `def/NETWORK.yaml`:

    ```yaml
    networks:
      MGMT:
        values:
          - address: 10.0.0.0/24
          - address: 192.168.10.0/24
    ```

    `def/SERVICES.yaml`:

    ```yaml
    services:
      SSH:
        - port: 22
          protocol: tcp
    ```

    `policies/includes/default-deny.yaml`:

    ```yaml
    terms:
      - name: default-deny
        action: deny
    ```

    `policies/pol/edge-inbound.yaml`:

    ```yaml
    filters:
      - header:
          targets:
            cisco: edge-inbound extended
            juniper: edge-inbound inet
        terms:
          - name: allow-ssh
            comment: |-
              Allow SSH from management.
            source-address: MGMT
            protocol: tcp
            destination-port: SSH
            action: accept
          - include: includes/default-deny.yaml
    ```

5. **Remove the originals.** Delete the `.pol`, `.inc`, `.net` and `.svc` files once you are happy with the YAML.

    !!! warning
        Do not leave both formats in `def/`. Aerleon reads the `.net` and `.yaml` definitions together, finds `MGMT` defined twice, and stops. The last lines of the `aclgen` error are:

        ```
        aerleon.lib.naming.NamespaceCollisionError:
        Multiple definitions found for network: MGMT
        ```

        Do not leave both the `.pol` and the converted `.yaml` policy in `pol/` either. `aclgen` raises no error: it renders both files, which write to the same output names, so one set of output files silently overwrites the other. With `edge-inbound.pol` and `edge-inbound.yaml` both present, `aclgen` reports `2 pol files found` and `writing 4 files to disk`, but only `edge-inbound.acl` and `edge-inbound.jcl` result.

6. **Run `aclgen`.** With only the YAML files left, `aclgen` succeeds and writes the Cisco and Juniper files to the current directory:

    ```
    ./edge-inbound.acl
    ./edge-inbound.jcl
    ```
