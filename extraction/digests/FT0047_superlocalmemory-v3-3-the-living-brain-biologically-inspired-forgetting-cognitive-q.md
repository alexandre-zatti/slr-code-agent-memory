# SuperLocalMemory V3.3

## Identifiers

- Included ID: I088
- Full-text ID: FT0047
- Extraction key: `bhardwaj2026superlocalmemory`
- Role: `architecture`
- Architecture status: `arch_persistent_workspace_state`
- Architecture denominator decision: `include_architecture`

## Evidence Role

Architecture record extracted from the paper text.

## Key Extracted Facts

- Architecture status: `arch_persistent_workspace_state`.
- Storage: local SQLite/sqlite-vec databases for memories, learning state, and code graph, with active/warm/cold/archive quantization tiers.
- Retrieval/control: FRQAD retrieval combines semantic, keyword, entity graph, temporal, spreading activation, consolidation, and Hopfield-style channels with lifecycle hooks and forgetting/consolidation.
- Evaluation: FRQAD retrieval tests, LoCoMo Mode A/Mode C, system/package evidence, and comparison to V3.2.
- Main result: FRQAD mixed-precision retrieval reports 100% precision versus 85.6% for cosine retrieval; LoCoMo Mode A zero-LLM accuracy is 70.4%.
- Cost/token reporting: `sim_parcial`; the paper emphasizes zero-LLM local operation but does not report monetary per-task cost.

## Denominator Notes

- Controlled-comparison status: `pending_extraction`.
- Extraction verification status: `verified_from_full_text`.
- Quality score should be read from `extraction/extracted-data.tsv`.

## Source Files

- PDF text: `search/full-texts/text/FT0047_TA00247_superlocalmemory-v3-3-the-living-brain-biologically-inspired-forgetting-cognitiv.txt`
- JSON: `extraction/json/FT0047_superlocalmemory-v3-3-the-living-brain-biologically-inspired-forgetting-cognitive-q.json`
