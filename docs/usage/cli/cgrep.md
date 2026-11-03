# cgrep

`cgrep` answers queries about addresses, ports and protocols found in the definition files.

## Flags

```
usage: cgrep [-h] [-d DEFS] [-i IP [IP ...]] [-t TOKEN] [-c OBJ OBJ | -g IP IP | -o OBJ [OBJ ...] | -s SVC [SVC ...] | -p PORT PROTO]

c[apirca]grep

options:
  -h, --help            show this help message and exit
  -d DEFS, --def DEFS   Network Definitions directory location.
  -c OBJ OBJ, --cmp OBJ OBJ
                        Compare the two given network definition tokens
  -g IP IP, --gmp IP IP
                        Diff the network objects to which the given IP(s) belong
  -o OBJ [OBJ ...], --obj OBJ [OBJ ...]
                        Return list of IP(s) contained within the given token(s)
  -s SVC [SVC ...], --svc SVC [SVC ...]
                        Return list of port(s) contained within given token(s)
  -p PORT PROTO, --port PORT PROTO
                        Returns a list of tokens containing the given port and protocol

  -i IP [IP ...], --ip IP [IP ...]
                        Return list of definitions containing the IP(s).
                        Multiple IPs permitted.
  -t TOKEN, --token TOKEN
                        See if an IP is contained within the given token.
                        Must be used in conjunction with -i/--ip [addr].
```

Options shared with other tools: _[Common Options](index.md#common-options)_.
