# Definitions Spec

The naming library is used by the Aerleon system to parse definitions of network
and service data. These definitions are based on 'tokens' that are used in the
high-level _[policy language](policy_files.md)_.

## Basic Usage

**Create a directory to hold the definitions files**

```bash
mkdir /path/to/definitions/directory
```

**Create a definition YAML file**

```yaml
cat > /path/to/definitions/directory/definitions.yaml
networks:
  INTERNAL:
    values:
      - address: 10.0.0.0/8
        comment: "RFC1918"
      - address: 172.16.0.0/12
        comment: "RFC1918"
      - address: 192.168.0.0/16
        comment: "RFC1918"
  WEB_SERVERS:
    values:
      - address: 200.3.2.1/32
        comment: "webserver-1"
      - address: 200.3.2.4/32
        comment: "webserver-2"
  MAIL_SERVERS:
    values:
      - address: 200.3.2.5/32
        comment: "mailserver-1"
      - address: 200.3.2.6/32
        comment: "mailserver-2"
services:
  MAIL_SERVICES:
    - name: SMTP
    - name: ESMTP
    - name: SMTP_SSL
    - name: POP_SSL
  SMTP:
    - port: 25
      protocol: tcp
  DNS:
    - port: 53
      protocol: tcp
    - port: 53
      protocol: udp
  HTTP:
    - port: 80
      protocol: tcp
      comment: "web traffic"
  SMTP_SSL:
    - port: 465
      protocol: tcp
  ESMTP:
    - port: 587
      protocol: tcp
  POP_SSL:
    - port: 995
      protocol: tcp
^D
```

**Create a Naming object**

```python
from aerleon.lib import naming
defs = naming.Naming('/path/to/definitions/directory')
```

**Access Definitions From the Naming Object**

```python
defs.GetNet('INTERNAL')
defs.GetService('MAIL')
defs.GetServiceByProto('DNS','udp')
```

## Methods

The methods of `Naming` are rendered in the _[API Reference](../api/reference.md#aerleon.lib.naming.Naming)_.
