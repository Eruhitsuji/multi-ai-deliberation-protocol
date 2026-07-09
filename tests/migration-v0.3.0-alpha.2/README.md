# MADP v0.3.0-alpha.2 Migration Fixtures

These fixtures describe draft migration expectations from `MADP-v0.3.0-alpha.1` material to `MADP-v0.3.0-alpha.2` planning artifacts.

They are intentionally separate from `tests/migration/`, which remains the published alpha.1 migration fixture corpus.

The alpha.2 fixtures are not a complete migration engine. They check conservative invariants for draft alpha.2 features:

- active alpha.1 sessions must not auto-upgrade to alpha.2;
- missing `relay_mode` must default to `DELIBERATION` only as an explicit migration interpretation;
- historical text that resembles `/madp` syntax must not be retroactively treated as an authorized command;
- command, TODO, and external-action authority boundaries must remain explicit.
