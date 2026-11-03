# pol2yaml

`pol2yaml` converts .pol, .inc, .svc, and .net files to equivalent YAML files. It can be found in [its own repository](https://github.com/aerleon/pol2yaml) but is documented here.

## Flags

```
pol2yaml: Convert .pol, .inc policy files and .svc, .net definitions into equivalent YAML files.

Usage: pol2yaml [--base_directory DIRECTORY] [-c|--config_file FILE] [--definitions_directory DIRECTORY]
    [-h|--help] [--no-fix-include] [--output_directory DIRECTORY] [-s|--sanity_check]

Examples:

* Recursively convert all .pol and .inc files in base_directory.
  Original files are left in place. Each YAML file is placed in the same
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
