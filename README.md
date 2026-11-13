# dMSA Change Review

Identify changes in delegated Managed Service Account inventories.

## Quick start

Use Python 3.10 or newer. The CLI runs locally with the standard library. From the repository root, run:

```sh
python3 main.py before.json after.json
```

The sample reports one account whose predecessor and migration state changed. The stable GUID ties both records to the same object.

## Input and output

| Input | Format | Output or purpose |
| --- | --- | --- |
| Before and after | JSON arrays with `object_guid`, `dn`, `predecessor_dn`, `migration_state` | Added, absent and changed records |
| `object_guid` | Stable identifier unique within each snapshot | Joins records even after a rename |

Results are JSON on stdout. Redirect to a file when you want to save the review.

## Interpreting results

Capture equivalent directory scopes and keep both snapshots. An absent object is an observation, not proof of deletion. Investigate unexpected links against approved changes and directory audit logs. DN and state values are compared as exported.

## Troubleshooting

- Use the included fixture first to confirm the command and working directory.
- Check the input path and required fields if the CLI exits with status 2.
- Keep real assessment exports and generated reports in your private workspace.

## Verify locally

```sh
python3 -m unittest discover -s tests -v
```
