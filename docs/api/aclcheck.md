# AclCheck API

`AclCheck()` answers one question: what does a policy do with a given packet? You give it a policy, the definitions the policy refers to, and the packet's addresses, ports and protocol. It returns the terms that match. It is the Python counterpart of the `aclcheck` command, described in _[aclcheck](../usage/cli/aclcheck.md)_.

Examples run from `docs/examples/api/`, because the test harness runs every example from that directory. Run them from that directory if you try them yourself.

## Example

The example checks a packet from `192.168.1.0/24` to `10.0.0.10`, TCP, source port `49152` and destination port `80`. The policy and definitions are plain dictionaries, and the checked packet matches the first term.

```python title="aclcheck_example.py"
--8<-- "docs/examples/api/aclcheck_example.py"
```

??? example "Output"

    ```text title="aclcheck_example.stdout.ref"
    --8<-- "docs/examples/api/aclcheck_example.stdout.ref"
    ```

## Inputs

`AclCheck(input_policy, definitions, src, dst, sport, dport, proto, source_zone, destination_zone)` takes:

- `input_policy`: one policy dictionary, shaped as described in _[Policy Objects](policy_objects.md)_. Pass a single dictionary, not a list.
- `definitions`: a `Naming` object holding the names the policy uses, built as described in _[Definitions (Naming)](definitions.md)_.
- `src`, `dst`: an address or network such as `10.0.0.10` or `192.168.1.0/24`. The default is `"any"`.
- `sport`, `dport`: a port number, as an integer or a string. The default is `"any"`. A service name such as `SSH` is not accepted here and raises an error.
- `proto`: a protocol name such as `tcp`. The default is `"any"`.
- `source_zone`, `destination_zone`: a zone name. The default is `"any"`.

A `None` for `src`, `dst`, `sport`, `dport` or `proto` is treated as `"any"`.

Even though the check does not depend on the platform, the policy must have at least one target in every filter header. `AclCheck()` fails on a header without one (see _[Errors](#errors-and-limits)_ below), while `Generate()` silently renders nothing for it. The first target's filter name is the key you will see in the summary, so `AclCheck()` reports a filter once, even when the header lists several platforms.

## Reading the summary

`AclCheck()` returns a dictionary keyed by filter name. Each value maps a term name to a dictionary with two keys:

- `possibles`: a list of reasons the term only possibly matches. It is empty for an exact match. The reasons are `source-ip` and `destination-ip` (the packet is broader than the term), `first-frag`, `frag-offset`, `packet-length`, `est` and `tcp-est`. The last ones depend on state that `AclCheck()` does not know, such as whether the connection is already established.
- `message`: a short text for people, with the term name and the action. For a possible match it reads `action if [reasons]`. It contains no action field of its own, so a program should not parse it.

Terms are listed in policy order, and the list stops at the first exact match, because later terms cannot be reached. An empty result means that no term matched.

The output in the next section shows real summaries for two packets. The policy's first term is `allow-established`, with the option `tcp-established`, so every TCP packet only possibly matches it, with the reason `tcp-est`. The packets differ in the exact match that follows. The `message` text has a ten-space indent for the term line and a sixteen-space indent for the action line.

## Deciding the outcome

To turn a summary into an answer, collect the conditional matches and then take the action of the exact match that ended the list. The `outcome()` function below does that. The summary has no action field, so it looks up each term's action by name in the policy you passed in, and it does not read the `message` text.

```python title="aclcheck_outcome.py"
--8<-- "docs/examples/api/aclcheck_outcome.py"
```

??? example "Output"

    ```text title="aclcheck_outcome.stdout.ref"
    --8<-- "docs/examples/api/aclcheck_outcome.stdout.ref"
    ```

The first packet, from the management network to port 22, matches `allow-ssh` exactly, so the answer is `accept`, with `accept if ['tcp-est']` as an earlier conditional match. The second packet is from an address outside `MGMT`, so it falls through to `default-deny`. It is denied unless it belongs to an established connection, which the summary shows as `accept if ['tcp-est']`.

The summary key is `edge-inbound`, the first target's filter name. The `edge-in-j` name of the second target does not appear.

## Errors and limits

- A port that is not a number, such as `dport="SSH"`, raises `aerleon.lib.port.BadPortValue` (`port SSH is not valid.`). Convert service names to numbers yourself.
- A name in the policy that the definitions don't provide raises `aerleon.aclgen.ACLParserError`, as with `Generate()`. The first line of its message names the policy. See _[Best Practices](best_practices.md#catch-the-errors-you-can-handle)_.
- `AclCheck()` does not expand includes. A policy that contains an include term fails with `KeyError: 'name'`. Expand the includes first, or check a policy that has none. See _[Includes in the API](includes.md)_.
- A filter header with no targets, whether it is `{"targets": {}}` or has no `targets` key at all, ends in an `IndexError` or a `KeyError` instead of a clear message. Always give the header at least one target.
