---
description: Format and rules for writing Capsule documentation units
tags: ["Documentation", "Capsule", "Format"]
audience: ["LLMs"]
categories: ["Reference[100%]"]
---

# Writing Capsules

## What Is a Capsule?

A Capsule is a self-contained documentation unit for a system behavior, architectural invariant, or integration pattern. Capsules are the primary documentation format in `ARCHITECTURE.md` and similar files.

A Capsule answers: **What is always true here, and why does it matter?**

---

## Capsule Format

```markdown
### Capsule: {PascalCaseName}

**Invariant**
One or two sentences stating what is always true. Be specific and falsifiable.
//BOUNDARY: (optional) The edge condition where this invariant can break.

**Example**
A concrete instance of the invariant in action. Use real code or real hostnames.

**Depth**

- Distinction: What makes this different from a naive assumption
- Trade-off: What you give up to maintain this invariant
- NotThis: A common mistake or misconception about this pattern
- Critical: (optional) A fact that would cause outages if ignored
- SeeAlso: Related Capsule names (comma-separated)
```

---

## Rules

1. **Name is PascalCase** and descriptive: `ExternalSecretSync`, `TraefikIngress`, `DualClusterIsolation`
2. **Invariant is falsifiable** — a reader should be able to test whether it holds
3. **Example is concrete** — use actual paths, hostnames, resource names from this repo
4. **Depth is a list** — not prose. Each bullet is one terse thought.
5. **SeeAlso links Capsules by name** — not by file path; Capsules are looked up by name
6. **No fluff** — if a Capsule needs more than ~15 lines, split it or move detail to prose

---

## When to Write a Capsule

Write a Capsule when:

- You need to explain something that would surprise an experienced Kubernetes user
- You are documenting a cross-cutting concern that affects multiple files
- You are establishing an invariant that must not be broken

Do **not** write a Capsule for:

- Simple YAML configuration — a code block with comments is enough
- Something that is obvious from the Kubernetes docs
- A one-off procedure — use a numbered list in WORKFLOWS.md instead

---

## Example

```markdown
### Capsule: ExternalSecretSync

**Invariant**
ExternalSecrets pull values from HashiCorp Vault; Kubernetes Secrets populate before pods start.
ClusterSecretStore is named `admin` on both clusters.
//BOUNDARY: A missing Vault entry blocks ExternalSecret sync and blocks pod startup.

**Example**
`ExternalSecret` in `gitops/manifests/wireguard/genmachine/templates/externalsecret.yaml` references
store `admin`, path `wireguard/oidc/genmachine`; at sync the operator creates a Kubernetes Secret;
the pod mounts it via `secretRef`.

**Depth**

- Distinction: Vault is the source of truth; Kubernetes Secrets are ephemeral caches
- Trade-off: More indirection vs repo stays public with no embedded secrets
- NotThis: Do not hardcode secrets in values files — even base64-encoded
- Critical: Vault must be unsealed for ExternalSecrets to sync on cluster restart
- SeeAlso: `VaultPKI`, `SOPSEncryption`
```
