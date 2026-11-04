# Definitions (Naming)

A `Naming` object holds the network and service tokens that a policy refers to, such as `MGMT` and `SSH`. `Generate()` needs one to expand those tokens into addresses and ports. You can build it from definitions files, from Python dictionaries, or from both. For the format of the files and dictionaries, see _[Definitions Spec](../reference/definitions.md)_. For writing the files, see _[Writing Definitions](../usage/writing_definitions.md)_.

Examples run from `docs/examples/api/`, because they load files with relative paths such as `def/`. Run them from that directory if you try them yourself.

## Loading definitions

Every tab prints the addresses of `MGMT` and the sorted names of the services it loaded. The files and dictionaries hold the same data.

=== "Directory"

    `Naming(naming_dir)` reads every definitions file directly in the directory, the way `aclgen` does.

    ```python title="definitions_directory.py"
    --8<-- "docs/examples/api/definitions_directory.py"
    ```

    ??? example "Output"

        ```text title="definitions_directory.stdout.ref"
        --8<-- "docs/examples/api/definitions_directory.stdout.ref"
        ```

=== "Single file"

    `Naming(naming_dir, naming_file)` loads one file. The file name is joined to the directory, so the directory is required: `Naming(naming_file="def/networks.yaml")` raises `TypeError`. Only that file loads, so the services are empty here.

    ```python title="definitions_single_file.py"
    --8<-- "docs/examples/api/definitions_single_file.py"
    ```

    ??? example "Output"

        ```text title="definitions_single_file.stdout.ref"
        --8<-- "docs/examples/api/definitions_single_file.stdout.ref"
        ```

=== "ParseDefinitionsObject"

    `Naming()` creates an empty object. Call `ParseDefinitionsObject(data, file_name)` once for each source: one call for networks and one for services, or one call with both. The dictionaries have the same structure as a definitions file.

    ```python title="definitions_objects.py"
    --8<-- "docs/examples/api/definitions_objects.py"
    ```

    ??? example "Output"

        ```text title="definitions_objects.stdout.ref"
        --8<-- "docs/examples/api/definitions_objects.stdout.ref"
        ```

    The second argument, `file_name`, is used only in warning messages. Aerleon logs ``Ignoring empty address book file. File=<file_name>.`` for an empty dictionary and ``File contains no network or service data. File=<file_name>.`` for one that has neither a `networks` nor a `services` key. The name does not appear in any error.

=== "Mixed"

    A `Naming` created from a file or a directory can take dictionaries too. Here the services come from a file and the networks from a dictionary.

    ```python title="definitions_mixed.py"
    --8<-- "docs/examples/api/definitions_mixed.py"
    ```

    ??? example "Output"

        ```text title="definitions_mixed.stdout.ref"
        --8<-- "docs/examples/api/definitions_mixed.stdout.ref"
        ```

The files used above:

```yaml title="def/networks.yaml"
--8<-- "docs/examples/api/def/networks.yaml"
```

```yaml title="def/services.yaml"
--8<-- "docs/examples/api/def/services.yaml"
```

## Nested tokens

A token can list another token with `- name: OTHER`, and the result includes that token's values. The other token can be defined later: in the example, `INTERNAL` names `MGMT` before `MGMT` appears.

```python title="definitions_nested.py"
--8<-- "docs/examples/api/definitions_nested.py"
```

??? example "Output"

    ```text title="definitions_nested.stdout.ref"
    --8<-- "docs/examples/api/definitions_nested.stdout.ref"
    ```

A bare string in `values` is a name reference, not an address. `"10.0.0.0/8"` still resolves, but Aerleon also records it in `unseen_networks`, as if it were a token that is not defined. Loading the same data with `Naming(naming_dir)` would then fail. Write `{"address": "10.0.0.0/8"}` instead.

## Token collisions

Defining a token that already exists raises `NamespaceCollisionError`. This holds across separate `ParseDefinitionsObject` calls, and between a file and a dictionary. The message reads `Multiple definitions found for network: MGMT`, or `... for service: SSH`.

The error is raised across sources. A key that appears twice in the same YAML file does not raise it: YAML keeps the later one and silently drops the earlier. See _[Writing Definitions](../usage/writing_definitions.md)_.

The same token also cannot be defined in two pieces. If you load definitions from an inventory system, group all the values for a token into one entry before you load them.

## Checking for undefined names

!!! warning "Undefined nested names often pass silently"

    A token can list a name that no definition provides. Only `Naming(naming_dir)`, with no `naming_file`, checks for this when it loads, and it raises an error such as `UndefinedAddressError` (or `UndefinedServiceError` for services). A single file, and every `ParseDefinitionsObject` call, load without any error. The undefined names are kept in `Naming.unseen_networks` and `Naming.unseen_services`, and the error appears only when something uses the name: `GetNet` raises `UNDEFINED: NOT_DEFINED`, and so does `Generate()`, wrapped in an `ACLParserError`. If you load definitions by any route other than the directory, check these two attributes yourself before you generate.

```python title="definitions_errors.py"
--8<-- "docs/examples/api/definitions_errors.py"
```

??? example "Output"

    ```text title="definitions_errors.stdout.ref"
    --8<-- "docs/examples/api/definitions_errors.stdout.ref"
    ```

The `def_unseen/networks.yaml` file used by two of the cases:

```yaml title="def_unseen/networks.yaml"
--8<-- "docs/examples/api/def_unseen/networks.yaml"
```

_[Best Practices](best_practices.md#validate-before-generating)_ shows how to turn this check into a validation step.
