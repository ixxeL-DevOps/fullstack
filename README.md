<div align="center">
<p align="center"><img style="display: block; margin: auto; width: 220px;"  src="docs/src/pictures/k8s-home2.png"></p>

<!-- markdownlint-disable no-trailing-punctuation -->

### My home-lab repository :rocket:

✨*managed with k0s/Talos, ArgoCD, Renovate and GitHub*✨
</div>

<div align="center">

**INFRASTRUCTURE**

![K0sVersion](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Finfra%2Fk0s%2Ffullstack.yaml&query=%24.spec.k0s.version&style=for-the-badge&logo=kubernetes&logoColor=%23326CE5&label=k0s&color=%23326CE5
)
![ArgoCD](https://img.shields.io/badge/argocd-v2.14.2-version?style=for-the-badge&logo=argo&logoColor=%23F76B39&color=%23F76B39
)
</div>

<div align="center">

**TOOLING HELM VERSION**

![adguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fadguard%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=adguard&label=AdGuard&color=%2366B574)
![authentik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fauthentik%2Fapp%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=authentik&label=Authentik&color=%23FD4B2D)
![vault](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fvault%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=vault&label=Vault&color=%23FFB81C
)
![traefik](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Ftraefik%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=traefikproxy&logoColor=%239D0FB0&label=traefik&color=%239D0FB0
)
![wireguard](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fwireguard%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=wireguard&logoColor=%23841618&label=wireguard&color=%23841618
)
![homarr](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FixxeL-DevOps%2Ffullstack%2Frefs%2Fheads%2Fmain%2Fgitops%2Fmanifests%2Fhomarr%2FChart.yaml&query=%24.dependencies%5B0%5D.version&style=for-the-badge&logo=homarr&label=homarr&color=%23F44336
)


</div>

This project utilizes Infrastructure as Code and GitOps to automate provisioning, operating, and updating self-hosted services in my homelab. 