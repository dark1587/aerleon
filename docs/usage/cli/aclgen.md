# aclgen

`aclgen` generates ACL files from your policy files. It is the primary Aerleon program.

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
