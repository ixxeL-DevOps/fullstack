<div align="center">
<p align="center"><img style="display: block; margin: auto; width: 400px;"  src="assets/k8s-home2.png"></p>
</div>

# **My home-lab repository**

**Hosted with k0s & Talos**

**Managed by ArgoCD**

**Powered by Renovate and GitHub**

**Fueled by Cilium**

---

**INFRASTRUCTURE K0S**

![K0sVersion](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Fk0s%2Ffullstack.yaml&query=%24.spec.k0s.version&style=for-the-badge&logo=kubernetes&logoColor=%23326CE5&label=k0s&color=%23326CE5)
![ArgoCD](https://img.shields.io/badge/argocd-v2.14.8-version?style=for-the-badge&logo=argo&logoColor=%23F76B39&color=%23F76B39)

**TOOLING**

![traefik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Ftraefik%2Fbeelink%2Fbeelink-values.yaml&query=%24.traefik.image.tag&style=for-the-badge&logo=traefikproxy&logoColor=%239D0FB0&label=traefik&color=%239D0FB0)
![adguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fadguard%2Fbeelink%2Fbeelink-values.yaml&query=%24.adguard-home.image.tag&style=for-the-badge&logo=adguard&label=AdGuard&color=%2366B574)
![authentik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fauthentik%2Fbeelink%2Fapp%2Fbeelink-values.yaml&query=%24.authentik.global.image.tag&style=for-the-badge&logo=authentik&label=Authentik&color=%23FD4B2D)
![vault](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fvault%2Fbeelink%2Fbeelink-values.yaml&query=%24.vault.server.image.tag&style=for-the-badge&logo=vault&label=Vault&color=%23FFB81C)
![wireguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fwireguard%2Fbeelink%2Fbeelink-values.yaml&query=%24.wg-portal.image.tag&style=for-the-badge&logo=wireguard&logoColor=%23841618&label=wireguard&color=%23841618)
![homarr](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fhomarr%2Fbeelink%2Fbeelink-values.yaml&query=%24.homarr.image.tag&style=for-the-badge&logo=homarr&label=homarr&color=%23F44336)

---

**INFRASTRUCTURE TALOS**

![TalosVersion](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Ftalos%2Fgenmachine%2Fbootstrap%2Ftalconfig.yaml&query=%24.talosVersion&style=for-the-badge&logo=talos&label=Talos&color=%23FF4400)
![k8s](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Ftalos%2Fgenmachine%2Fbootstrap%2Ftalconfig.yaml&query=%24.kubernetesVersion&style=for-the-badge&logo=kubernetes&label=K8s&color=%23326CE5)
![Cilium](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fcilium%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.cilium.image.tag&style=for-the-badge&logo=cilium&label=Cilium&color=%23E9B824)

**TOOLING**

![Argocd](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fbootstrap%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.argo-cd.global.image.tag&style=for-the-badge&logo=argo&label=Argocd&color=%23EF5A29)
![traefik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Ftraefik%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.traefik.image.tag&style=for-the-badge&logo=traefikproxy&logoColor=%239D0FB0&label=traefik&color=%239D0FB0)
![prometheus](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fprometheus%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.kube-prometheus-stack.prometheus.prometheusSpec.image.tag&style=for-the-badge&logo=prometheus&label=prometheus&color=%23E6522C)
![grafana](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fprometheus%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.kube-prometheus-stack.grafana.image.tag&style=for-the-badge&logo=grafana&label=grafana&color=%23F46800)
![minio](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fminio%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.minio.image.tag&style=for-the-badge&logo=minio&logoColor=e0e0e0&label=minio&color=e0e0e0)
![adguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fadguard%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.adguard-home.image.tag&style=for-the-badge&logo=adguard&label=AdGuard&color=%2366B574)

---

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ixxeL-DevOps/fullstack/main.svg)](https://results.pre-commit.ci/latest/github/ixxeL-DevOps/fullstack/main)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/ixxeL-DevOps/fullstack?style=flat-square)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/ixxeL-DevOps/fullstack?style=flat-square)
![Renovate](https://img.shields.io/badge/deps-renovate-ok?style=flat-square&logo=renovate&logoColor=%230099FF&logoSize=auto&color=%230099FF)

---

This project utilizes Infrastructure as Code and GitOps to automate provisioning, operating, and updating self-hosted services in my homelab.

## Architecture Overview

```mermaid
graph TB
    subgraph internet["Internet"]
        user["User"]
    end

    subgraph home["Home Network (192.168.1.x)"]
        router["Router"]
        adguard["AdGuard Home\nDNS resolver"]
    end

    subgraph github["GitHub"]
        repo["fullstack\nrepository"]
        renovate["Renovate Bot\nautomated PRs"]
        actions["GitHub Actions\nCI / helm-rmp"]
    end

    subgraph beelink["Beelink — k0s cluster"]
        traefik_b["Traefik\nIngress"]
        argocd_b["ArgoCD"]
        authentik["Authentik\nIdP / SSO"]
        vault_b["Vault\nbeelink"]
        wireguard["WireGuard\nVPN"]
    end

    subgraph genmachine["Genmachine — Talos cluster"]
        subgraph proxmox["Proxmox hypervisor"]
            vm1["talos-1\n192.168.1.151"]
            vm2["talos-2\n192.168.1.152"]
            vm3["talos-3\n192.168.1.153"]
        end
        traefik_g["Traefik\nIngress"]
        argocd_g["ArgoCD"]
        vault_g["Vault\ngenmachine"]
        prometheus["Prometheus\n+ Grafana"]
        minio["MinIO\nobject storage"]
    end

    user -->|HTTPS| router
    router -->|ingress| traefik_b
    router -->|ingress| traefik_g
    router -->|DNS| adguard

    argocd_b -->|pull| repo
    argocd_g -->|pull| repo
    renovate -->|auto-PR| repo
    actions -->|helm diff| repo

    vault_b <-->|transit auto-unseal| vault_g

    style beelink fill:#1a3a5c,stroke:#4d94ff,color:#fff
    style genmachine fill:#1a3a1a,stroke:#4dff4d,color:#fff
    style github fill:#2d1a3a,stroke:#9d4dff,color:#fff
    style home fill:#3a2d1a,stroke:#ffb84d,color:#fff
    style proxmox fill:#2a3a2a,stroke:#4dff4d,color:#fff
```
