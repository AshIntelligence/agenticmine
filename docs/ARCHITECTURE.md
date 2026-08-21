# Architecture

## Shared principles

1. **Decompose before prompting.** Different operations have different failure modes.
2. **Retrieve/tool first; synthesize second.** Fluent output is not evidence.
3. **Persist observable artifacts.** Traces and evals should survive the model call.
4. **Keep consequential actions gated.** The prototype can recommend; approval boundaries stay explicit.
5. **Design for model/provider failure.** Mock mode lets architecture and orchestration remain testable without an API.

## Document Intelligence

```mermaid
flowchart LR
    U[User question] --> I[Document ingestion]
    I --> C[Chunking]
    C --> R[BM25Lite retriever]
    R --> E[Evidence chunks + IDs]
    E --> L[Claude synthesis]
    L --> A[Grounded answer]
    A --> V[Citation coverage eval]
    R --> T[JSONL trace]
    L --> T
    V --> T
```

The local lexical retriever is intentional: it keeps the retrieval boundary simple, debuggable, deterministic, and replaceable by hybrid/vector retrieval later.

## Research / Job Discovery

```mermaid
flowchart LR
    Q[Search intent] --> D[Candidate discovery]
    D --> J[Job candidates]
    R[Resume evidence] --> M[Requirement matching]
    J --> M
    M --> G[Gap analysis]
    Q --> S[Query relevance]
    G --> F[Fit score]
    S --> K[Combined ranking]
    F --> K
    K --> X[Explanation + evidence/gaps]
```

Candidate-fit coverage and current query relevance are intentionally separate metrics.

## Product / Technical Design

```mermaid
flowchart TD
    B[Product brief] --> D[Discovery agent]
    D --> A[Architecture agent]
    A --> E[Evaluation agent]
    E --> R[Red-team agent]
    R --> O[Structured product design]
    O --> S[Schema eval]
```

Each stage has a distinct objective: user/problem clarity, system boundaries, measurable behavior, and failure discovery/control boundaries.
