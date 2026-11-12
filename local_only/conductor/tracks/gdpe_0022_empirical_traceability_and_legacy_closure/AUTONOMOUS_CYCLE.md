# Autonomous Cycle Rules

This template uses a chained Ralph-style Conductor cycle.

## Per-phase loop

For each phase:

1. Complete the phase tasks.
2. Run the Conductor review protocol for the current phase scope.
3. Write `phase_<N>_review.md`.
4. Automatically implement all in-scope recommendations.
5. Re-run the same review.
6. Repeat until:
   - no critical or high findings remain; and
   - any remaining medium or low findings are either fixed or explicitly deferred.
7. Only then proceed.

## Per-track loop

At the end of the track:

1. Confirm local verification is clean.
2. Push the changes remotely.
3. Monitor workflows for the pushed commit until completion.
4. Verify the Streamlit dashboard locally and remotely where configured.
5. Assess flow-on effects.
6. If residual work remains, create the next follow-on track immediately.
7. Update the template reflection log with improvements to the process itself.

## Improvement rounds

Every new track created from this template must run 3 to 5 track-improvement rounds before implementation begins:

1. Ask whether there are improvements recommended for the track.
2. Incorporate them.
3. Repeat.

If operating without a human in the loop, replace the question with a documented self-review round and persist the critique artifact.
