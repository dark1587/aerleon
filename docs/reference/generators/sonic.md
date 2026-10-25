# SONiC

Renders ACL sets for [SONiC](https://sonicfoundation.dev/) switches as JSON. The SONiC generator is built on the _[OpenConfig](openconfig.md)_ generator.

## Header Format

```yaml
targets:
    sonic: [filter name] {inet|inet6|mixed}
```

| Option | Description | Notes |
|---|---|---|
| `filter name` | Name of the ACL set. | Rendered as `name` and `config.name`. If it's left out, both render as `null`. |
| `inet` | IPv4 only. | Default. ACL type `ACL_IPV4`. |
| `inet6` | IPv6 only. | ACL type `ACL_IPV6`. |
| `mixed` | IPv4 and IPv6. | ACL type `ACL_MIXED`. Each term is rendered once for IPv4 and once for IPv6. A term with no addresses of one family matches everything in that family; see _[Known Issues](#known-issues)_. |


## Term Format

### Common tokens

These tokens are included from the _[Common](common.md)_ page.

!!! warning "Not supported on SONiC"
    Like OpenConfig, SONiC doesn't support `platform`, `platform-exclude` or `verbatim`. A term that uses any of them raises an error.

--8<-- "docs/reference/generators/common.md:common-tokens"

### Inherited tokens

These tokens are included from the _[OpenConfig](openconfig.md#how-tokens-are-rendered)_ page.

--8<-- "docs/reference/generators/openconfig.md:term-format"

## Actions

### Inherited actions

These actions are included from the _[OpenConfig](openconfig.md#actions)_ page.

--8<-- "docs/reference/generators/openconfig.md:actions"

## Option

| Option | Description | Example | Notes |
|---|---|---|---|
| `tcp-established` | Match established TCP sessions. | `option: tcp-established` | Renders `"tcp-session-established": true` under `transport.config`, instead of OpenConfig's `"detail-mode": "BUILTIN", "builtin-detail": "TCP_ESTABLISHED"`. The term's `protocol` must be exactly `tcp`, otherwise `TcpEstablishedWithNonTcpError` is raised. |

For an example, see [`tcp-established`](#tcp-established).

## Output

Each policy file renders to one file with the same name and a `.oacl` extension, so `sample.yaml` renders `sample.oacl`. OpenConfig uses the same extension, so rendering one policy for both `openconfig` and `sonic` writes both to the same file.

### Examples

#### Sample policy

The _[sample policy](../generators.md#sample-policy)_ used on every generator page, rendered by `aclgen`.

```yaml title="sample.yaml"
filters:
  - header:
      targets:
        sonic: edge-inbound inet
--8<-- "docs/reference/generators.md:sample-terms"
```

```json title="sample.oacl"
[
  {
    "acl-entries": {
      "acl-entry": [
        {
          "actions": {
            "config": {
              "forwarding-action": "ACCEPT"
            }
          },
          "ipv4": {
            "config": {
              "protocol": 6,
              "source-address": "10.0.0.0/24"
            }
          },
          "sequence-id": 5,
          "transport": {
            "config": {
              "destination-port": 22
            }
          }
        },
        {
          "actions": {
            "config": {
              "forwarding-action": "ACCEPT"
            }
          },
          "ipv4": {
            "config": {
              "protocol": 6,
              "source-address": "192.168.10.0/24"
            }
          },
          "sequence-id": 10,
          "transport": {
            "config": {
              "destination-port": 22
            }
          }
        },
        {
          "actions": {
            "config": {
              "forwarding-action": "DROP"
            }
          },
          "sequence-id": 15
        }
      ]
    },
    "config": {
      "name": "edge-inbound",
      "type": "ACL_IPV4"
    },
    "name": "edge-inbound",
    "type": "ACL_IPV4"
  }
]
```

#### `tcp-established`

A term with `option: tcp-established`. SONiC renders it as `tcp-session-established` (see _[Option](#option)_).

```yaml title="established.yaml"
filters:
  - header:
      targets:
        sonic: edge inet
    terms:
      - name: established
        protocol: tcp
        option: tcp-established
        action: accept
```

```json title="established.oacl"
[
  {
    "acl-entries": {
      "acl-entry": [
        {
          "actions": {
            "config": {
              "forwarding-action": "ACCEPT"
            }
          },
          "ipv4": {
            "config": {
              "protocol": 6
            }
          },
          "sequence-id": 5,
          "transport": {
            "config": {
              "tcp-session-established": true
            }
          }
        }
      ]
    },
    "config": {
      "name": "edge",
      "type": "ACL_IPV4"
    },
    "name": "edge",
    "type": "ACL_IPV4"
  }
]
```

## Known Issues

These known issues are included from _[OpenConfig](openconfig.md#known-issues)_.

--8<-- "docs/reference/generators/openconfig.md:known-issues"
