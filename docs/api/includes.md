# Includes in the API

An include pulls a shared list of terms into a filter, so that several policies can reuse the same terms. In Python you supply the include sources to `Generate()` yourself, either as a directory of YAML files (`include_path`) or as a dictionary (`includes`). For the concepts and the expansion diagram, see _[Includes](../usage/includes.md)_.

Examples run from `docs/examples/api/`, because they load definitions with the relative path `def/`. Run them from that directory if you try them yourself.

## include_path or includes

Both examples use the same policy. Its `edge-inbound` filter starts with `{"include": "bogons.yaml"}`, then allows SSH from `MGMT`, then ends with `default-deny`. The include supplies two deny terms, `deny-reserved` and `deny-bogons`.

=== "include_path"

    `include_path` is a directory. Each include name is a file path relative to it. Here the directory is `policies/includes`, and it holds `bogons.yaml`.

    ```yaml title="policies/includes/bogons.yaml"
    --8<-- "docs/examples/api/policies/includes/bogons.yaml"
    ```

    ```python title="includes_path.py"
    --8<-- "docs/examples/api/includes_path.py"
    ```

=== "includes dict"

    `includes` maps each include name to a dictionary with a `terms` list, the same content as the YAML file. The name is just a key, so no file is read.

    ```python title="includes_dict.py"
    --8<-- "docs/examples/api/includes_dict.py"
    ```

Both examples print the same ACL. The two deny terms from the include come first, followed by `allow-ssh` and `default-deny`.

??? example "Output"

    ```text title="includes_path.stdout.ref"
    --8<-- "docs/examples/api/includes_path.stdout.ref"
    ```

## Rules

- **Suffix and directory rules apply to `include_path` only.** An include name must end in `.yaml` or `.yml`, and the file it names must be inside the `include_path` directory. A name that points outside the directory, such as `../edge-inbound.yaml`, is refused.
- **Dictionary keys are any string.** With `includes` there is no suffix rule and no directory rule. The key only has to equal the name written in the `include` term. Each value is a dictionary of the form `{"terms": [...]}`, which is `PolicyFilterTermsOnly` in the code. See _[Policy Objects](policy_objects.md)_.
- **Filter includes work only with `include_path`.** A whole-filter include, which uses `filters_include_only` in the file, cannot be supplied through the `includes` dictionary. Aerleon does not report this clearly: the call fails with an `AttributeError` instead of a message about includes. Use `include_path` for filter includes.
- **Nesting is limited to 5 levels.** An included file can include other files, up to five levels deep. Deeper nesting is an error.
- **The two arguments are mutually exclusive.** Passing a non-empty `include_path` and a non-empty `includes` together raises a `TypeError`.
- **Include terms need one of the two arguments.** If a policy contains an `include` term and you pass neither argument, the call fails. See _[Policy Objects](policy_objects.md)_.

## Errors

```python title="includes_errors.py"
--8<-- "docs/examples/api/includes_errors.py"
```

??? example "Output"

    ```text title="includes_errors.stdout.ref"
    --8<-- "docs/examples/api/includes_errors.stdout.ref"
    ```

The first case shows the `TypeError` for passing both arguments. The third and fourth cases show the two `include_path` checks, the missing suffix and the path outside the directory.

!!! warning "A mistyped dictionary key is not an error"

    The second case misspells the key as `bogon.yaml`. Aerleon finds no source for `bogons.yaml`, skips the include, and logs `Ignoring empty policy include source.` to the log. The call still succeeds, and the ACL has no `deny-reserved` or `deny-bogons` term. The output above shows only the `allow-ssh` and `default-deny` remarks. Check the generated ACL when you build an `includes` dictionary, and keep the keys and the `include` values in one place.
