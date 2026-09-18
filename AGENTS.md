# Repository map

This repository is an ASO screenshot skill, not an app. Keep changes small and
preserve the four-principle constitution in [SKILL.md](SKILL.md).

- [CLAUDE.md](CLAUDE.md): architecture and renderer boundaries.
- [Layout and state contract](references/layouts-and-state.md): choose compositions and persist progress.
- [Sketch workflow](references/sketch-template-workflow.md): editable generation and localization.
- [Raster workflow](references/raster-workflow.md): scaffold, enhancement, finalization.
- [QA](references/localization-and-qa.md): visual and export acceptance criteria.
- [Constitution evaluations](evals/constitution.md): behavioral evaluation protocol.

Install `requirements.txt`, then run `python check.py` before finishing a change.
For a user's screenshot project, run `python check.py --state /path/to/screenshots/aso-state.json`.
Mechanical checks do not establish visual appeal, factual claim validity, or
conversion lift. Record visual review evidence separately.
