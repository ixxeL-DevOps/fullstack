---
description: Dual-cluster GitOps architecture — topology, application inventory, GitOps patterns, storage, secrets, and bootstrap
tags: ["GitOps", "ArgoCD", "DualCluster", "Talos", "k0s", "ExternalSecrets", "Vault"]
audience: ["LLMs", "Humans"]
categories: ["Architecture[100%]", "Reference[90%]"]
---

# Dual-Cluster Homelab Architecture

## Core Pattern

### Capsule: DualClusterIsolation

**Invariant**
Genmachine and Beelink clusters are independent; no shared code except `gitops/manifests/{app}/common/`.

**Example**
Genmachine configuration lives in `infra/talos/genmachine/` and `gitops/manifests/{app}/genmachine/`;
Beelink lives in `infra/k0s/` and `gitops/manifests/{app}/beelink/`; changes to one never affect the other.
//BOUNDARY: No automatic sync between clusters; any cross-cluster change requires explicit manual action.

**Depth**

- Distinction: Not environments or branches — completely separate hardware and OS distributions
- Beelink: single bare-metal node running k0s v1.32.2 with KubeRouter CNI
- Genmachine: 3 Proxmox VMs running Talos v1.12.7 / Kubernetes v1.36.0 with Cilium CNI
- Trade-off: Duplicate configuration for safety vs shared code for consistency
- NotThis: They don't share namespaces, ArgoCD instances, or Vault mounts
- Critical: Always confirm which cluster before writing any manifest
- SeeAlso: `GitOpsReconciliation`, `ClusterOrganization`

---

### Capsule: GitOpsReconciliation

**Invariant**
Cluster state converges to match Git; ArgoCD reverts manual changes on next sync (within 3 minutes).
Deployment requires **both**: a manifest in `gitops/manifests/` **and** an ArgoCD definition in `gitops/core/apps/`.

**Example**
Push `gitops/manifests/traefik/genmachine/genmachine-values.yaml`; ArgoCD detects the change, renders the Helm chart,
and applies the diff. A `kubectl edit` on the same resource gets overwritten on next reconciliation.

**Depth**

- Distinction: GitOps is declarative (desired state in Git); `kubectl` is imperative
- Trade-off: Consistency and auditability vs immediate manual changes
- NotThis: `kubectl apply` bypasses GitOps and creates drift — do not use for lasting changes
- Timing: ArgoCD reconciles every 3 minutes; also triggers on Git push via webhook
- SeeAlso: `ApplicationSetPattern`, `HelmChartConvention`

---

### Capsule: ExternalSecretSync

**Invariant**
ExternalSecrets pull values from HashiCorp Vault; Kubernetes Secrets populate before pods start.
ClusterSecretStore is named `admin` on both clusters.

**Example**
An `ExternalSecret` in `gitops/manifests/wireguard/genmachine/templates/externalsecret.yaml` references
`admin` store, path `wireguard/oidc/genmachine`; at sync time the operator fetches the value from Vault
and creates a Kubernetes Secret; the pod mounts it via `secretRef`.
//BOUNDARY: A missing Vault entry blocks ExternalSecret sync and blocks pod startup.

**Depth**

- Auth: Kubernetes service account auth; mount paths are `beelink-k8s` (Beelink) and `genmachine` (Genmachine)
- Role: `eso`, ServiceAccount: `eso-auth` in `external-secrets` namespace
- CA: Injected from cert-manager Bundle `fredcorp-ca-chain` (bundle.chain/inject label on namespace)
- Path convention: `{app}/{secret-type}/{cluster}` — e.g., `wireguard/oidc/beelink`
- SeeAlso: `VaultPKI`, `SOPSEncryption`

---

## Cluster Topology

| Aspect            | Beelink (k0s)                     | Genmachine (Talos)                   |
| ----------------- | --------------------------------- | ------------------------------------ |
| **Hardware**      | Bare-metal BeeLink mini-PC        | 3× Proxmox VMs                       |
| **OS / Distro**   | k0s v1.32.2                       | Talos v1.12.7                        |
| **Kubernetes**    | v1.32.2                           | v1.36.0                              |
| **CNI**           | KubeRouter                        | Cilium                               |
| **Load Balancer** | MetalLB                           | MetalLB                              |
| **Nodes**         | 1 (192.168.1.190)                 | 3 (192.168.1.151-153, VIP .150)      |
| **Traefik IP**    | 192.168.1.191                     | 192.168.1.160                        |
| **DNS domain**    | `*.k0s-fullstack.fredcorp.com`    | `*.talos-genmachine.fredcorp.com`    |
| **ArgoCD URL**    | argocd.k0s-fullstack.fredcorp.com | argocd.talos-genmachine.fredcorp.com |
| **Vault URL**     | vault.k0s-fullstack.fredcorp.com  | vault.talos-genmachine.fredcorp.com  |

---

## Application Inventory

### Genmachine (Talos) — ApplicationSets

| App                    | Namespace          | AppProject     | Notes                                   |
| ---------------------- | ------------------ | -------------- | --------------------------------------- |
| cilium                 | kube-system        | infra-core     | CNI; deployed at bootstrap via helmfile |
| coredns                | kube-system        | infra-core     | Cluster DNS                             |
| kubelet-csr-approver   | kube-system        | infra-core     | Auto-approves kubelet CSRs              |
| metrics-server         | kube-system        | infra-tools    | Resource metrics                        |
| spegel                 | spegel             | infra-storage  | Distributed OCI image mirror            |
| metallb                | metallb-system     | infra-network  | L2 load balancer                        |
| traefik                | traefik            | infra-network  | Ingress controller                      |
| adguard                | adguard            | infra-network  | DNS / ad-blocking                       |
| cert-manager           | cert-manager       | infra-security | TLS certificates via Vault PKI          |
| external-secrets       | external-secrets   | infra-security | ESO pulling from Vault                  |
| kyverno                | kyverno            | infra-security | Policy enforcement                      |
| vault                  | vault              | infra-security | Secret store (PKI + KV + Transit/SOPS)  |
| authentik              | authentik          | infra-security | OIDC identity provider                  |
| wireguard              | wireguard          | infra-network  | VPN portal (wg-portal)                  |
| prometheus             | monitoring         | monitoring     | kube-prometheus-stack                   |
| loki                   | loki               | monitoring     | Log aggregation                         |
| minio                  | minio              | infra-storage  | S3-compatible object store              |
| minio-operator         | minio-operator     | infra-storage  | MinIO tenant operator                   |
| csi-driver-nfs         | csi-driver-nfs     | infra-storage  | NFS PVC provisioner                     |
| proxmox-csi-plugin     | proxmox-csi-plugin | infra-storage  | Proxmox block storage CSI               |
| volsync                | volsync            | infra-storage  | PVC backup/restore                      |
| local-path-provisioner | local-path-storage | infra-storage  | HostPath PVC provisioner                |
| homarr                 | homarr             | infra-tools    | Dashboard                               |
| homepage               | homepage           | infra-tools    | Dashboard alternative                   |
| stakater               | stakater           | infra-tools    | Reloader for configmap/secret changes   |
| crossplane             | crossplane         | infra-tools    | Infrastructure CRD provisioner          |
| popeye                 | popeye             | monitoring     | Cluster linter                          |
| gha-arc-controller     | arc-system         | infra-tools    | GitHub Actions runner controller        |
| system-upgrade         | system-upgrade     | infra-tools    | tuppr — Talos/k8s upgrade controller    |
| fstrim                 | kube-system        | infra-tools    | Weekly SSD fstrim CronJob               |
| vrising                | vrising            | misc           | V Rising game server                    |

### Beelink (k0s) — Applications

| App                    | Namespace          | Notes                          |
| ---------------------- | ------------------ | ------------------------------ |
| argocd                 | argocd             | GitOps controller              |
| adguard                | adguard            | DNS / ad-blocking              |
| authentik              | authentik          | OIDC identity provider         |
| cert-manager           | cert-manager       | TLS certificates via Vault PKI |
| external-secrets       | external-secrets   | ESO pulling from Vault         |
| homarr                 | homarr             | Dashboard                      |
| local-path-provisioner | local-path-storage | HostPath PVC provisioner       |
| metallb                | metallb-system     | L2 load balancer               |
| stakater               | stakater           | Reloader                       |
| traefik                | traefik            | Ingress controller             |
| vault                  | vault              | Secret store                   |
| wireguard              | wireguard          | VPN portal                     |

---

## Directory Structure

### Capsule: ClusterOrganization

**Invariant**
Each cluster has exactly two root directories: `infra/{distro}/` for OS-level config and `gitops/manifests/{app}/{cluster}/` for deployed manifests.

```
infra/
├── k0s/fullstack.yaml              # k0sctl cluster spec
└── talos/genmachine/
    └── bootstrap/
        ├── talconfig.yaml          # Talhelper cluster config (generates per-node machineconfigs)
        ├── clusterconfig/          # Generated; gitignored
        ├── talsecret.sops.yaml     # SOPS-encrypted Talos secrets
        └── resources/
            ├── prepare.sh          # Bootstrap script
            └── helmfile.yaml       # Bootstrap Helm installs (Cilium, ArgoCD)

gitops/
├── bootstrap/{beelink,genmachine}/ # ArgoCD installation Helm charts
├── core/
│   ├── appProjects/                # 7 AppProject definitions
│   ├── apps/
│   │   ├── beelink/                # Plain Application CRDs (one per app)
│   │   └── genmachine/
│   │       ├── argo/
│   │       ├── infra/
│   │       ├── kube-system/
│   │       ├── misc/
│   │       ├── observability/
│   │       ├── storage/
│   │       ├── system/
│   │       └── system-upgrade/
│   ├── clusters/                   # Cluster destination definitions
│   └── repos/                      # VCS repo secrets
└── manifests/{app}/
    ├── common/common-values.yaml   # Shared Helm values
    ├── beelink/
    │   ├── Chart.yaml
    │   ├── beelink-values.yaml
    │   └── templates/
    └── genmachine/
        ├── Chart.yaml
        ├── genmachine-values.yaml
        └── templates/
```

---

## ApplicationSet Pattern

### Capsule: ApplicationSetPattern

**Invariant**
Genmachine apps use `ApplicationSet` with a git directory generator. The generator discovers
`gitops/manifests/{app}/*` directories (excluding `common`, `beelink`, `k0s`) and deploys one
ArgoCD Application per matching directory (named after the directory).

**Example**

```yaml
generators:
  - git:
      directories:
        - path: "gitops/manifests/traefik/*"
          exclude: false
        - path: "gitops/manifests/traefik/common"
          exclude: true
        - path: "gitops/manifests/traefik/beelink"
          exclude: true
        - path: "gitops/manifests/traefik/k0s"
          exclude: true
```

Generated app name: `traefik-genmachine`. Destination cluster name: `genmachine`.

**Depth**

- `manifest-generate-paths: .;../common` annotation triggers reconciliation on common changes
- Value files: `common/common-values.yaml` (shared) + `{cluster}/{cluster}-values.yaml` (override)
- `ignoreMissingValueFiles: true` prevents failure when a cluster-specific file doesn't exist
- SeeAlso: `HelmChartConvention`

---

## AppProjects

| Project          | Purpose                                                    |
| ---------------- | ---------------------------------------------------------- |
| `infra-core`     | Core Kubernetes infrastructure (CNI, DNS, CSR approver)    |
| `infra-network`  | Networking (MetalLB, Traefik, AdGuard, WireGuard)          |
| `infra-security` | Security (cert-manager, ESO, Kyverno, Vault, Authentik)    |
| `infra-storage`  | Storage (CSI drivers, MinIO, Volsync, local-path)          |
| `infra-tools`    | Tooling (metrics-server, Stakater, ArgoCD, system-upgrade) |
| `monitoring`     | Observability (Prometheus, Loki, Grafana)                  |
| `argocd`         | ArgoCD itself                                              |

---

## Secrets Architecture

### Capsule: VaultPKI

**Invariant**
All TLS certificates are issued by cert-manager using Vault as a PKI backend. The cluster issuer is `fredcorp-ca`.

**Example**
An Ingress annotation `cert-manager.io/cluster-issuer: fredcorp-ca` triggers cert-manager to request
a certificate from Vault's PKI engine. The certificate is stored as a Kubernetes Secret and referenced
in the Ingress `tls` block.

**Depth**

- CA chain: `fredcorp-ca-chain` cert-manager Bundle injects CA into namespaces with `bundle.chain/inject: enabled` label
- Wildcard certs: `k0s-fullstack-wildcard`, `genmachine-wildcard` (Traefik default)
- Per-app pattern: `cert-manager.io/common-name: {app}.{cluster-domain}.fredcorp.com`
- SeeAlso: `ExternalSecretSync`, `TraefikIngress`

---

### Capsule: SOPSEncryption

**Invariant**
Files containing secrets committed to Git must end in `.sops.yaml` and be encrypted with Age before commit.

**Example**
`infra/talos/genmachine/bootstrap/talsecret.sops.yaml` contains encrypted Talos bootstrap secrets.
The pre-commit hook (`SOPS check-encryption`) blocks commits of unencrypted SOPS files.

**Depth**

- Tool: `age` (asymmetric) — public key in `.sops.yaml` config
- Encryption: `task sops:encrypt -- <file>`
- Decryption: `task sops:decrypt -- <file>` (requires private key)
- Renovate ignores `**/*.sops.*`
- SeeAlso: `ExternalSecretSync`

---

## Bootstrap Process

### Genmachine (Talos)

1. **Provision VMs** on Proxmox with static DHCP MACs → IPs
2. **Apply Talos machineconfigs** via `task talos:apply` (generated by talhelper from `talconfig.yaml`)
3. **Bootstrap etcd** on first control-plane node
4. **Run `resources/helmfile.yaml`** — installs Cilium CNI and ArgoCD via Helm
5. **Apply `gitops/bootstrap/genmachine/`** — bootstraps ArgoCD app-of-apps
6. **ArgoCD self-manages** — reconciles all ApplicationSets, deploys all apps

### Beelink (k0s)

1. **Apply k0sctl config** via `task k0s:apply-config` — spins up k0s on the node
2. **Install ArgoCD** from `gitops/bootstrap/beelink/`
3. **Apply core Applications** — ArgoCD takes over from there

---

## Common Failures

| Symptom                                    | Cause                                           | Fix                                                                 |
| ------------------------------------------ | ----------------------------------------------- | ------------------------------------------------------------------- |
| Pod stuck `Pending`                        | ExternalSecret not synced / Vault entry missing | `kubectl describe externalsecret -n <ns> <name>`, check Vault path  |
| ArgoCD app `OutOfSync` loop                | ServerSideApply conflict or annotation drift    | Check `argocd app diff`, add `RespectIgnoreDifferences`             |
| Certificate not issued                     | Vault PKI unreachable or wrong issuer name      | `kubectl describe certificaterequest -n <ns>`                       |
| Pod `CrashLoopBackOff` after secret change | Stakater Reloader not watching annotation       | Add `reloader.stakater.com/auto: "true"` annotation                 |
| Cilium pod not starting on Talos           | `hubble-ui` needs privilege                     | Check Talos `allowSchedulingOnControlPlanes` and Cilium tolerations |
