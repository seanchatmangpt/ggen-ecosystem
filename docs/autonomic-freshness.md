# Autonomic ecosystem freshness

The default branch is not considered fresh merely because a scheduled workflow ran.

The freshness invariant is:

1. Observe every declared direct submodule remote default-branch head.
2. Manufacture a candidate containing only admitted Gitlink and lock-identity changes.
3. Execute the exact candidate through the repository's local Chicago courts.
4. Promote only by a non-forced fast-forward when `origin/main` still equals the observed base SHA.
5. Publish and smoke the exact promoted crown container and bind its digest/run identity into a receipt.
6. If the default branch moved during qualification, refuse promotion and recompute on the next scheduled run.

This keeps freshness automatic without granting the runtime authority to rewrite workflow definitions, bypass validation, or overwrite concurrent changes.
