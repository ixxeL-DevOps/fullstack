---
description: Rules and patterns for writing Mermaid diagrams in this repository's documentation
tags: ["Mermaid", "Diagrams", "Documentation"]
audience: ["LLMs", "Humans"]
categories: ["Reference[90%]"]
---

# Mermaid Diagram Guide

## Supported Diagram Types

Mermaid is rendered natively in:
- **MkDocs** (via `pymdownx.superfences` — configured in `mkdocs.yml`)
- **GitHub** (native support since 2022 — works in `.md` files, issues, PRs)
- **README.md and docs/*.md** — use ` ```mermaid ` fences

---

## Diagram Types and When to Use Them

| Type | Directive | Use for |
|---|---|---|
| Flowchart | `graph TB` / `graph LR` | Architecture, component relationships, data flows |
| Sequence | `sequenceDiagram` | Protocol flows, auth sequences, request/response |
| State | `stateDiagram-v2` | Lifecycle states (pod, ESO, ArgoCD app) |
| Gitgraph | `gitGraph` | Branch strategies |

---

## Syntax Rules

### Flowchart

```mermaid
graph TB
    subgraph Cluster["🖥️ Genmachine (Talos)"]
        ArgoCD["ArgoCD"]
        Traefik["Traefik"]
        Vault["Vault"]
    end

    Git["GitHub\n(source of truth)"] -->|webhook| ArgoCD
    ArgoCD --> Traefik
    ArgoCD --> Vault
```

- Use `TB` (top-bottom) for architecture diagrams; `LR` (left-right) for flows
- Use `subgraph` for logical groupings (clusters, namespaces, layers)
- Node IDs are camelCase; labels can contain spaces and emoji
- Arrow labels: `-->|label|`
- Use `["label"]` for rectangles, `(["label"])` for rounded, `{{"label"}}` for diamonds

### Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant DNS as AdGuard Home
    participant LB as MetalLB
    participant Traefik
    participant App

    User->>DNS: resolve app.talos-genmachine.fredcorp.com
    DNS-->>User: 192.168.1.160
    User->>LB: HTTPS :443
    LB->>Traefik: forward
    Traefik->>App: proxy (TLS terminated)
    App-->>User: response
```

- Use `actor` for external users
- `->>` for solid arrows (requests), `-->>` for dashed (responses)
- Add `participant X as "Label"` to alias long names

---

## Style Guidelines

1. **Keep diagrams focused** — one diagram per concept; don't try to show everything
2. **Use real names** — `vault.talos-genmachine.fredcorp.com` not `my-service`
3. **Subgraphs for clusters** — always wrap cluster components in a labeled subgraph
4. **Minimal labels** — arrow labels should be verbs or protocols, not sentences
5. **Prefer TB for architecture** — left-to-right is better for request flows
6. **Emoji in subgraph labels** — `🖥️`, `☁️`, `🔐` help distinguish cluster types visually

---

## MkDocs Integration

Mermaid blocks in MkDocs Material use this fenced syntax:

````markdown
```mermaid
graph TB
    A --> B
```
````

The `pymdownx.superfences` configuration in `mkdocs.yml` handles rendering:

```yaml
- pymdownx.superfences:
    custom_fences:
      - name: mermaid
        class: mermaid
        format: !!python/name:pymdownx.superfences.fence_code_format
```

No extra JavaScript is needed when using MkDocs Material.

---

## Common Patterns in This Repo

### Traffic Flow (standard)

```mermaid
graph LR
    Client -->|DNS| AdGuard
    AdGuard -->|192.168.1.160| MetalLB
    MetalLB --> Traefik
    Traefik -->|TLS terminated| App
```

### Dual Cluster Overview

```mermaid
graph TB
    subgraph BK["🖥️ Beelink — k0s"]
        B_Traefik["Traefik"] --> B_Vault["Vault"]
        B_Traefik --> B_Auth["Authentik"]
    end
    subgraph GM["🖥️ Genmachine — Talos"]
        G_Traefik["Traefik"] --> G_Vault["Vault"]
        G_Traefik --> G_Auth["Authentik"]
    end
    GitHub["GitHub\n(source of truth)"] -->|ArgoCD sync| BK
    GitHub -->|ArgoCD sync| GM
```

### Secret Sync Flow

```mermaid
sequenceDiagram
    participant ESO as ExternalSecrets Operator
    participant Vault
    participant K8s as Kubernetes Secret
    participant Pod

    ESO->>Vault: fetch secret (k8s auth)
    Vault-->>ESO: secret value
    ESO->>K8s: create/update Secret
    Pod->>K8s: mount Secret
```
