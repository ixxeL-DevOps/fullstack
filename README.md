<div align="center">
<p align="center"><img style="display: block; margin: auto; width: 220px;"  src="docs/assets/k8s-home2.png"></p>

<!-- markdownlint-disable no-trailing-punctuation -->

### My home-lab repository :rocket:

✨*managed with k0s/Talos, ArgoCD, Renovate and GitHub*✨

</div>

<div align="center">

---

**INFRASTRUCTURE K0S**

![K0sVersion](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Fk0s%2Ffullstack.yaml&query=%24.spec.k0s.version&style=for-the-badge&logo=kubernetes&logoColor=%23326CE5&label=k0s&color=%23326CE5)
![ArgoCD](https://img.shields.io/badge/argocd-v2.14.2-version?style=for-the-badge&logo=argo&logoColor=%23F76B39&color=%23F76B39)

**TOOLING**

![adguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fadguard%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=adguard&label=AdGuard&color=%2366B574)
![authentik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fauthentik%2Fapp%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=authentik&label=Authentik&color=%23FD4B2D)
![vault](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fvault%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=vault&label=Vault&color=%23FFB81C)
![traefik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Ftraefik%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=traefikproxy&logoColor=%239D0FB0&label=traefik&color=%239D0FB0)
![wireguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fwireguard%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=wireguard&logoColor=%23841618&label=wireguard&color=%23841618)
![homarr](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fhomarr%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=homarr&label=homarr&color=%23F44336)

</div>

<div align="center">

---

**INFRASTRUCTURE TALOS**

![TalosVersion](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Ftalos%2Fgenmachine%2Fbootstrap%2Ftalconfig.yaml&query=%24.talosVersion&style=for-the-badge&logo=talos&label=Talos&color=%23FF4400)
![k8s](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Ftalos%2Fgenmachine%2Fbootstrap%2Ftalconfig.yaml&query=%24.kubernetesVersion&style=for-the-badge&logo=kubernetes&label=K8s&color=%23326CE5)
![Cilium](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fcilium%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.cilium.image.tag&style=for-the-badge&logo=cilium&label=Cilium&color=%23E9B824)

**TOOLING**

![Argocd](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fbootstrap%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.argo-cd.global.image.tag&style=for-the-badge&logo=argo&label=Argocd&color=%23EF5A29)
![traefik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Ftraefik%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.traefik.image.tag&style=for-the-badge&logo=traefikproxy&logoColor=%239D0FB0&label=traefik&color=%239D0FB0)
![prometheu](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fprometheus%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.kube-prometheus-stack.prometheus.prometheuspec.image.tag&style=for-the-badge&logo=prometheus&label=prometheus&color=%23E6522C)
![grafana](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fprometheus%2Fgenmachine%2Fgenmachine-values.yaml&query=%24.kube-prometheus-stack.grafana.image.tag&style=for-the-badge&logo=grafana&label=grafana&color=%23F46800)

</div>

---

![pre-commit.ci status](https://github.com/ixxeL-DevOps/fullstack/actions/workflows/pre-commit.yaml/badge.svg)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/ixxeL-DevOps/fullstack?style=flat-square)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/ixxeL-DevOps/fullstack?style=flat-square)
![Renovate](https://img.shields.io/badge/deps-renovate-ok?style=flat-square&logo=renovate&logoColor=%230099FF&logoSize=auto&color=%230099FF)

---

# Overview

This is my mono repo for my home infrastructure. It's based loosely on the ideas from [szinn/k8s-homelab](https://github.com/szinn/k8s-homelab) as well as various templates and resources from GitHub and Reddit.

It follows the concept of **Infrastructure as Code** and [**GitOps**](https://opengitops.dev/), leveraging tools such as ArgoCD, Renovate, and go-task to create an easily bootstrappable and manageable home lab environment, with a strong focus on automation for Day 1/Day 2 operations.

The motivation behind setting up this home lab was to refactor my original environment, which was primarily based on a Raspberry Pi 4 running Docker Compose. While this setup worked, it lacked scalability, automation, and was not GitOps-friendly. To address these limitations, I decided to migrate to a fully Kubernetes-based infrastructure, leveraging its rich and advanced ecosystem. This transition allows for better workload orchestration, improved automation through GitOps practices, and seamless integration with cloud-native tools, making the entire environment more maintainable, resilient, and future-proof.

The entire infrastructure is fully virtualized on **Proxmox**, where each server runs as a virtual machine within the Proxmox cluster. This setup provides flexibility, isolation, and ease of management while allowing efficient resource allocation.

# Kubernetes

To experiment with different Kubernetes distributions, I use a mix of **k0s** and **Talos**. Each of these distributions offers unique advantages and match different requirements of my environment.

- A cluster running k0s, intended for a lab environment running on the BeeLink hardware
- Another cluster running Talos, used for a production environment running on the GenMachine hardware.

The choice of k0s for the lab cluster is due to its suitability for hardware with limited resources. In this case, k0s has been configured with a minimal setup and a low footprint.
On the other hand, Talos is used for the production cluster, allowing me to take advantage of advanced features and capabilities.

# GitOps

ArgoCD watches both clusters, leveraging `ApplicationSet` CRDs to centralize management in the main cluster.

Renovate monitors my entire repository for dependency updates. When updates are found, a PR is automatically created and sometimes merged automatically. Once PRs are merged, ArgoCD applies the changes to my clusters.

The security aspect of GitOps is managed using **HC Vault** as a secret manager and **External Secrets** for synchronization to prevent pushing sensitive information into Git.
