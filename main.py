"""Compare two dMSA inventories and surface migration changes for review."""
import argparse
import json
from pathlib import Path
from uuid import UUID

FIELDS = ("dn", "predecessor_dn", "migration_state")


def load(path):
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("expected an array of inventory records")
    accounts = {}
    for row in rows:
        key = str(UUID(row["object_guid"].strip()))
        if not key or key in accounts:
            raise ValueError("Empty or duplicate object GUID")
        for field in FIELDS:
            if field not in row:
                raise ValueError(f"Missing inventory field: {field}")
        accounts[key] = row
    return accounts


def diff(before, after):
    return {
        "added": [after[key] for key in sorted(after.keys() - before.keys())],
        "not_observed": [before[key] for key in sorted(before.keys() - after.keys())],
        "changed": [
            {"object_guid": key, "fields": changed}
            for key in sorted(before.keys() & after.keys())
            if (changed := {f: {"before": before[key][f], "after": after[key][f]}
                            for f in FIELDS if before[key][f] != after[key][f]})
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    args = parser.parse_args()
    print(json.dumps(diff(load(args.before), load(args.after)), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
        import sys

        print(f"Invalid input: {exc}", file=sys.stderr)
        raise SystemExit(2) from None
