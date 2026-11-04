# Best Practices

This page collects habits that keep API-driven generation predictable: check your input before you call `Generate()`, keep output names unique, handle errors by type, and choose between returned strings and files. For the function itself, see _[API Overview](index.md)_.

Examples run from `docs/examples/api/`, because they load definitions with the relative path `def/`. Run them from that directory if you try them yourself.

## Validate before generating

Two mistakes can pass through `Generate()` without an error, so check for them yourself.

The first is an undefined name that a definition refers to. A `Naming` built from a dictionary or a single file keeps such names in `unseen_networks` and `unseen_services`, and only fails later when something uses them. Raise an error as soon as either one is not empty. _[Definitions (Naming)](definitions.md#checking-for-undefined-names)_ explains where the check applies.

The second is a repeated output name. `Generate()` names each result from `Path(filename).stem` plus the platform suffix, so `edge-inbound` and `pol/edge-inbound` both produce `edge-inbound.acl`, and the later policy silently replaces the earlier one. Comparing stems is a little stricter than needed, because two platforms with different suffixes would not collide, but it is simple and it never misses a clash.

The example below defines `check_definitions`, `check_output_names` and `generate`, which runs both checks first. It then tries four cases: a good policy, an undefined name in the definitions, a repeated output name, and a policy that uses `NOPE`, which no definition provides.

```python title="best_practices_validate.py"
--8<-- "docs/examples/api/best_practices_validate.py"
```

??? example "Output"

    ```text title="best_practices_validate.stdout.ref"
    --8<-- "docs/examples/api/best_practices_validate.stdout.ref"
    ```

Keep term keys hyphenated exactly as in the _[Policy File Spec](../reference/policy_files.md)_, such as `source-address`. An unknown key such as `destination_address` is dropped with an `Unexpected term keyword destination_address` message in the log, and the term then renders as `permit ip any any`. Review the warnings that `Generate()` logs, because that message is the only sign of the mistake.

## Use a unique filename per policy

The `filename` of each policy decides the names of its output files. Give every policy a distinct stem, and don't rely on directories or extensions to tell them apart: `pol/edge-inbound` and `edge-inbound.yaml` both become `edge-inbound`. A policy without a `filename` is written as `<unknown>.acl`, so a second one without a name replaces it.

## Catch the errors you can handle

Errors that occur while a policy or its definitions are built are wrapped. A missing name raises `aerleon.aclgen.ACLParserError`, and a failure inside a platform generator raises `aerleon.aclgen.ACLGeneratorError`. The first line of the message names the policy, for example `Error parsing policy bad-policy:`. The example above turns both into a `RuntimeError` that carries only that line.

Some errors are not wrapped, so catch them separately if your program can run into them:

- Errors from expanding includes: `aerleon.lib.yaml.PolicyTypeError`, `aerleon.lib.policy.BadIncludePath`, `FileNotFoundError` and `aerleon.lib.yaml.ExcessiveRecursionError`. See _[Includes in the API](includes.md)_.
- Errors from loading definitions: subclasses of `aerleon.lib.naming.Error`.
- Errors from `AclCheck()`, such as `aerleon.lib.port.BadPortValue` for a port that is not a number.

## Keep definitions and policies separate

Load the definitions once and reuse the `Naming` object for every `Generate()` call. Policies then only refer to names such as `MGMT` and `SSH`, and a change to an address is made in one place. Build the `Naming` from files with `naming.Naming("def")` or from dictionaries with `ParseDefinitionsObject()`, as shown in _[Definitions (Naming)](definitions.md)_. Don't pass bare address strings in `values`, because they count as undefined names.

## Point your editor at the JSON Schema

The repository ships two schemas, `schemas/aerleon-policies.schema.json` and `schemas/aerleon-definitions.schema.json`. An editor with the YAML language server can then check your files and complete keys as you type. Add one line at the top of each file:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/aerleon/aerleon/main/schemas/aerleon-policies.schema.json
```

Use `aerleon-definitions.schema.json` for definitions files. The fields are described in _[Policy File Spec](../reference/policy_files.md)_. For the schemas themselves, see _[JSON Schema](../reference/policy_files.md#json-schema)_.

## Returned strings or output_directory

Without `output_directory`, `Generate()` returns a dictionary from file name to text, and writes nothing. Use it when your program needs the text, for example to push it to a device or compare it with something. With `output_directory`, it returns `None` and writes the same names into that directory. Use it when the files are the product.

`output_directory` must be a `pathlib.Path`. A plain `str` raises a `TypeError`. The files are written flat, without subdirectories, and only files whose content changed are written.

```python title="best_practices_output_directory.py"
--8<-- "docs/examples/api/best_practices_output_directory.py"
```

??? example "Output"

    ```text title="best_practices_output_directory.stdout.ref"
    --8<-- "docs/examples/api/best_practices_output_directory.stdout.ref"
    ```

## Workflow

- Generate in CI, so every change to a policy or a definition produces fresh output.
- Review the diffs of the generated output, because a small policy change can touch many lines.
- Keep policies and definitions in git, with the generated files if you deploy from them.
