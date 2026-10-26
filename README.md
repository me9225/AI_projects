# Venue Agent — Results Report

## Implementations
- **API**: Groq Python client calling the Chat Completions API; the tool loop is implemented in our own harness.
- **SDK**: same Groq Python client package and same shared harness/domain tools. If the assignment means a distinct agent SDK (not the Groq client SDK), clarify this distinction with the instructor.

## Data provenance
- Source: `shared/data/venues.pdf`
- Normalized dataset: `shared/data/venues.json`
- Do not treat demo records as real. Replace them with verified PDF-derived records and preserve `source_page`.

## Scenario
- Scenario definition: `scenario.json`
- Execution output: `results/scenario_results.json`
- Raw measurements: `results/metrics.jsonl`

## Measurements
Run the scenario separately for API and SDK, and report measured values from the generated metrics files. Do not fabricate measurements.

| Implementation | Model calls | Tool calls | Prompt tokens | Completion tokens | Total tokens | Runtime (s) | Estimated cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| API | TODO | TODO | TODO | TODO | TODO | TODO | TODO |
| SDK | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

## Limitations
- Weather calls require network access at runtime; tests should mock HTTP requests.
- Token counts are populated only when the provider returns usage data.
- Costs require verified per-token model pricing; do not infer rates.
- The included venue JSON is demo data until replaced with extracted and verified source data.
