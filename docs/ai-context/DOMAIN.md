---
description: Domain glossary, naming rules, hard invariants, and state machines
tags: ["Domain", "Glossary", "Invariants"]
audience: ["LLMs", "Humans"]
categories: ["Reference[100%]"]
---

# Domain

## Glossary

| Term | Definition |
|---|---|
| **genmachine** | The Talos-based 3-node Kubernetes cluster running on Proxmox VMs |
| **beelink** | The k0s-based single-node Kubernetes cluster on bare-metal BeeLink hardware |
| **talconfig.yaml** | Talhelper input file that generates per-node Talos machineconfigs |
| **talhelper** | CLI tool that renders `talconfig.yaml` into Talos machineconfig YAML |
| **ApplicationSet** | ArgoCD resource that generates multiple Applications from a template + generator |
| **Application** | ArgoCD resource defining a single app's source, destination, and sync policy |
| **AppProject** | ArgoCD resource scoping allowed sources, destinations, and cluster resources |
| **common/** | Directory holding Helm values shared across all clusters for an app |
| **ExternalSecret** | ESO CRD that pulls a secret from Vault and creates a Kubernetes Secret |
| **ClusterSecretStore** | ESO CRD defining how to connect to Vault; always named `admin` |
| **SOPS** | Secrets Operations tooling; files ending in `.sops.yaml` are Age-encrypted |
| **Age** | Asymmetric encryption algorithm used by SOPS for secret files |
| **Capsule** | A structured documentation unit with Invariant, Example, Depth sections |
| **Renovate** | Bot that opens PRs to update versions; driven by inline `# renovate:` comments |
| **tuppr** | Talos/k8s upgrade controller replacing system-upgrade-controller |
| **wg-portal** | WireGuard Portal — web UI for managing WireGuard VPN users and peers |
| **Authentik** | Self-hosted OIDC identity provider; source of OIDC tokens for all apps |
| **fredcorp.com** | Internal domain; all services live under `*.{cluster-domain}.fredcorp.com` |

---

## Hard Invariants

These are facts that must not be violated when making changes:

1. **Two clusters, no shared code** — `common/` values are the only exception
2. **ArgoCD reverts `kubectl apply`** within 3 minutes; only Git changes persist
3. **Secrets in Git = SOPS-encrypted** — the pre-commit hook enforces this
4. **ClusterSecretStore is always named `admin`** — hardcoded in all ExternalSecret templates
5. **Renovate owns version pins** — do not bump without a `# renovate:` annotation
6. **Talos nodes are all control-plane** — `allowSchedulingOnControlPlanes: true`; there are no dedicated worker nodes
7. **Both clusters are independent ArgoCD instances** — no multi-cluster ArgoCD; each cluster manages itself
8. **Vault PKI is the only certificate authority** — cert-manager issuer is `fredcorp-ca` on both clusters

---

## Naming Rules

### Clusters

| Identifier | Beelink | Genmachine |
|---|---|---|
| ArgoCD cluster name | `beelink` | `genmachine` |
| Directory name | `beelink/` | `genmachine/` |
| Values file | `beelink-values.yaml` | `genmachine-values.yaml` |
| DNS subdomain | `k0s-fullstack.fredcorp.com` | `talos-genmachine.fredcorp.com` |
| Vault k8s auth mount | `beelink-k8s` | `genmachine` |

### Applications

- ArgoCD Application name: `{app}-{cluster}` (e.g., `traefik-genmachine`)
- Helm release name: always matches app name (e.g., `traefik`)
- Namespace: matches app name unless app lives in a shared namespace (e.g., `kube-system`)
- Vault path: `{app}/{secret-type}/{cluster}` (e.g., `wireguard/oidc/beelink`)

---

## State Machines

### ExternalSecret Lifecycle

```
Created → Pending
    │
    ▼
Vault reachable? ──No──► Error (blocks pod startup)
    │
   Yes
    ▼
Path exists in Vault? ──No──► Error
    │
   Yes
    ▼
K8s Secret created → Ready
    │
    ▼
Refreshed every 12h
```

### ArgoCD Application Lifecycle

```
ApplicationSet detects new directory
    │
    ▼
Application created (OutOfSync)
    │
    ▼
Helm rendered → diff computed
    │
    ▼
Resources applied (ServerSideApply)
    │
    ▼
Synced (Healthy)
    │
    ▼ [any drift]
OutOfSync → selfHeal → re-sync
```

### Talos Node Upgrade (via tuppr)

```
tuppr detects new Talos/k8s version
    │
    ▼
Cordon node
    │
    ▼
Apply new machineconfig / upgrade
    │
    ▼
Node reboots
    │
    ▼
Uncordon node
    │
    ▼ [next node]
Repeat (rolling)
```

---

## AppProject Assignment Rules

| App type | Project |
|---|---|
| CNI, DNS, core k8s | `infra-core` |
| Ingress, LB, VPN, DNS UI | `infra-network` |
| Secrets, PKI, OIDC, policy | `infra-security` |
| CSI drivers, object store, backup | `infra-storage` |
| Dashboards, runners, operators, fstrim | `infra-tools` |
| Prometheus, Grafana, Loki, metrics | `monitoring` |
| ArgoCD bootstrap | `argocd` |
