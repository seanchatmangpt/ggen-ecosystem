# How-to: route a failed manufacture

Attach the exact consumer SHA, GGen identity, marketplace SHA, capsule digest, pack,
receipt, replay result, generated path, and workflow URL to every report.

| Observation | Owner | Required action |
|---|---|---|
| Invalid or incomplete consumer intent | Consumer | Repair authored ontology/manifest; regenerate |
| Duplicate generated path | Pack + consumer | Resolve ownership; do not hand-edit output |
| Marketplace SHA or pack gate refusal | Marketplace | Repair or qualify the reusable pack |
| GGen parser/engine failure | GGen | Reproduce against exact producer identity |
| Image pull, architecture, or digest failure | Ecosystem transport | Repair capsule publication and release metadata |
| Non-identical second generation | Producer/pack | Refuse release; preserve both outputs for diagnosis |
| Missing or invalid receipt | Workflow/evidence | Repair evidence binding before merge |

No issue is considered closed from a green local test alone. The exact GitHub head,
consumer consequence, and replay status must be recorded.
