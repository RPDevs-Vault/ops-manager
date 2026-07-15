# ADR-0001: Record Architecture Decisions

## Status
Approved

## Context
We need a structured way to record architectural decisions across the RPDevs-Vault organization. As the system grows to a 9-manager layout, tracking *why* certain designs were chosen becomes vital to prevent regression and maintain system invariants.

## Decision
We will use light-weight Architectural Decision Records (ADRs) formatted in Markdown. These records will live inside `/home/llmuser/projects/managers/thought-manager/adr/` and be sequentially numbered.

## Consequences
- Every major structural shift must have a corresponding ADR.
- Code repositories should link back to relevant ADRs in their files/documentation.
- Future agents can parse this history to retain deep architectural context.
