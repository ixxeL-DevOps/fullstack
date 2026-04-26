---
description: Collaborative planning lifecycle — how to scope, design, and validate implementations before writing code
tags: ["Planning", "Process"]
audience: ["LLMs"]
categories: ["Reference[90%]"]
---

# Planning

## Before Writing Any Code

Answer these questions before touching a single file:

1. **Which cluster?** Beelink, genmachine, or both? If both, are the changes independent?
2. **What category?** New app deployment, chart update, secret addition, infrastructure change, documentation?
3. **Does a similar pattern already exist?** Find the nearest existing example and replicate its structure.
4. **What are the dependencies?** Does this app need Vault secrets? A certificate? A storage class? Are those already present?
5. **What AppProject?** Use the assignment table in DOMAIN.md.

---

## Planning Phases

### Phase 1 — Clarify

If the request is ambiguous:
- Ask which cluster before writing manifests
- Ask if an existing pattern should be followed or if this is intentionally different
- Ask if secrets need to be created in Vault first

### Phase 2 — Locate

Before writing, locate:
- The most similar existing app (same type: upstream Helm chart, pure-template chart, etc.)
- The correct `gitops/core/apps/{cluster}/{category}/` directory
- Any required pre-existing resources (namespaces, secrets, storage classes)

### Phase 3 — Plan (list files to create/modify)

State explicitly:
- Files to create (with relative paths)
- Files to modify (and what changes)
- Files NOT to touch (and why — e.g., "coredns is excluded from refactor because it's a Talos built-in")
- Any manual steps required (e.g., "add secret to Vault before deploying")

### Phase 4 — Implement

Follow CONVENTIONS.md for every file written. Use existing files as templates, not this document.

### Phase 5 — Validate

After committing:
- Pre-commit hooks must pass (yamllint, SOPS check, prettier, commitizen)
- Commit message must follow conventional commits format: `{type}({scope}): {description}`
- After PR merge: check the CI manifest diff comment to verify the rendered output matches intent

---

## Commit Message Format

```
{type}({scope}): {short description}

{optional body}

Closes #{issue}
```

Types: `feat`, `fix`, `refactor`, `docs`, `chore`
Scope: app name or area (e.g., `fstrim`, `traefik`, `talos`, `vault`)

Examples:
```
feat(fstrim): add weekly SSD fstrim CronJob for Talos nodes
fix(traefik): correct wildcard certificate secret name
refactor(cert-manager): rename values/ to common/
docs(architecture): add Capsule for CiliumCNI
```

---

## Scope of Changes

When asked to implement something on "both clusters":
1. Implement genmachine first (ApplicationSet pattern — more complex)
2. Implement beelink second (plain Application — simpler, mirrors genmachine)
3. Commit both in one PR unless the changes are independent

When a change touches `common/common-values.yaml`:
- This affects all clusters that include that file
- Verify the change is intentionally shared; if cluster-specific, put it in the cluster values file instead

---

## Red Flags — Stop and Ask

- The request references a cluster by an ambiguous name (e.g., "the cluster", "the server")
- The request would touch `cilium`, `coredns`, or `kubelet-csr-approver` — these have Talos-specific configs and must be handled carefully
- The request involves changing Vault's storage backend or auth methods
- The request asks to commit secrets or credentials
- The request would affect all apps (e.g., changing a shared ApplicationSet generator pattern)
