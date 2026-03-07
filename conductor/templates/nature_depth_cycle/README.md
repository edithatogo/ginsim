# Nature-Depth Cycle Template

This template is for a single Conductor track that takes one repository aspect through a full improvement cycle:

1. deep exploration;
2. Nature-level sophistication audit;
3. planning;
4. implementation;
5. Conductor review pass;
6. automatic in-scope remediation;
7. local and remote verification;
8. push to remote;
9. workflow monitoring;
10. flow-on effect assessment;
11. creation of the next follow-on track.

It is deliberately tool-agnostic and written so it can be used by Codex, Gemini CLI, and Qwen Code without relying on agent-specific slash commands.

## Included files

- `spec.template.md`
- `plan.template.md`
- `metadata.template.json`
- `AUTONOMOUS_CYCLE.md`
- `TRACK_CLOSEOUT.template.md`
- `TEMPLATE_REFLECTION_LOG.md`

## Intended use

Use this template when the repo still contains non-trivial sophistication, completeness, traceability, UX, or deployment debt and the right operating pattern is:

- one aspect at a time;
- deep review before implementation;
- repeated improvement loops;
- strong verification gates;
- explicit chaining into the next track.

## Generator

Instantiate a real track from this template with:

```bash
python -m scripts.create_nature_depth_track \
  --track-id gdpe_00xx_example \
  --title "Example title" \
  --aspect "single repository aspect"
```

After generation:

1. add the track to `conductor/tracks.md`;
2. run the 3 to 5 refinement rounds before implementation;
3. only then start the phase loop.
