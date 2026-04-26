<div align="center">
<img src="docs/assets/k8s-home2.png" width="180px" />

# ixxeL-DevOps HomeLab

_Infrastructure as Code · GitOps · Self-hosted · Fully automated_

</div>

<div align="center">

**BEELINK — k0s**

![K0sVersion](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Fk0s%2Ffullstack.yaml&query=%24.spec.k0s.version&style=for-the-badge&logo=kubernetes&logoColor=%23326CE5&label=k0s&color=%23326CE5)
![ArgoCD](https://img.shields.io/badge/argocd-v2.14.8-version?style=for-the-badge&logo=argo&logoColor=%23F76B39&color=%23F76B39)
![traefik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Ftraefik%2Fbeelink%2Fbeelink-values.yaml&query=%24.traefik.image.tag&style=for-the-badge&logo=traefikproxy&logoColor=%239D0FB0&label=traefik&color=%239D0FB0)
![vault](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fvault%2Fbeelink%2Fbeelink-values.yaml&query=%24.vault.server.image.tag&style=for-the-badge&logo=vault&label=Vault&color=%23FFB81C)
![authentik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fauthentik%2Fbeelink%2Fapp%2Fbeelink-values.yaml&query=%24.authentik.global.image.tag&style=for-the-badge&logo=authentik&label=Authentik&color=%23FD4B2D)
![wireguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fwireguard%2Fbeelink%2Fbeelink-values.yaml&query=%24.wg-portal.image.tag&style=for-the-badge&logo=wireguard&logoColor=%23841618&label=wireguard&color=%23841618)
![adguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fadguard%2Fbeelink%2Fbeelink-values.yaml&query=%24.adguard-home.image.tag&style=for-the-badge&logo=adguard&label=AdGuard&color=%2366B574)
![homarr](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fhomarr%2Fbeelink%2Fbeelink-values.yaml&query=%24.homarr.image.tag&style=for-the-badge&logo=homarr&label=homarr&color=%23F44336)

**GENMACHINE — Talos**

![TalosVersion](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Ftalos%2Fgenmachine%2Fbootstrap%2Ftalconfig.yaml&query=%24.talosVersion&style=for-the-badge&logo=talos&label=Talos&color=%23FF4400)
![k8s](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Ftalos%2Fgenmachine%2Fbootstrap%2Ftalconfig.yaml&query=%24.kubernetesVersion&style=for-the-badge&logo=kubernetes&label=K8s&color=%23326CE5)
![Cilium](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fcilium%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.cilium.image.tag&style=for-the-badge&logo=cilium&label=Cilium&color=%23E9B824)
![Argocd](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fbootstrap%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.argo-cd.global.image.tag&style=for-the-badge&logo=argo&label=Argocd&color=%23EF5A29)
![traefik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Ftraefik%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.traefik.image.tag&style=for-the-badge&logo=traefikproxy&logoColor=%239D0FB0&label=traefik&color=%239D0FB0)
![vault](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fvault%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.vault.server.image.tag&style=for-the-badge&logo=vault&label=Vault&color=%23FFB81C)
![prometheus](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fprometheus%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.kube-prometheus-stack.prometheus.prometheusSpec.image.tag&style=for-the-badge&logo=prometheus&label=prometheus&color=%23E6522C)
![grafana](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fprometheus%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.kube-prometheus-stack.grafana.image.tag&style=for-the-badge&logo=grafana&label=grafana&color=%23F46800)
![minio](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fminio%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.minio.image.tag&style=for-the-badge&logo=minio&logoColor=e0e0e0&label=minio&color=e0e0e0)

</div>

---

![pre-commit.ci status](https://github.com/ixxeL-DevOps/fullstack/actions/workflows/pre-commit.yaml/badge.svg)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/ixxeL-DevOps/fullstack?style=flat-square)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/ixxeL-DevOps/fullstack?style=flat-square)
![Renovate](https://img.shields.io/badge/deps-renovate-ok?style=flat-square&logo=renovate&logoColor=%230099FF&logoSize=auto&color=%230099FF)

---

## Overview

This repository is the single source of truth for a homelab running on two Kubernetes clusters, following **GitOps** and **Infrastructure as Code** principles. Every component — cluster bootstrap, application configuration, secret management, and certificate lifecycle — is declared as code and reconciled automatically.

The infrastructure evolved from a Raspberry Pi running Docker Compose into a production-grade Kubernetes platform. The two clusters are complementary: **Beelink** (k0s, bare metal) hosts the security and access infrastructure, while **Genmachine** (Talos Linux, Proxmox VMs) runs production workloads and the observability stack.

## Architecture

```mermaid
graph TB
    subgraph GH["GitHub"]
        repo[("fullstack\nrepository")]
        renovate["🤖 Renovate\nauto-update PRs"]
        ci["⚙️ GitHub Actions\nhelm diff · kubeconform"]
    end

    subgraph NET["Home Network"]
        user(["👤 User"])
        adguard["🛡️ AdGuard\nDNS · *.fredcorp.com"]
        vpn["🔒 WireGuard VPN"]
    end

    subgraph BK["🖥️ Beelink — k0s (bare metal)"]
        traefik_b["Traefik\nIngress + TLS"]
        authentik["Authentik\nSSO · IdP · ForwardAuth"]
        vault_b["Vault\nPKI · KV"]
        eso_b["ExternalSecrets"]
        certmgr_b["cert-manager"]
        argocd_b["ArgoCD"]
    end

    subgraph GM["🖥️ Genmachine — Talos (3× VM on Proxmox)"]
        traefik_g["Traefik\nIngress + TLS"]
        vault_g["Vault\nPKI · KV"]
        eso_g["ExternalSecrets"]
        certmgr_g["cert-manager"]
        argocd_g["ArgoCD"]
        prometheus["Prometheus · Grafana\nLoki"]
        minio["MinIO\nS3 object store"]
    end

    user -- "DNS" --> adguard
    user -- "VPN" --> vpn
    adguard -- "ingress" --> traefik_b & traefik_g
    traefik_b -- "ForwardAuth" --> authentik

    renovate -- "auto-PR" --> repo
    ci -- "diff preview" --> repo
    argocd_b & argocd_g -- "pull · reconcile" --> repo

    vault_b -- "PKI signs" --> certmgr_b
    vault_g -- "PKI signs" --> certmgr_g
    vault_b -- "KV secrets" --> eso_b
    vault_g -- "KV secrets" --> eso_g
```

## GitOps Flow

```mermaid
flowchart LR
    dev(["💻 Developer\ngit push"])
    bot(["🤖 Renovate\nauto-PR"])
    repo(["📦 GitHub\nrepository"])
    ci["⚙️ CI\nhelm-rmp diff"]
    argocd["🔄 ArgoCD\nbeelink + genmachine"]
    clusters["☸️ Clusters\nbeelink · genmachine"]

    dev -->|push / PR| repo
    bot -->|dependency PR| repo
    repo -->|triggers| ci
    repo -->|poll main| argocd
    argocd -->|apply manifests| clusters
    ci -->|posts diff comment| repo
```

## Stack

| Layer | Tool | Role |
|---|---|---|
| Cluster | Talos Linux + k0s | Immutable OS (Genmachine) · lightweight K8s (Beelink) |
| GitOps | ArgoCD + Renovate | Continuous reconciliation · automated dependency updates |
| Networking | Cilium + Traefik | eBPF CNI · L2 LB announcements · TLS ingress |
| DNS | AdGuard Home | Local resolver · `*.fredcorp.com` split-horizon |
| PKI / Secrets | HashiCorp Vault | CA · KV secrets · SOPS transit encryption |
| Certificates | cert-manager + trust-manager | Automated TLS lifecycle from Vault PKI |
| Secret sync | ExternalSecrets | Vault → Kubernetes Secret synchronisation |
| Auth | Authentik | SSO IdP · OIDC provider · ForwardAuth outpost |
| VPN | WireGuard Portal | Self-hosted VPN management |
| Observability | Prometheus · Grafana · Loki | Metrics · dashboards · logs |
| Storage | MinIO · Proxmox CSI | S3 object store · block volumes |
| Encryption | SOPS | Secrets encrypted at rest in Git |

## Documentation

Full documentation is available at the [project docs site](https://ixxel-devops.github.io/fullstack).
