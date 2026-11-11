# aclgen

`aclgen` generates ACL files from your policy files. It is the primary Aerleon program.

## Examples

Render every policy under `./policies` (definitions are read from `./def`) into `out/`:

```bash
aclgen --output_directory out
```

Render a single policy file into `out2/`:

```bash
aclgen --output_directory out2 --policy_file policies/site-a/pol/core.yaml
```

With a Cisco and a Juniper target in each policy, the two runs write these files:

```
out/edge-inbound.acl
out/edge-inbound.jcl
out/site-a/core.acl
out/site-a/core.jcl
out2/site-a/core.acl
out2/site-a/core.jcl
```

## Finding policy files

`aclgen` renders the `*.pol`, `*.yaml` and `*.yml` files found directly inside every directory named `pol` under `base_directory`. Files in subdirectories of a `pol` directory aren't rendered. `pol` directories are skipped when they sit directly inside (`def/pol`) or one level below (`def/a/pol`) a directory matching one of the glob patterns in `--ignore_directories`; deeper ones (`def/a/b/pol`) are still found. The default is `DEPRECATED,def`, and the flag takes a comma-separated list. The example above uses this project:

```
def/
  definitions.yaml
policies/
  pol/
    edge-inbound.yaml
  site-a/
    pol/
      core.yaml
```

## Output file naming

Each output file is written to `output_directory`, then the path of the `pol` directory's parent relative to `base_directory`, then the policy file name without its extension plus the generator's suffix (see the File suffix column in the _[Generators Overview](../../reference/generators.md#generators)_). For example, `policies/site-a/pol/core.yaml` becomes `out/site-a/core.acl` for the Cisco target and `out/site-a/core.jcl` for the Juniper target.

!!! note
    A file given with `--policy_file` follows the same rule, so it must be under `base_directory`.

## Flags

```
  --base_directory: The base directory to search recursively for policy files.
                    Relative policy imports are resolved against this directory.
                    If --policy_file is used, aclgen will not search this directory.
    Default: './policies'

  --config_file: A YAML file with configuration options;
    repeat this option to specify a list of values

  --[no]debug: Display detailed messages.
    Default: 'false'

  --definitions_directory: Directory containing network and service definition files.
    Default: './def'

  --exp_info: Print a message when a term is set to expire in that many weeks.
    Default: '2'
    (an integer)

  --ignore_directories: Don't descend into directories that look like this string.
    Default: 'DEPRECATED,def'
    (a comma separated list)

  --max_renderers: Max number of rendering processes to use.
    Default: '10'
    (an integer)

  -o,--[no]optimize: Turn on optimization.
    Default: 'False'

  --output_directory: Directory to output the rendered acls.
    Default: './'

  --policy_file: Individual policy file to generate.

  --[no]shade_check: Raise an error when a term is completely shaded by a prior term.
    Default: 'false'
```

Options shared with other tools: _[Common Options](index.md#common-options)_.
