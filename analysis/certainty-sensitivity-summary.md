# Search Certainty And Sensitivity Scaffold

Generated from `extraction/extracted-data.tsv` on 2026-04-29.
This scaffold records sensitivity cuts for later synthesis. It does not assign final certainty to manuscript findings.

## Denominators

- Included search records: 95.
- Architecture records: 85.
- Contextual/boundary records: 10.

## Publication-Status Sensitivity

### Included Records

| Value | N | % |
| --- | ---: | ---: |
| `preprint` | 83 | 87.4% |
| `peer_reviewed` | 12 | 12.6% |

### Architecture Records

| Value | N | % |
| --- | ---: | ---: |
| `preprint` | 76 | 89.4% |
| `peer_reviewed` | 9 | 10.6% |

- Peer-reviewed-only architecture sensitivity retains 9 of 85 records (10.6%).
- Preprint-heavy evidence base: 76 of 85 architecture records are preprints (89.4%).

## Quality Sensitivity

| Value | N | % |
| --- | ---: | ---: |
| `high` | 31 | 36.5% |
| `very_high` | 25 | 29.4% |
| `moderate` | 22 | 25.9% |
| `moderate_low` | 5 | 5.9% |
| `low_retained` | 2 | 2.4% |

### Threshold Cuts

| Quality cut | Retained | Removed | Retained % |
| --- | ---: | ---: | ---: |
| `>= 3.0/6` | 85 | 0 | 100.0% |
| `>= 4.0/6` | 83 | 2 | 97.6% |
| `>= 4.5/6` | 78 | 7 | 91.8% |
| `>= 5.0/6` | 56 | 29 | 65.9% |

- Protocol sensitivity threshold `< 3.0/6` removes zero architecture records.
- Raising the cut to `>= 5.0/6` would retain only the highest-scored 56 architecture records and should be treated as an exploratory robustness check, not the protocol rule.

## Controlled-Comparison Sensitivity

| Value | N | % |
| --- | ---: | ---: |
| `strict_no_persistence_or_memory_ablation` | 56 | 65.9% |
| `broad_external_nonmemory_baseline` | 20 | 23.5% |
| `no_suitable_controlled_comparison` | 9 | 10.6% |

- Strict no-persistence or memory-ablation claims should use 56 of 85 architecture records (65.9%).
- Broad controlled-comparison claims, including external/non-memory baselines, can use 76 of 85 architecture records (89.4%).

## Use Notes

- Architecture taxonomy claims use the full 85-record architecture denominator unless explicitly framed as sensitivity analysis.
- Peer-reviewed-only sensitivity is informative but too restrictive for the main emerging-field synthesis.
- Quality-threshold sensitivity does not alter the corpus under the protocol `< 3.0/6` rule.
- Strict controlled claims and broad comparative claims must keep separate denominators.
