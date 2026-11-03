# cgrep

`cgrep` answers queries about the network and service definitions: which tokens contain an address, which addresses or ports a token expands to, and which service tokens contain a port. It reads definition files only; it takes no policy.

It reads definitions from `./def` by default. Use `-d` (`--def`, `--definitions_directory`) to read another directory. `cgrep` does not read `aerleon.yml`.

Results from `-i`, `-t` and `-g` are log lines on stderr, prefixed `INFO:root:`. For `-o`, `-s` and `-p` the header is a log line on stderr and the list is printed on stdout. The examples below show both streams together.

## Flags

```
usage: cgrep [-h] [-d DEFS] [-i IP [IP ...]] [-t TOKEN] [-c OBJ OBJ | -g IP IP |
             -o OBJ [OBJ ...] | -s SVC [SVC ...] | -p PORT PROTO]

c[apirca]grep

options:
  -h, --help            show this help message and exit
  -d, --def, --definitions_directory DEFS
                        Network Definitions directory location. 
  -c, --cmp OBJ OBJ     Compare the two given network definition tokens
  -g, --gmp IP IP       Diff the network objects to which the given IP(s) belong
  -o, --obj OBJ [OBJ ...]
                        Return list of IP(s) contained within the given token(s)
  -s, --svc SVC [SVC ...]
                        Return list of port(s) contained within given token(s)
  -p, --port PORT PROTO
                        Returns a list of tokens containing the given port and protocol

  -i, --ip IP [IP ...]  Return list of definitions containing the IP(s).
                        Multiple IPs permitted.
  -t, --token TOKEN     See if an IP is contained within the given token.
                        Must be used in conjunction with -i/--ip [addr].
```

Options shared with other tools: _[Common Options](index.md#common-options)_.

## Example definitions

The examples on this page run from a directory whose `def/` subdirectory holds this file. See the _[Definitions Spec](../../reference/definitions.md)_ for the file format.

```yaml
networks:
  MGMT:
    values:
      - address: 10.0.0.0/24
      - address: 192.168.10.0/24
  WEB_SERVERS:
    values:
      - address: 10.0.1.10/32
        comment: web1
      - address: 10.0.1.11/32
        comment: web2
  INTERNAL:
    values:
      - name: MGMT
      - name: WEB_SERVERS
      - address: 10.0.0.0/8
services:
  SSH:
    - port: 22
      protocol: tcp
  HTTP:
    - port: 80
      protocol: tcp
  HTTPS:
    - port: 443
      protocol: tcp
  WEB:
    - name: HTTP
    - name: HTTPS
```

## Queries

### Which tokens contain an IP

Lists every token that contains the address, with the path through the tokens that include it.

```bash
cgrep -i 10.0.1.10
```

```
INFO:root:Results for IP: 10.0.1.10
INFO:root:INTERNAL  ['10.0.1.10/32', '10.0.0.0/8']
INFO:root:INTERNAL -> WEB_SERVERS  ['10.0.1.10/32']
INFO:root:
```

### Is an IP in a token

Add `-t` to ask about one token. The result says whether the address is in the token or is _not_ in it.

```bash
cgrep -i 10.0.1.10 -t WEB_SERVERS
```

```
INFO:root:10.0.1.10 is in WEB_SERVERS
INFO:root:
```

```bash
cgrep -i 10.0.1.10 -t MGMT
```

```
INFO:root:10.0.1.10 is _not_ in MGMT
INFO:root:
```

### Compare where two IPs sit

Shows the tokens each address belongs to. Lines starting with `+` are tokens the address is in that the other is not; lines starting with `-` are tokens the other address is in.

```bash
cgrep -g 10.0.0.5 10.0.1.10
```

```
INFO:root:IP: 10.0.0.5
INFO:root:  INTERNAL
INFO:root:+ INTERNAL -> MGMT
INFO:root:- INTERNAL -> WEB_SERVERS
INFO:root:
INFO:root:IP: 10.0.1.10
INFO:root:  INTERNAL
INFO:root:+ INTERNAL -> WEB_SERVERS
INFO:root:- INTERNAL -> MGMT
INFO:root:
```

### List a network token's addresses

```bash
cgrep -o WEB_SERVERS
```

```
INFO:root:WEB_SERVERS:
INFO:root:
['10.0.1.10/32',
 '10.0.1.11/32']
```

### List a service token's ports

```bash
cgrep -s WEB
```

```
INFO:root:WEB:
INFO:root:
['443/tcp',
 '80/tcp']
```

### Which service tokens contain a port

```bash
cgrep -p 443 tcp
```

```
INFO:root:443/tcp:
INFO:root:
['HTTPS',
 'WEB']
```

### Compare two network tokens

```bash
cgrep -c MGMT WEB_SERVERS
```

!!! warning
    `cgrep -c` currently fails with `AttributeError: 'list' object has no attribute 'version'` for every pair of tokens.
