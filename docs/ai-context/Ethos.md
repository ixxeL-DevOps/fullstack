---
description: Hard rules and values that govern all AI assistance in this repository
tags: ["Philosophy", "Rules"]
audience: ["LLMs"]
categories: ["Reference[100%]"]
---

# Ethos — Hard Rules

These rules are non-negotiable. Apply them before and after every action.

## The Rules

### 1. Cluster Isolation Is Sacred

Beelink and genmachine are not environments of the same cluster. They are independent infrastructures.
A change for genmachine **never** touches beelink files, and vice versa — unless explicitly asked.
The only shared files are `gitops/manifests/{app}/common/common-values.yaml`.

### 2. GitOps Is the Only Deployment Path

Never suggest `kubectl apply` as a lasting solution. ArgoCD reverts it on next reconciliation (within 3 minutes).
All deployments require: a manifest in `gitops/manifests/` **and** a definition in `gitops/core/apps/`.

### 3. Secrets Never Appear in Plain Text

- Vault is the source of truth for all secrets
- Files containing secrets must end in `.sops.yaml` and be encrypted with Age before commit
- ExternalSecrets pull values from Vault at runtime — never hardcode them in values files
- ClusterSecretStore name is `admin` on both clusters

### 4. Renovate Owns Version Bumps

When pinning an image or chart version, always add the appropriate Renovate comment:

```yaml
# renovate: datasource=docker depName=ghcr.io/someorg/someimage
tag: "v1.2.3"
```

Manual version bumps without Renovate annotations will immediately fall out of automation.

### 5. Don't Invent Conventions — Match Existing Ones

Before writing a new Helm chart, ApplicationSet, or ExternalSecret, look at an existing one.
Follow the exact same structure: Chart.yaml format, value file names, template layout, sync policy options.

### 6. Prefer Minimal Diffs

Do not refactor surrounding code when fixing a bug. Do not add abstractions beyond what the task requires.
A one-line fix should produce a one-line diff. Cleanup belongs in a separate PR.

### 7. Verify Before Declaring Done

A successful `git push` and CI hook pass does not mean ArgoCD synced cleanly.
For significant changes, check the ArgoCD-generated manifest diff comment on the PR before declaring the task done.

### 8. Ask Which Cluster First

If the request is ambiguous about which cluster, ask before writing any code. Making an assumption
and writing the wrong cluster's files wastes more time than a clarifying question.

## Values

- **Reproducibility**: The repo should be the single source of truth. If it can't be derived from Git, it shouldn't exist.
- **Observability**: Prefer solutions that emit metrics (ServiceMonitor, PrometheusRule) and logs.
- **Least privilege**: SecurityContexts should drop capabilities. Privileged containers are exceptional and documented.
- **Automation**: Manual operational steps should be codified as Taskfile tasks.
