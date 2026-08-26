# Architecture

## Choices I reuse

1. Break work into stages when the stages fail differently.
2. Retrieve or call tools before asking a model to synthesize an answer.
3. Keep traces and eval results outside the model call so they can be reviewed later.
4. Put approval around high-impact actions instead of relying on model confidence alone.
5. Keep a deterministic mode so the orchestration can still be tested when a model provider is unavailable.

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

The local lexical retriever keeps retrieval easy to test and easy to replace later with hybrid or vector search.

## Research / Job Discovery

```mermaid
flowchart LR
    Q[Search intent] --> D[Role discovery]
    D --> J[Role options]
    R[Experience profile] --> M[Requirement matching]
    J --> M
    M --> G[Gap analysis]
    Q --> S[Query relevance]
    G --> F[Fit score]
    S --> K[Combined ranking]
    F --> K
    K --> X[Explanation + evidence/gaps]
```

Fit coverage and query relevance stay separate because they answer different questions.

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

The stages separate problem definition, architecture, evaluation and failure analysis instead of asking one model response to do all four jobs.
