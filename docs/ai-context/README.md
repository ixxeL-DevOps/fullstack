---
description: Navigation guide for AI context documentation — start here before any task
tags: ["Navigation", "Overview"]
audience: ["LLMs"]
categories: ["Reference[100%]"]
---

# AI Context — Navigation

This directory provides structured context for AI assistants (Claude and others) working on this repository. Read the documents relevant to your task before planning or executing changes.

## Document Map

| Document | When to Read |
|---|---|
| **ARCHITECTURE.md** | Always — cluster topology, app inventory, GitOps patterns |
| **CONVENTIONS.md** | Before writing or editing any Helm chart, ApplicationSet, or manifest |
| **NETWORKING.md** | When touching ingress, DNS, certificates, VPN, or OIDC |
| **DOMAIN.md** | For naming rules, glossary, and hard invariants |
| **WORKFLOWS.md** | When deploying a new app, updating a chart, or troubleshooting |
| **TOOLS.md** | Before running CLI commands — Taskfile tasks, talosctl, kubectl |
| **PLANNING.md** | Before starting a multi-step implementation |
| **writing-capsules.md** | When writing or updating capsule-format documentation |
| **mermaid-diagram-guide.md** | When writing Mermaid diagrams for docs/ |

## Critical Facts (Read Before Everything Else)

1. **Two independent clusters**: `genmachine` (Talos, 3-node Proxmox VMs) and `beelink` (k0s, bare-metal single node). No shared code between them except `gitops/manifests/{app}/common/`.

2. **GitOps is the only path**: ArgoCD reconciles every 3 minutes. `kubectl apply` creates drift and gets reverted. All changes go through Git.

3. **Secrets via Vault + ExternalSecrets**: No hardcoded secrets in manifests. Vault is source of truth. SOPS-encrypted files (`*.sops.yaml`) are encrypted with Age before commit.

4. **Renovate manages versions**: Pin versions with a `# renovate:` comment so Renovate picks them up. Never bump versions manually without checking the Renovate datasource annotation.

5. **Cluster-specific directories**: `genmachine/` uses ApplicationSets (one ApplicationSet covers all cluster env dirs). `beelink/` uses plain ArgoCD Applications.
