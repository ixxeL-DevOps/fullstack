---
description: When and how to write or update documentation in this repository
tags: ["Documentation", "Writing", "MkDocs"]
audience: ["LLMs"]
categories: ["Reference[85%]"]
---

# Writing Documentation

## When to Write Documentation

Write or update documentation when:

- A new architectural decision is made that future collaborators need to understand
- A non-obvious operational procedure is established (the "why" would surprise a reader)
- A component's integration with others is complex enough to warrant a diagram
- A hard invariant is added or changed

Do **not** write documentation for:

- Things that are obvious from reading the code
- Temporary states (in-progress work, current PR status)
- Things that will be outdated within days
- Step-by-step walkthroughs of straightforward Helm chart deployments

---

## Documentation Structure

```
docs/
├── index.md                    # Repo homepage (MkDocs)
├── ai-context/                 # AI assistant context files (this directory)
├── argocd/                     # ArgoCD-specific docs
├── authentication/             # OIDC, Authentik docs
├── cluster/                    # Talos, k0s cluster docs
├── secrets/                    # Vault, SOPS, ESO docs
└── assets/                     # Images, diagrams
```

---

## MkDocs Conventions

- All docs use Markdown with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) extensions
- Mermaid diagrams are supported via `pymdownx.superfences` — see `mermaid-diagram-guide.md`
- Admonitions: `> [!NOTE]`, `> [!CAUTION]`, `> [!TIP]` (GitHub-flavored) or `!!! note`, `!!! warning` (MkDocs)
- Tabbed content: `=== "Tab Name"` via `pymdownx.tabbed`
- Code blocks with syntax highlighting: ` ```yaml `, ` ```bash `, etc.

---

## Wisdom Triggers

Write a documentation update when you encounter any of these:

| Trigger                                         | Document in                                             |
| ----------------------------------------------- | ------------------------------------------------------- |
| "Why is this configured this way?"              | A Capsule in ARCHITECTURE.md or the relevant doc file   |
| "This broke because of X undocumented behavior" | DOMAIN.md (invariant) or WORKFLOWS.md (troubleshooting) |
| "You have to do Y before Z or it fails"         | WORKFLOWS.md                                            |
| "This only applies to cluster X not Y"          | ARCHITECTURE.md or CONVENTIONS.md with explicit callout |
| "The naming here is confusing"                  | DOMAIN.md (glossary)                                    |
| A new OIDC integration                          | docs/authentication/oidc.md                             |
| A new certificate pattern                       | docs/secrets/ or NETWORKING.md                          |

---

## Capsule Format

For architectural decisions and system behaviors, use the Capsule format (see `writing-capsules.md`).

For operational procedures, use numbered lists with code blocks.

For reference tables, use Markdown tables with concise entries.

---

## Style Rules

1. **One idea per section** — don't mix "how it works" with "how to configure it" in the same block
2. **Show, don't tell** — include real YAML examples rather than describing the fields abstractly
3. **No filler** — don't start sections with "This section describes..." or "In this document you will find..."
4. **Active voice** — "ArgoCD syncs every 3 minutes" not "The sync interval is configured to be 3 minutes"
5. **Concrete > abstract** — use real hostnames and paths from this repo, not generic placeholders
