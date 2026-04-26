---
description: Step-by-step workflows for deploying apps, updating charts, managing secrets, and troubleshooting
tags: ["Workflows", "Deployment", "Troubleshooting"]
audience: ["LLMs", "Humans"]
categories: ["Reference[95%]"]
---

# Workflows

## Deploy a New Application

### On Genmachine (ApplicationSet pattern)

1. **Create the Helm chart directory**:
   ```
   gitops/manifests/{app}/
   ├── common/common-values.yaml    ← shared values
   └── genmachine/
       ├── Chart.yaml               ← wrapper chart (with upstream dep if needed)
       ├── genmachine-values.yaml   ← cluster overrides
       └── templates/               ← ExternalSecrets, PVCs, etc.
   ```

2. **Create the ApplicationSet** in `gitops/core/apps/genmachine/{category}/{app}.yaml`
   - Choose the right `{category}` directory: `argo/`, `infra/`, `kube-system/`, `observability/`, `storage/`, `system/`, `system-upgrade/`, `misc/`
   - Choose the right AppProject from DOMAIN.md
   - Follow the ApplicationSet template in CONVENTIONS.md

3. **If the app needs secrets**: create an ExternalSecret in `templates/` and add the secret to Vault first

4. **If the app needs a certificate**: add Ingress with cert-manager annotations (see CONVENTIONS.md)

5. **Pin versions with Renovate annotations** (see CONVENTIONS.md)

6. **Commit, push, open PR** — ArgoCD will sync when merged to `main`

### On Beelink (Application pattern)

Same as above but:
- Use `beelink/` directory instead of `genmachine/`
- Create a plain `Application` in `gitops/core/apps/beelink/{app}.yaml`
- Follow the Application template in CONVENTIONS.md

---

## Update a Chart Version

1. Find the version pin in `gitops/manifests/{app}/{cluster}/Chart.yaml` (upstream dependency)
2. Check the Renovate annotation above the version line
3. Renovate normally handles this automatically — if doing manually:
   - Update the version in `Chart.yaml`
   - Update the image tag in `{cluster}-values.yaml` if needed
   - Update `Chart.lock` by running `helm dependency update gitops/manifests/{app}/{cluster}/`
4. Commit — ArgoCD applies the new chart on merge

---

## Add a Secret

1. **Add the secret to Vault** at path `{app}/{secret-type}/{cluster}`:
   ```bash
   vault kv put -address=https://vault.k0s-fullstack.fredcorp.com {app}/{secret-type}/{cluster} key=value
   ```

2. **Create an ExternalSecret** in `gitops/manifests/{app}/{cluster}/templates/externalsecret.yaml`:
   ```yaml
   apiVersion: external-secrets.io/v1beta1
   kind: ExternalSecret
   metadata:
     name: {secret-name}
   spec:
     secretStoreRef:
       kind: ClusterSecretStore
       name: admin
     target:
       name: {secret-name}
     data:
       - secretKey: {key}
         remoteRef:
           key: {app}/{secret-type}/{cluster}
           property: {vault-field}
   ```

3. **Reference the secret** in your Helm values or pod spec

---

## Encrypt a Secret File with SOPS

```bash
task sops:encrypt -- path/to/secret.sops.yaml
```

The file must be named `*.sops.yaml`. The pre-commit hook blocks unencrypted SOPS files from being committed.

To edit an encrypted file:
```bash
task sops:decrypt -- path/to/secret.sops.yaml
# edit the file
task sops:encrypt -- path/to/secret.sops.yaml
```

---

## Bootstrap Genmachine from Scratch

```bash
# 1. Provision Proxmox VMs (static MAC → IP via DHCP)
task proxmox:create-talos

# 2. Generate and apply Talos machineconfigs
task talos:apply

# 3. Bootstrap etcd
task talos:bootstrap

# 4. Get kubeconfig
task talos:kubeconfig

# 5. Install Cilium + ArgoCD via helmfile
cd infra/talos/genmachine/bootstrap/resources
helmfile apply

# 6. Apply ArgoCD bootstrap (app-of-apps)
kubectl apply -k gitops/bootstrap/genmachine/

# ArgoCD takes over from here
```

---

## Upgrade Talos / Kubernetes

Upgrades are handled automatically by **tuppr** (system-upgrade namespace).

To trigger manually:
```bash
# Check current versions
task talos:versions

# Update version in infra/talos/genmachine/bootstrap/talconfig.yaml
# Then apply machineconfig changes
task talos:upgrade
```

---

## Troubleshoot ArgoCD Sync Failure

```bash
# List all apps and their sync status
argocd app list

# Get detailed diff for a specific app
argocd app diff {app}-genmachine

# Force resync
argocd app sync {app}-genmachine

# Check application logs
argocd app logs {app}-genmachine
```

Common causes:
- ExternalSecret not synced → `kubectl describe externalsecret -n {ns} {name}`
- Helm render error → check values files for typos, missing keys
- ServerSideApply conflict → add field to `ignoreDifferences`
- Namespace missing CA label → add `bundle.chain/inject: enabled` label to namespace

---

## Troubleshoot Pod Not Starting

```bash
kubectl describe pod -n {namespace} {pod-name}
kubectl logs -n {namespace} {pod-name} --previous

# Check ExternalSecret
kubectl get externalsecret -n {namespace}
kubectl describe externalsecret -n {namespace} {name}

# Check Vault connectivity
vault status -address=https://vault.{cluster-domain}.fredcorp.com
```

---

## Run Taskfile Tasks

```bash
# List available tasks
task --list

# Common tasks
task talos:kubeconfig       # Get genmachine kubeconfig
task k0s:kubeconf           # Get beelink kubeconfig
task vault:unseal           # Unseal Vault (after restart)
task eso:configure          # Configure ESO ClusterSecretStore
task sops:encrypt -- file   # Encrypt a SOPS file
task sops:decrypt -- file   # Decrypt a SOPS file
task mkdocs:serve           # Serve documentation locally
task lint:yaml              # Run yamllint
```

---

## Update Documentation

```bash
# Serve locally with live reload
task mkdocs:serve
# or: mkdocs serve

# Build static site
task mkdocs:build
# or: mkdocs build
```

Documentation lives in `docs/`. MkDocs config is `mkdocs.yml`. Mermaid diagrams are supported — see `mermaid-diagram-guide.md`.
