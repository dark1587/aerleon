# Policy Objects

`Generate()` takes a list of policy objects. A policy object is a Python dictionary with the same structure as a policy YAML file: the file loaded into dictionaries and lists. This page describes the four dictionary shapes and how a YAML file maps onto them. For the meaning of each field, see _[Policy File Spec](../reference/policy_files.md)_.

## PolicyDict

One policy, which `Generate()` turns into one output file per target.

- `filters`: a list of `PolicyFilter` dictionaries.
- `filename` (optional): a name that decides the output file name. See _[Gotchas](#gotchas)_.

Rendered in API Reference.

## PolicyFilter

One filter: a header and the terms it contains.

- `header`: a dictionary with `targets`, a dictionary that maps a platform name to its target value, and optionally `comment`, `apply-groups` and `apply-groups-except`.
- `terms`: a list of terms. Each entry is either a term dictionary or a `PolicyInclude`.

Rendered in API Reference.

## PolicyFilterTermsOnly

The body of an include: a dictionary with only `terms`, which is a list of term dictionaries. You pass these in the `includes` argument of `Generate()`, keyed by include name.

- `terms`: a list of terms.

Rendered in API Reference.

## PolicyInclude

A term-list entry that pulls in the terms of an include.

- `include`: the include name.

Rendered in API Reference.

These four are `TypedDict`s. They exist for type checkers and editors only: nothing checks them when the code runs, so a wrong key or a wrong type is not reported by the dictionary itself.

## YAML and dicts

A policy file and a `PolicyDict` hold the same data. The keys are identical, including the hyphens, so `source-address` in YAML is `"source-address"` in the dictionary.

=== "YAML"

    ```yaml title="policies/edge-inbound.yaml"
    --8<-- "docs/examples/api/policies/edge-inbound.yaml"
    ```

=== "Python dict"

    ```python title="policy_yaml_to_dict.py"
    --8<-- "docs/examples/api/policy_yaml_to_dict.py:dict"
    ```

The module `policy_yaml_to_dict.py` loads the YAML file with `yaml.safe_load`, compares it with the dictionary, and generates from the loaded data. Examples run from `docs/examples/api/`.

??? example "Output"

    ```text title="policy_yaml_to_dict.stdout.ref"
    --8<-- "docs/examples/api/policy_yaml_to_dict.stdout.ref"
    ```

The mapping rules:

- A term value that holds several names can be a list or a space-separated string: `["MGMT", "BOGON"]` and `"MGMT BOGON"` are the same.
- A target value is a string of the form `"<filter-name> <options…>"`, for example `"edge-inbound mixed"`.
- `filename` is not in the YAML file, because `aclgen` uses the name of the file. When you load YAML yourself, add `filename` to the dictionary, as the example does with `"edge-inbound.yaml"`.

## Gotchas

These cases come from `policy_gotchas.py`. Each case prints under its own `--- <case> ---` line.

```python title="policy_gotchas.py"
--8<-- "docs/examples/api/policy_gotchas.py"
```

??? example "Output"

    ```text title="policy_gotchas.stdout.ref"
    --8<-- "docs/examples/api/policy_gotchas.stdout.ref"
    ```

- **A missing `filename` gives `<unknown>.acl`.** Set `filename` on every policy.
- **`filename` becomes the output name.** The directory part is dropped and the last suffix is replaced by the generator's suffix, so `"pol/edge-inbound"` and `"edge-inbound.yaml"` both give `edge-inbound.acl`.
- **Equal output names overwrite each other, silently.** Two policies with the same `filename` and platform produce one file, and the later policy wins. In the example the result has one entry, and it holds the `second` filter. Keep names unique, as described in _[Best Practices](best_practices.md#use-a-unique-filename-per-policy)_.
- **A misspelled term key is dropped.** `destination_address` is not a term keyword. It is ignored with an `Unexpected term keyword destination_address` message in the log, and the term renders as `permit ip any any`. The example prints the `permit` lines so you can see it.
- **A list and a space-separated string are equivalent.** Both forms of `source-address` render the same ACL, as the last case shows.
- **A target value must be a non-empty string.** An empty value is an error, not a default.
- **An `include` term needs a source.** A `{"include": ...}` term only works if you pass `include_path` or `includes` to `Generate()`. Without either, it fails. See _[Includes in the API](includes.md)_.
