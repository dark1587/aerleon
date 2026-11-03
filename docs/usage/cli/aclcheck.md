# aclcheck

`aclcheck` is a tool bundled with Aerleon that checks which terms in a single policy file would match a specific packet, and what action or actions the generated ACL would take. Use it to verify policy correctness, troubleshoot connectivity issues, and understand the impact of policy changes.

## Basic Example

To check whether traffic from `192.168.1.10` to `10.0.0.1` on TCP port `80` is allowed by the sample Cisco policy, run this from the repository root:

```bash
aclcheck --policy-file ./policies/pol/sample_cisco_lab_yaml.yaml --source 192.168.1.10 --destination 10.0.0.1 --protocol tcp --dport 80
```

```
  filter: allowtointernet
          term: accept-tcp-replies (possible match)
                accept if ['tcp-est']
          term: deny-to-internal
                deny
```

The output shows the terms in the policy that match the specified traffic and the action (for example `accept`, `deny`, `next`) taken by those terms.

## Flags

```
usage: aclcheck [-h] -p POL [--definitions-directory DEFINITIONS_DIRECTORY]
                [--base-directory BASE_DIRECTORY] [--config-file CONFIG_FILE] [-d DESTINATION_IP]
                [-s SOURCE_IP] [--proto PROTOCOL] [--dport DESTINATION_PORT] [--sport SOURCE_PORT]
                [--source-zone SOURCE_ZONE] [--destination-zone DESTINATION_ZONE]

Check where hosts, ports and protocols match in a NAC policy.

options:
  -h, --help            show this help message and exit
  -p, --policy-file, --policy_file POL
                        The policy file to examine.
  --definitions-directory, --definitions_directory DEFINITIONS_DIRECTORY
                        The directory where network and service definition files can be found.
  --base-directory, --base_directory BASE_DIRECTORY
                        The base directory to use when resolving policy include paths.
  --config-file, --config_file CONFIG_FILE
                        Change the location searched for the configuration YAML file.
  -d, --destination DESTINATION_IP
                        Destination IP address or network.
  -s, --source SOURCE_IP
                        Source IP address or network.
  --proto, --protocol PROTOCOL
                        Protocol (tcp, udp, icmp, etc.)
  --dport, --destination-port, --destination_port DESTINATION_PORT
                        Destination port.
  --sport, --source-port, --source_port SOURCE_PORT
                        Source port.
  --source-zone, --source_zone SOURCE_ZONE
                        Source security/zone identifier. When provided, `AclCheck` will only match terms that either have no `source-zone` constraint or explicitly match this zone. Use the exact zone name as used in your policy (case-sensitive).
  --destination-zone, --destination_zone DESTINATION_ZONE
                        Destination security/zone identifier. When provided, `AclCheck` will only match terms that either have no `destination-zone` constraint or explicitly match this zone. Use the exact zone name as used in your policy (case-sensitive).
```

Options shared with other tools: _[Common Options](index.md#common-options)_.

### Defaults

| Flag | Default |
|---|---|
| `-d`, `--destination` | `200.1.1.1` |
| `-s`, `--source` | `any` |
| `--proto`, `--protocol` | `any` |
| `--dport`, `--destination-port` | `80` |
| `--sport`, `--source-port` | `1025` |
| `--definitions-directory` | `./def` |
| `--base-directory` | `./policies` |

## Detailed Example

This example uses several options. Run it from the repository root:

```bash
aclcheck --policy-file ./policies/pol/sample_cisco_lab_yaml.yaml \
         --definitions-directory ./def \
         --source 10.1.1.1 \
         --destination 172.16.1.0/24 \
         --protocol udp \
         --dport 53 \
         --sport 12345
```

This checks the `sample_cisco_lab_yaml.yaml` policy, using definitions from the `./def` directory, for traffic from `10.1.1.1` (source port `12345`) to `172.16.1.0/24` (destination port `53`) using the UDP protocol. The output indicates which terms in the policy match this traffic and what action or actions are taken.

```
  filter: allowtointernet
          term: deny-to-internal
                deny
```

To call AclCheck from Python, see _[AclCheck API](../../aclcheck_api.md)_.
