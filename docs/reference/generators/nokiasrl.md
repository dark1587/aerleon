# Nokia SR Linux

Renders Nokia SR Linux ACL filters as JSON. The Nokia SR Linux generator is built on the _[OpenConfig](openconfig.md)_ generator.

## Header Format

```yaml
targets:
    nokiasrl: [filter name] {inet|inet6|mixed} {stats} {r24.3|r24.3.2}
```

| Option | Description | Notes |
|---|---|---|
| `filter name` | Name of the ACL filter. | |
| `inet` | IPv4 only. | Default. |
| `inet6` | IPv6 only. | |
| `mixed` | IPv4 and IPv6. | Renders one IPv4 and one IPv6 filter. |
| `stats` | Collect statistics per entry. | Adds `statistics-per-entry: true`. |
| `r24.3` | Use the SR Linux 24.3.1 filter syntax. | Renders `acl-filter` with a `type`, instead of `ipv4-filter`/`ipv6-filter`. |
| `r24.3.2` | Use the syntax for SR Linux 24.3.2 and later. | Same as `r24.3`, plus matches are nested under `ipv4`/`ipv6`/`transport`, and `logging` works with any action. |

## Term Format

### Common tokens

These tokens are included from the _[Common](common.md)_ page.

!!! warning "Not supported on Nokia SR Linux"
    Nokia SR Linux doesn't support `platform`, `platform-exclude` or `verbatim`. A term that uses any of them raises an error.

--8<-- "docs/reference/generators/common.md:common-tokens"

### Nokia SR Linux tokens

Nokia SR Linux also reads:

| Token | Description | Example | Notes |
|---|---|---|---|
| `destination-prefix` | Match a named prefix list under `acl match-list`. | `destination-prefix: DC-NETS` | Can't be combined with `destination-address`. |
| `logging` | Log matching packets. | `logging: true` | Without `r24.3.2`, only allowed on `deny` terms (raises an error otherwise). |
| `source-prefix` | Match a named prefix list under `acl match-list`. | `source-prefix: CORP-NETS` | Can't be combined with `source-address`. |

The term name becomes the entry `description`, and `comment` becomes `_annotate_description` (max 255 characters). Entries get sequence IDs 5, 10, 15, …

## Actions

| Action | Rendered as | Notes |
|---|---|---|
| `accept` | `accept` | |
| `deny` | `drop` | |

## Option

| Option | Description | Example | Notes |
|---|---|---|---|
| `established` | Match established connections. | `option: established` | TCP: <code>tcp-flags: ack&#124;rst</code>. UDP: sets the destination port to 1024-65535. Requires a `tcp` or `udp` protocol. |
| `first-fragment` | Match the first fragment. | `option: first-fragment` | `first-fragment: true`. |
| `is-fragment`, `fragments` | Match fragments. | `option: is-fragment` | `fragment: true`. |
| `not-syn-ack` | Match TCP packets that are not SYN+ACK. | `option: not-syn-ack` | `tcp-flags: !(syn&ack)`. |
| `tcp-established` | Match established TCP connections. | `option: tcp-established` | <code>tcp-flags: ack&#124;rst</code>. TCP only. |
| `tcp-initial` | Match the first packet of a TCP connection. | `option: tcp-initial` | `tcp-flags: syn`. |

Options that set `tcp-flags` also set the protocol to TCP.

## Output

Each policy file renders to one file with the same name and a `.srl_acl` extension, so `sample.yaml` renders `sample.srl_acl`.

### Differences from OpenConfig

Nokia SR Linux inherits the OpenConfig generator logic to process Aerleon policies. Everything written into an entry is its own:

| Area | OpenConfig | Nokia SR Linux |
|---|---|---|
| Filter | One `acl-set` per filter, with `type` `ACL_IPV4`, `ACL_IPV6` or `ACL_MIXED` | One `ipv4-filter` and/or `ipv6-filter` per filter (`acl-filter` with `r24.3`); `mixed` renders both |
| Matches | `ipv4.config.…`, `ipv6.config.…` and `transport.config.…` | `match.…`, e.g. `source-ip.prefix` and `destination-port.value` |
| IPv6 protocol | `ipv6.config.protocol` | `match.next-header` |
| Actions | `forwarding-action`: `ACCEPT`, `DROP`, `REJECT` | `action`: `accept`, `drop`; `reject` isn't supported |
| Term name and `comment` | Not rendered | `description` and `_annotate_description` |
| Repository tags | Not rendered | `_annotate` on each filter |
| Sequence IDs | 5, 10, 15, …, carried on across filters | 5, 10, 15, …, restarting in each filter |
| `tcp-established` | `"builtin-detail": "TCP_ESTABLISHED"` | <code>"tcp-flags": "ack&#124;rst"</code> |

### Examples

#### Sample policy

The _[sample policy](../generators.md#sample-policy)_ used on every generator page, rendered by `aclgen`.

```yaml title="sample.yaml"
filters:
  - header:
      targets:
        nokiasrl: edge-inbound inet
--8<-- "docs/reference/generators.md:sample-terms"
```

```json title="sample.srl_acl"
[
  {
    "ipv4-filter": {
      "_annotate": "$Id:$ $Date:$ $Revision:$",
      "description": "",
      "entry": [
        {
          "_annotate_description": "Allow SSH from the management network.",
          "action": {
            "accept": {}
          },
          "description": "allow-ssh",
          "match": {
            "destination-port": {
              "value": 22
            },
            "protocol": 6,
            "source-ip": {
              "prefix": "10.0.0.0/24"
            }
          },
          "sequence-id": 5
        },
        {
          "_annotate_description": "Allow SSH from the management network.",
          "action": {
            "accept": {}
          },
          "description": "allow-ssh",
          "match": {
            "destination-port": {
              "value": 22
            },
            "protocol": 6,
            "source-ip": {
              "prefix": "192.168.10.0/24"
            }
          },
          "sequence-id": 10
        },
        {
          "action": {
            "drop": {}
          },
          "description": "default-deny",
          "match": {},
          "sequence-id": 15
        }
      ],
      "name": "edge-inbound"
    }
  }
]
```

## Known Issues

These known issues are included from _[OpenConfig](openconfig.md#known-issues)_.

--8<-- "docs/reference/generators/openconfig.md:known-issues"