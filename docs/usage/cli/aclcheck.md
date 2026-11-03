# aclcheck

`aclcheck` checks where hosts, ports and protocols are matched in a single policy file.

## Flags

```
usage: aclcheck [-h] -p POL [--definitions-directory DEFINITIONS_DIRECTORY] [--base-directory BASE_DIRECTORY] [--config-file CONFIG_FILE] [-d DESTINATION_IP] [-s SOURCE_IP]
                [--proto PROTOCOL] [--dport DESTINATION_PORT] [--sport SOURCE_PORT]

Check where hosts, ports and protocols match in a NAC policy.

options:
  -h, --help            show this help message and exit
  -p POL, --policy-file POL, --policy_file POL
                        The policy file to examine.
  --definitions-directory DEFINITIONS_DIRECTORY, --definitions_directory DEFINITIONS_DIRECTORY
                        The directory where network and service definition files can be found.
  --base-directory BASE_DIRECTORY, --base_directory BASE_DIRECTORY
                        The base directory to use when resolving policy include paths.
  --config-file CONFIG_FILE, --config_file CONFIG_FILE
                        Change the location searched for the configuration YAML file.
  -d DESTINATION_IP, --destination DESTINATION_IP
                        Destination IP.
  -s SOURCE_IP, --source SOURCE_IP
                        Source IP.
  --proto PROTOCOL, --protocol PROTOCOL
                        Protocol (tcp, udp, icmp, etc.)
  --dport DESTINATION_PORT, --destination-port DESTINATION_PORT, --destination_port DESTINATION_PORT
                        Destination port.
  --sport SOURCE_PORT, --source-port SOURCE_PORT, --source_port SOURCE_PORT
                        Source port.
  --source-zone, --source_zone SOURCE_ZONE
                        Source security/zone identifier. When provided, `AclCheck` will only match terms that either have no `source-zone` constraint or explicitly match this zone. Use the exact zone name as used in your policy (case-sensitive).
  --destination-zone, --destination_zone DESTINATION_ZONE
                        Destination security/zone identifier. When provided, `AclCheck` will only match terms that either have no `destination-zone` constraint or explicitly match this zone. Use the exact zone name as used in your policy (case-sensitive).
```

Options shared with other tools: _[Common Options](index.md#common-options)_.
