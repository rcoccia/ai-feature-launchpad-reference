# Glossary — Control Tower

Quick reference for the method's ubiquitous language. Canonical source: `framework/doctrine/MANIFESTO.md` §3.

| Term | Meaning |
|---|---|
| **Tower** | The AI copilot (this method), under human command, that builds the software system aligned to the governing artifacts. May delegate bounded execution to sub-agents. |
| **Human / Architect** | The person in command: owns Vision, Constraints, and Roadmap; selects and approves features; resolves strategic choices. |
| **Governing artifacts** | Vision (Mission), Constraints, and Roadmap — the truth every decision and implementation must stay aligned to. |
| **Execution sub-agent (worker)** | A bounded coding or testing task the tower delegates; an execution detail, never a peer that redefines strategy. |
| **Feature / Slice** | The atomic unit of governed advancement, driven through select → design → plan → code → test. |
| **Specification** | The design/contract produced for a feature before implementing it. |
| **Constraint** | A declared technical, functional, or non-functional requirement that gates features. |
| **Knowledge Base** | The versioned set of tower artifacts (vision, constraints, roadmap, plans, gap register, baseline, session state, decisions, diagnostics). |
| **Eval harness** | The validation environment that proves behavior without hosting it. |
| **Golden set** | Curated reference framework/examples/transcripts used for regression. |
| **Handoff** | The implementation-ready package for a feature (may go to a delegated coding sub-agent). |
| **Promotion / Block** | The decision to accept a feature or send it back and record the gap. |
| **Deterministic runtime** | The tool/code layer that produces artifacts reproducibly and fail-closed. |
| **Semantic review** | Human-like judgment of completeness and drift-from-artifacts / invention risk. |
