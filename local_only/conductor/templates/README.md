# Conductor Templates

This directory holds reusable Conductor templates for recurring track patterns.

## Available templates

- `nature_depth_cycle/`
  - A chained, nature-grade repository improvement template for one aspect of the repo at a time.
  - Designed for use across Codex, Gemini CLI, and Qwen Code.
  - Uses Ralph-loop style repeated improvement, Conductor review gates, automatic in-scope remediation, remote push discipline, workflow verification, and Streamlit app verification.
  - Can be instantiated with `python -m scripts.create_nature_depth_track ...`.
  - Seeds handoff and review artifacts so another coding agent can resume without hidden context.

## Template use rule

When creating a new track from one of these templates:

1. Copy the template structure into `conductor/tracks/<track_id>/`.
2. Replace placeholder values with the chosen repository aspect, current evidence, and current risk surface.
3. Run the track-specific refinement loop before implementation starts.
4. At track close-out, create the next follow-on track if material residual work remains.
5. Update the template's reflection log if the completed track revealed a better pattern.
