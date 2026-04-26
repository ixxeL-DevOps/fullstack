---
description: CLI tools available, how to install them, and key commands for cluster management
tags: ["Tools", "CLI", "Taskfile", "kubectl", "talosctl", "helm"]
audience: ["LLMs", "Humans"]
categories: ["Reference[90%]"]
---

# Tools

## Tool Management

Tools are managed via **mise** (`mise.toml` at repo root). To install all tools:

```bash
mise install
```

Python packages (mkdocs, yamllint, etc.) are managed via **uv** (`pyproject.toml`):

```bash
uv sync
```

---

## Core Tools

| Tool | Purpose | Install |
|---|---|---|
| `kubectl` | Kubernetes CLI | mise |
| `talosctl` | Talos OS management | mise |
| `helm` | Kubernetes package manager | mise |
| `task` | Taskfile runner | mise |
| `argocd` | ArgoCD CLI | mise |
| `vault` | HashiCorp Vault CLI | mise |
| `sops` | Secret file encryption | mise |
| `age` | Age encryption (used by SOPS) | mise |
| `talhelper` | Talos machineconfig generator | mise |
| `helmfile` | Declarative Helm deployment | mise |
| `kustomize` | Kubernetes manifest overlays | mise |
| `cilium` | Cilium CLI | mise |
| `mkdocs` | Documentation site generator | uv (Python) |

---

## Taskfile Reference

The root `Taskfile.yaml` includes sub-taskfiles. Run `task --list` to see all available tasks.

### Talos

```bash
task talos:apply            # Apply machineconfigs to all nodes
task talos:bootstrap        # Bootstrap etcd on first node
task talos:kubeconfig       # Fetch kubeconfig and merge into ~/.kube/config
task talos:upgrade          # Upgrade Talos OS
task talos:dashboard        # Open Talos dashboard
```

### k0s (Beelink)

```bash
task k0s:kubeconf           # Fetch kubeconfig
task k0s:apply-config       # Apply k0sctl config
task k0s:upgrade-cluster    # Upgrade k0s
```

### Vault

```bash
task vault:unseal           # Unseal Vault
task vault:unseal-genmachine  # Unseal Vault on genmachine
task vault:unseal-beelink     # Unseal Vault on beelink
```

### ESO (External Secrets)

```bash
task eso:configure          # Configure ClusterSecretStore on current cluster
```

### SOPS

```bash
task sops:encrypt -- <file>   # Encrypt a file with Age
task sops:decrypt -- <file>   # Decrypt a SOPS file
```

### Proxmox

```bash
task proxmox:create-talos   # Create Talos VMs on Proxmox
```

### Bootstrap

```bash
task bootstrap:talos        # Full Talos bootstrap sequence
```

### Helm

```bash
task helm:update -- <chart-dir>   # Run helm dependency update
```

### Lint

```bash
task lint:yaml              # Run yamllint on all YAML files
```

### MkDocs

```bash
task mkdocs:serve           # Serve docs locally (http://localhost:8000)
task mkdocs:build           # Build static docs site
```

### Restic

```bash
task restic:backup          # Run a backup
task restic:restore         # Restore from backup
```

### Authentik

```bash
task authentik:apply-blueprint  # Apply an Authentik blueprint
```

---

## kubectl Quick Reference

```bash
# Context management
kubectl config get-contexts
kubectl config use-context genmachine   # or beelink

# ArgoCD apps
kubectl get applications -n argocd
kubectl get applicationsets -n argocd

# ExternalSecrets
kubectl get externalsecret -A
kubectl describe externalsecret -n {ns} {name}

# Cert-manager
kubectl get certificate -A
kubectl get certificaterequest -A

# Check node status
kubectl get nodes -o wide

# Check pod status
kubectl get pods -A | grep -v Running
```

---

## talosctl Quick Reference

```bash
# Set talosconfig
export TALOSCONFIG=infra/talos/genmachine/talosconfig

# Check node health
talosctl health --nodes 192.168.1.151,192.168.1.152,192.168.1.153

# Get service status
talosctl services --nodes 192.168.1.151

# View logs
talosctl logs kubelet --nodes 192.168.1.151

# Apply machineconfig
talosctl apply-config --nodes 192.168.1.151 --file infra/talos/genmachine/bootstrap/clusterconfig/genmachine-talos-1.yaml

# Dashboard
talosctl dashboard --nodes 192.168.1.151
```

---

## argocd Quick Reference

```bash
# Login
argocd login argocd.talos-genmachine.fredcorp.com

# List all apps
argocd app list

# Get app details
argocd app get {app-name}

# Sync an app
argocd app sync {app-name}

# Diff (what would change)
argocd app diff {app-name}

# Hard refresh (force re-render)
argocd app get {app-name} --hard-refresh
```

---

## Vault Quick Reference

```bash
# Login (OIDC)
vault login -method=oidc -address=https://vault.talos-genmachine.fredcorp.com

# Read a secret
vault kv get -address=https://vault.talos-genmachine.fredcorp.com {app}/{secret-type}/{cluster}

# Write a secret
vault kv put -address=https://vault.talos-genmachine.fredcorp.com {app}/{secret-type}/{cluster} key=value

# Check PKI
vault pki health-check -address=https://vault.talos-genmachine.fredcorp.com fredcorp-pki
```

---

## Helm Quick Reference

```bash
# Update dependencies for a chart
helm dependency update gitops/manifests/{app}/{cluster}/

# Template a chart locally (dry run)
helm template {release} gitops/manifests/{app}/{cluster}/ \
  -f gitops/manifests/{app}/common/common-values.yaml \
  -f gitops/manifests/{app}/{cluster}/{cluster}-values.yaml

# List installed releases
helm list -A
```
