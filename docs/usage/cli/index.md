# Command Line Usage

Aerleon contains three command line programs:

* _[aclgen](aclgen.md)_ generates ACL files from your policy files (the primary program)
* _[aclcheck](aclcheck.md)_ checks where hosts, ports and protocols are matched in a single policy file
* _[cgrep](cgrep.md)_ answers queries about addresses, ports and protocols found in the definition files

A fourth program, _[pol2yaml](pol2yaml.md)_, converts .pol, .inc, .svc, and .net files to equivalent YAML files. It can be found in [its own repository](https://github.com/aerleon/pol2yaml) but is documented here.

## Common Options

Options used by more than one command line program are listed here. Setting these options in your config file is a good practice. See _[--config_file](#config_file)_.

Option | aclgen | aclcheck | pol2yaml | cgrep
---- | --- | --- | --- | ---
base_directory | input,<br>import resolution | import resolution | input,<br>import resolution | n/a
definitions_directory | ✔ | ✔ | ✔ | flag only
output_directory | ✔ |  | ✔
optimize | ✔ |  |  |
debug | ✔ |  |  |
max_renderers | ✔ |  |  |
shade_check | ✔ |  |  |
exp_info | ✔ |  |  |

*Above: which config file options are supported by which program.*

`cgrep` accepts `--definitions_directory` on the command line but doesn't read `aerleon.yml`.


### base_directory

Policy files should be placed in **base_directory**. `aclgen` renders the policy files in every directory named `pol` under it (see _[Finding policy files](aclgen.md#finding-policy-files)_); `pol2yaml` converts every `.pol` and `.inc` file under it, except if the flag `--policy_file` is used to give a specific input file (`aclgen` only). Relative paths that appear in "include" directives will be resolved against base_directory. The default value is './policies'.

### definitions_directory

Network and service definition files should be placed in **definitions_directory**. All files in this directory will be loaded and used to resolve symbolic network and service names. Unlike base_directory, definitions_directory is not searched recursively for input files. The default value is './def'.

### output_directory

`aclgen` will place all generated ACLs in this directory. For `aclgen` the default value is the current directory.

`pol2yaml` will place each converted file adjacent to its input file by default. If **output_directory** is given, `pol2yaml` will mirror the directory structure of the input files in the output_directory, potentially creating directories in the process.

### config_file

In addition to accepting command line arguments, `aclgen`, `aclcheck`, and
`pol2yaml` will look for a config file named 'aerleon.yml' in the current directory.
This location can be configured with the `--config_file` option. Options specified on
the command line take precedence over options in config files.

For example:

```yaml
base_directory: ./policies
definitions_directory: ./def
exp_info: 2
max_renderers: 10
```
