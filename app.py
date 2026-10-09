"""Assess a dataset schema change against documented downstream uses."""

import json

from review_core import InputError, run_cli


def dataset(event):
    if not isinstance(event, dict):
        raise InputError("invalid_event")
    outputs = event.get("outputs")
    if (
        not isinstance(outputs, list)
        or len(outputs) != 1
        or not isinstance(outputs[0], dict)
    ):
        raise InputError("invalid_outputs")
    output = outputs[0]
    namespace, name = output.get("namespace"), output.get("name")
    if not all(isinstance(x, str) and 1 <= len(x) <= 200 for x in (namespace, name)):
        raise InputError("invalid_dataset")
    facets = output.get("facets")
    schema = facets.get("schema") if isinstance(facets, dict) else None
    fields = schema.get("fields") if isinstance(schema, dict) else None
    if not isinstance(fields, list) or not 1 <= len(fields) <= 100:
        raise InputError("invalid_schema")
    found = {}
    for index, field in enumerate(fields):
        if not isinstance(field, dict):
            raise InputError("invalid_field")
        fname, ftype = field.get("name"), field.get("type")
        description = field.get("description", "")
        if (
            not isinstance(fname, str)
            or not 1 <= len(fname) <= 100
            or not isinstance(ftype, str)
            or not 1 <= len(ftype) <= 100
            or not isinstance(description, str)
            or len(description) > 300
            or fname in found
        ):
            raise InputError("invalid_field")
        found[fname] = (ftype, description, index)
    return namespace + "/" + name, found


def adapt(payload):
    if not isinstance(payload, dict):
        raise InputError("invalid_case")
    subject_before, old = dataset(payload.get("before"))
    subject_after, new = dataset(payload.get("after"))
    if subject_before != subject_after:
        raise InputError("dataset_mismatch")
    uses = payload.get("consumers")
    if not isinstance(uses, list) or not 1 <= len(uses) <= 10:
        raise InputError("invalid_consumers")
    consumers = []
    for item in uses:
        if not isinstance(item, dict):
            raise InputError("invalid_consumer")
        name, purpose, columns = (
            item.get("name"),
            item.get("purpose"),
            item.get("columns"),
        )
        if (
            not isinstance(name, str)
            or not 1 <= len(name) <= 100
            or not isinstance(purpose, str)
            or not 1 <= len(purpose) <= 500
            or not isinstance(columns, list)
            or len(columns) > 30
            or any(not isinstance(c, str) or not 1 <= len(c) <= 100 for c in columns)
        ):
            raise InputError("invalid_consumer")
        consumers.append({"name": name, "purpose": purpose, "columns": columns})
    changes, evidence, flags = [], [], []
    for name in sorted(set(old) | set(new)):
        before, after = old.get(name), new.get(name)
        if before and after and before[:2] == after[:2]:
            continue
        changes.append(
            {
                "field": name,
                "before": before[:2] if before else None,
                "after": after[:2] if after else None,
            }
        )
        if before:
            evidence.append(f"before.outputs[0].facets.schema.fields[{before[2]}]")
        if after:
            evidence.append(f"after.outputs[0].facets.schema.fields[{after[2]}]")
        if before and not after:
            flags.append("field_removed")
        elif before and after and before[0] != after[0]:
            flags.append("type_changed")
    if not changes or len(changes) > 50:
        raise InputError("invalid_change_count")
    text = (
        "Dataset: "
        + subject_after
        + "\nSchema changes: "
        + json.dumps(changes, sort_keys=True)
        + "\nDocumented consumers: "
        + json.dumps(consumers, sort_keys=True)
    )
    return {
        "subject": subject_after,
        "text": text,
        "evidence": evidence,
        "flags": flags,
    }


if __name__ == "__main__":
    run_cli(adapt, "impact")
