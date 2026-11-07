# Evidence RAG Studio

**GenAI** · A citation-first document question-answering pipeline with an optional live model adapter.

## Run locally

Python 3.11+; no third-party packages required. From this directory:

```bash
python main.py demo
python main.py run example.json
python -m unittest discover -s tests -v
```

`example.json` is the input contract and contains only synthetic or fictional data. `core.run(payload)` returns a JSON-serializable result. Invalid inputs produce an error and a nonzero CLI exit code.

## What it implements

- Deterministic overlapping text chunking and BM25 retrieval with document/chunk citations.
- Abstains when there is no lexical evidence; local mode returns excerpts, not simulated LLM inference.
- Optional OpenAI chat-completions adapter; sends only selected context and treats retrieved documents as untrusted.
- Bounded document size, retrieved-context budget and explicit provider errors.

## Design and limitations

Offline mode is extractive retrieval, not a generative model. Live mode requires internet, OPENAI_API_KEY and OPENAI_MODEL; API use may cost money. The adapter has unit tests with a mocked HTTP response, not a real provider test. Lexical retrieval is weaker than embeddings for paraphrases. Prompt instructions reduce risk but cannot guarantee injection resistance. Do not send sensitive documents to an external provider without approval.

## Suggested next step

Add your own data and domain-specific acceptance tests. Read and understand the implementation before presenting it in interviews. No live deployment is implied.

<!-- AH-INDEPTH-DOCS:START -->
## In-depth engineering guide

### Problem and scope

A citation-first document question-answering pipeline with an optional live model adapter.

This is an independent runnable reference implementation, with synthetic sample input and explicit limits. It is not a deployed service or independently validated business result.

### Architecture and end-to-end flow

```text
Question → chunk documents → BM25 rank → bounded context → extractive answer or explicit provider call → citations
```

| File | Responsibility |
|---|---|
| core.py | Domain validation and project-specific algorithm/state transitions |
| main.py | Bounded JSON CLI input, demo dispatch and JSON output |
| example.json | Exact reproducible sample input |
| tests/test_core.py | Unit and edge-case coverage |

### Design decisions and trade-offs

1. BM25 is lexical ranking, not embedding-based semantic search. Chunk overlap reduces boundary loss but can repeat evidence. No vector database or neural encoder is implied.

2. The default extractive path requires lexical evidence and abstains when retrieval cannot support an answer. Source and chunk identifiers preserve provenance; this is not a guarantee that a generative provider will obey citation instructions.

3. Live generation is opt-in. OPENAI_API_KEY and OPENAI_MODEL are read from the environment only. The adapter targets the OpenAI chat-completions endpoint with a 30-second timeout; tests mock the provider and validate the target/header without real credentials.

### Reproducible setup

Requires Python 3.11+ and no third-party Python packages. Run from this project folder:

```bash
python main.py demo
python main.py run example.json
python -m unittest discover -s tests -v
```

CLI inputs are JSON objects, bounded to 1 MB. Supported domain errors produce a JSON error on stderr and a nonzero exit; inspect the message rather than treating a failed run as a result. The demo does not require a model key, network access or production data.

### Exact example input

```json
{
  "mode": "extractive",
  "question": "How are snapshot blocks protected?",
  "documents": [
    {
      "id": "storage-notes",
      "text": "Snapshot blocks are immutable. CRC32 checksums detect accidental corruption. Named snapshots retain block references."
    },
    {
      "id": "web-notes",
      "text": "The booking API rejects conflicting room reservations."
    }
  ]
}
```

### Core implementation interfaces

| Callable | Boundary |
|---|---|
| `tokens(s)` | Implementation boundary; see source for validation and return structure. |
| `chunks(doc, size=90, overlap=20)` | Implementation boundary; see source for validation and return structure. |
| `generate(question, context)` | Implementation boundary; see source for validation and return structure. |
| `run(p)` | Implementation boundary; see source for validation and return structure. |

The Python `run` result is JSON-serializable. Inspect the source and `main.py run example.json` output for the exact return keys; do not assume another project’s result schema.

### Test coverage and reproducibility

- `tests/test_core.py::test_evidence`
- `tests/test_core.py::test_abstain`
- `tests/test_core.py::test_duplicate_ids`
- `tests/test_core.py::test_unknown_mode`
- `tests/test_core.py::test_live_adapter`
- `tests/test_core.py::test_provider_request_target`

6 named tests are present in this folder. Run the command above to reproduce the local test results. Provider calls are mocked; Docker build/run was not executed; no real cloud/model/production-cluster validation is claimed.

### Security and failure boundaries

Offline mode is extractive retrieval, not a generative model. Live mode requires internet, OPENAI_API_KEY and OPENAI_MODEL; API use may cost money. The adapter has unit tests with a mocked HTTP response, not a real provider test. Lexical retrieval is weaker than embeddings for paraphrases. Prompt instructions reduce risk but cannot guarantee injection resistance. Do not send sensitive documents to an external provider without approval.

Never commit .env, real API keys, runtime databases, approval material or customer data. See SECURITY.md. A successful example demonstrates the included workflow, not safe internet deployment.

### Troubleshooting

- **Import error:** run from this project’s own folder; each project intentionally has its own core.py.
- **Invalid sample/schema:** start from example.json, then change one field at a time and read the returned validation message.
- **Port already in use:** stop the previous process or select another --port where server.py exists.
- **SQLite lock/state surprise:** close duplicate processes, confirm PROJECT_DB and back up before deliberate resets. Do not delete unrelated project data.
- **External dependency unavailable:** default demos run offline; live provider calls and container pulls require your own working access and may incur external costs.

### Known limitations

Offline mode is extractive retrieval, not a generative model. Live mode requires internet, OPENAI_API_KEY and OPENAI_MODEL; API use may cost money. The adapter has unit tests with a mocked HTTP response, not a real provider test. Lexical retrieval is weaker than embeddings for paraphrases. Prompt instructions reduce risk but cannot guarantee injection resistance. Do not send sensitive documents to an external provider without approval.

### Extension roadmap — not implemented

Replace lexical retrieval with measured hybrid retrieval and add groundedness evaluation; implement rate limiting and structured provider errors before public use.
<!-- AH-INDEPTH-DOCS:END -->
