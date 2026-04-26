<div align="center">
<p align="center"><img style="display: block; margin: auto; width: 300px;" src="assets/k8s-home2.png"></p>
<h1>ixxeL-DevOps HomeLab</h1>
<p><em>Infrastructure as Code · GitOps · Self-hosted · Fully automated</em></p>
</div>

---

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ixxeL-DevOps/fullstack/main.svg)](https://results.pre-commit.ci/latest/github/ixxeL-DevOps/fullstack/main)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/ixxeL-DevOps/fullstack?style=flat-square)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/ixxeL-DevOps/fullstack?style=flat-square)
![Renovate](https://img.shields.io/badge/deps-renovate-ok?style=flat-square&logo=renovate&logoColor=%230099FF&logoSize=auto&color=%230099FF)

---

## Overview

This repository is the single source of truth for a fully automated homelab running on two Kubernetes clusters. Every component — from cluster bootstrap to application configuration — is declared as code, reconciled by ArgoCD, and kept up-to-date by Renovate.

The two clusters are complementary: **Beelink** (k0s on bare metal) hosts security and access infrastructure, while **Genmachine** (Talos Linux on Proxmox VMs) hosts the production workloads and observability stack. Both share a unified GitOps structure and are managed from a single repository.

=== "Beelink — k0s"

    **Cluster**

    ![K0sVersion](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Fk0s%2Ffullstack.yaml&query=%24.spec.k0s.version&style=for-the-badge&logo=kubernetes&logoColor=%23326CE5&label=k0s&color=%23326CE5)
    ![ArgoCD](https://img.shields.io/badge/argocd-v2.14.8-version?style=for-the-badge&logo=argo&logoColor=%23F76B39&color=%23F76B39)

    **Applications**

    ![traefik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Ftraefik%2Fbeelink%2Fbeelink-values.yaml&query=%24.traefik.image.tag&style=for-the-badge&logo=traefikproxy&logoColor=%239D0FB0&label=traefik&color=%239D0FB0)
    ![adguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fadguard%2Fbeelink%2Fbeelink-values.yaml&query=%24.adguard-home.image.tag&style=for-the-badge&logo=adguard&label=AdGuard&color=%2366B574)
    ![authentik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fauthentik%2Fbeelink%2Fapp%2Fbeelink-values.yaml&query=%24.authentik.global.image.tag&style=for-the-badge&logo=authentik&label=Authentik&color=%23FD4B2D)
    ![vault](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fvault%2Fbeelink%2Fbeelink-values.yaml&query=%24.vault.server.image.tag&style=for-the-badge&logo=vault&label=Vault&color=%23FFB81C)
    ![wireguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fwireguard%2Fbeelink%2Fbeelink-values.yaml&query=%24.wg-portal.image.tag&style=for-the-badge&logo=wireguard&logoColor=%23841618&label=wireguard&color=%23841618)
    ![homarr](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fhomarr%2Fbeelink%2Fbeelink-values.yaml&query=%24.homarr.image.tag&style=for-the-badge&logo=homarr&label=homarr&color=%23F44336)

=== "Genmachine — Talos"

    **Cluster**

    ![TalosVersion](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Ftalos%2Fgenmachine%2Fbootstrap%2Ftalconfig.yaml&query=%24.talosVersion&style=for-the-badge&logo=talos&label=Talos&color=%23FF4400)
    ![k8s](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Ftalos%2Fgenmachine%2Fbootstrap%2Ftalconfig.yaml&query=%24.kubernetesVersion&style=for-the-badge&logo=kubernetes&label=K8s&color=%23326CE5)
    ![Cilium](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fcilium%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.cilium.image.tag&style=for-the-badge&logo=cilium&label=Cilium&color=%23E9B824)

    **Applications**

    ![Argocd](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fbootstrap%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.argo-cd.global.image.tag&style=for-the-badge&logo=argo&label=Argocd&color=%23EF5A29)
    ![traefik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Ftraefik%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.traefik.image.tag&style=for-the-badge&logo=traefikproxy&logoColor=%239D0FB0&label=traefik&color=%239D0FB0)
    ![prometheus](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fprometheus%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.kube-prometheus-stack.prometheus.prometheusSpec.image.tag&style=for-the-badge&logo=prometheus&label=prometheus&color=%23E6522C)
    ![grafana](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fprometheus%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.kube-prometheus-stack.grafana.image.tag&style=for-the-badge&logo=grafana&label=grafana&color=%23F46800)
    ![minio](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fminio%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.minio.image.tag&style=for-the-badge&logo=minio&logoColor=e0e0e0&label=minio&color=e0e0e0)
    ![adguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fadguard%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.adguard-home.image.tag&style=for-the-badge&logo=adguard&label=AdGuard&color=%2366B574)

---

## Architecture

### Infrastructure topology

```mermaid
graph TB
    subgraph github["   GitHub   "]
        repo[("fullstack\nrepository")]
        renovate["Renovate\nauto-update PRs"]
        ci["GitHub Actions\nhelm diff · kubeconform"]
    end

    subgraph access["   Access layer   "]
        user(["User"])
        vpn["WireGuard\nVPN"]
        adguard["AdGuard Home\nDNS · *.fredcorp.com"]
    end

    subgraph beelink["   Beelink — k0s (bare metal)   "]
        direction TB
        traefik_b["Traefik\nIngress + TLS termination"]
        subgraph security["Security plane"]
            authentik["Authentik\nSSO / IdP"]
            vault_b["Vault\nPKI · KV · Transit"]
            certmgr_b["cert-manager\n+ trust-manager"]
            eso_b["ExternalSecrets"]
        end
        subgraph apps_b["Applications"]
            homarr["Homarr\ndashboard"]
            adguard_b["AdGuard\nDNS"]
        end
        argocd_b["ArgoCD"]
    end

    subgraph genmachine["   Genmachine — Talos (Proxmox VMs)   "]
        direction TB
        subgraph vms["3× control-plane VMs  ·  etcd  ·  Cilium CNI"]
            traefik_g["Traefik\nIngress + TLS termination"]
            subgraph obs["Observability"]
                prometheus["Prometheus\n+ Grafana"]
                loki["Loki\nlog aggregation"]
            end
            subgraph storage_g["Storage"]
                minio["MinIO\nobject store"]
                csi["Proxmox CSI\nblock volumes"]
            end
            vault_g["Vault\nPKI · KV · Transit"]
            certmgr_g["cert-manager"]
            eso_g["ExternalSecrets"]
            argocd_g["ArgoCD"]
        end
    end

    user -->|"HTTPS / DNS"| adguard
    user -->|"WireGuard tunnel"| vpn
    adguard -->|"routes *.fredcorp.com"| traefik_b & traefik_g
    traefik_b -->|"ForwardAuth"| authentik

    renovate -->|"auto-PR"| repo
    ci -->|"diff preview"| repo
    argocd_b & argocd_g -->|"pull reconcile"| repo

    style github fill:#21262d,stroke:#6e40c9,color:#e6edf3
    style access fill:#161b22,stroke:#3fb950,color:#e6edf3
    style beelink fill:#0d2137,stroke:#4d94ff,color:#e6edf3
    style security fill:#0d1a2e,stroke:#4d94ff,color:#e6edf3
    style apps_b fill:#0d1a2e,stroke:#4d94ff,color:#e6edf3
    style genmachine fill:#0d2010,stroke:#3fb950,color:#e6edf3
    style vms fill:#0d1a0d,stroke:#3fb950,color:#e6edf3
    style obs fill:#0d1a0d,stroke:#3fb950,color:#e6edf3
    style storage_g fill:#0d1a0d,stroke:#3fb950,color:#e6edf3
```

### Request flow — authenticated access

```mermaid
flowchart LR
    user(["User"])
    dns["AdGuard\nDNS"]
    traefik["Traefik"]
    fwdauth["Authentik\noutpost"]
    app["Application"]
    vault["Vault\nPKI"]
    certmgr["cert-manager"]

    user -->|"1 · DNS lookup\n*.fredcorp.com"| dns
    dns -->|"2 · resolves to\nMetalLB IP"| traefik
    traefik -->|"3 · ForwardAuth\nmiddleware"| fwdauth
    fwdauth -->|"4 · 401 → login\nor 200 + headers"| traefik
    traefik -->|"5 · proxy +\nX-authentik-* headers"| app
    certmgr -->|"issues TLS cert\nfrom Vault PKI"| traefik
    vault -->|"signs CSR"| certmgr
```

---

## Stack

| Layer | Component | Role |
|---|---|---|
| **Cluster** | [Talos Linux](https://www.talos.dev/) | Immutable, API-driven OS for Genmachine nodes |
| **Cluster** | [k0s](https://k0sproject.io/) | Lightweight single-node Kubernetes for Beelink |
| **GitOps** | [ArgoCD](https://argo-cd.readthedocs.io/) | Continuous reconciliation of all cluster state |
| **GitOps** | [Renovate](https://docs.renovatebot.com/) | Automated dependency update PRs |
| **Networking** | [Cilium](https://cilium.io/) | eBPF CNI with L2 LoadBalancer announcements |
| **Ingress** | [Traefik](https://traefik.io/) | Reverse proxy with automatic TLS and ForwardAuth |
| **DNS** | [AdGuard Home](https://adguard.com/adguard-home/) | Local DNS resolver with ad-blocking |
| **PKI / Secrets** | [HashiCorp Vault](https://www.vaultproject.io/) | PKI CA, KV secrets, Transit auto-unseal |
| **Certificates** | [cert-manager](https://cert-manager.io/) | Automated certificate lifecycle from Vault PKI |
| **Secrets** | [ExternalSecrets](https://external-secrets.io/) | Vault → Kubernetes Secret synchronisation |
| **Auth** | [Authentik](https://goauthentik.io/) | SSO IdP — OIDC provider + ForwardAuth outpost |
| **VPN** | [WireGuard Portal](https://github.com/h44z/wg-portal) | Self-hosted VPN management UI |
| **Observability** | Prometheus · Grafana · Loki | Metrics, dashboards, and log aggregation |
| **Storage** | MinIO · Proxmox CSI | S3-compatible object store + block volumes |
| **Encryption** | [SOPS](https://github.com/getsops/sops) | Secrets encryption in Git via Vault Transit |
