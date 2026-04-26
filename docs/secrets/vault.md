# HashiCorp Vault

## Overview

Two Vault instances are deployed across the two clusters. Each instance serves as both a secrets engine and a PKI certificate authority for its cluster, and as an auto-unseal transit engine for the other cluster.

```mermaid
graph TB
    subgraph beelink["Beelink — k0s cluster"]
        vault_b["Vault beelink\nvault.k0s-fullstack.fredcorp.com"]
        pki_b["PKI Engine\nRoot + Intermediate CA\nfredcorp.com"]
        transit_b["Transit Engine\nkey: unseal-genmachine"]
        kv_b["KV Engine\nadmin/ secrets"]
    end

    subgraph genmachine["Genmachine — Talos cluster"]
        vault_g["Vault genmachine\nvault.talos-genmachine.fredcorp.com"]
        pki_g["PKI Engine\nRoot + Intermediate CA\nfredcorp.com"]
        transit_g["Transit Engine\nkey: unseal-beelink"]
        kv_g["KV Engine\nadmin/ secrets"]
    end

    vault_b -->|auto-unseal via transit| transit_g
    vault_g -->|auto-unseal via transit| transit_b

    pki_b -->|signs certs for| cm_b["cert-manager\nbeelink"]
    pki_g -->|signs certs for| cm_g["cert-manager\ngenmachine"]
    kv_b -->|serves secrets| eso_b["ExternalSecrets\nbeelink"]
    kv_g -->|serves secrets| eso_g["ExternalSecrets\ngenmachine"]

    style vault_b fill:#1a2a3a,stroke:#FFB81C,color:#FFB81C
    style vault_g fill:#1a2a3a,stroke:#FFB81C,color:#FFB81C
```

## Transit Auto-Unseal

Each Vault is configured to use the **other cluster's Transit engine** to automatically unseal on restart. This removes the need for manual Shamir key entry after a pod restart.

```mermaid
sequenceDiagram
    participant vb as Vault beelink
    participant tg as Transit Engine\ngenmachine
    participant vg as Vault genmachine
    participant tb as Transit Engine\nbeelink

    Note over vb: Pod restarts (sealed)
    vb->>tg: Decrypt unseal key\n(key: unseal-beelink)
    tg-->>vb: Plaintext unseal key
    Note over vb: Vault unsealed

    Note over vg: Pod restarts (sealed)
    vg->>tb: Decrypt unseal key\n(key: unseal-genmachine)
    tb-->>vg: Plaintext unseal key
    Note over vg: Vault unsealed
```

### Helm configuration

The transit seal block is injected into the Vault `standalone.config` HCL via a Kubernetes secret:

```yaml
vault:
  server:
    extraSecretEnvironmentVars:
      - envName: TRANSIT_UNSEAL_TOKEN
        secretName: vault-transit-token
        secretKey: token
    standalone:
      enabled: true
      config: |-
        ui = true
        listener "tcp" {
          tls_disable = 1
          address     = "[::]:8200"
        }
        storage "file" {
          path = "/vault/data"
        }
        seal "transit" {
          address         = "https://vault.talos-genmachine.fredcorp.com"
          token           = "$TRANSIT_UNSEAL_TOKEN"
          key_name        = "unseal-beelink"
          mount_path      = "transit/"
          tls_skip_verify = "true"
        }
```

The `vault-transit-token` secret must be created **before** ArgoCD syncs Vault. Use the Taskfile helpers:

```bash
# Create the transit token secret on beelink (reads token from genmachine Vault)
task vault:unseal-secret:beelink

# Create the transit token secret on genmachine (reads token from beelink Vault)
task vault:unseal-secret:genmachine
```

### Circular deadlock recovery

> [!WARNING]
> If both Vaults restart simultaneously, they each try to contact the other's transit engine while both are sealed — causing a crash loop.

```mermaid
flowchart TD
    start["Both Vaults restart simultaneously"]
    sealed_b["Vault beelink: sealed\ntrying to contact genmachine transit"]
    sealed_g["Vault genmachine: sealed\ntrying to contact beelink transit"]
    crash["Both in CrashLoopBackOff\n503 — no available server"]

    start --> sealed_b & sealed_g
    sealed_b --> crash
    sealed_g --> crash

    crash -->|recover one first| fix["1. Strip seal block from ConfigMap\n2. Delete pod → Shamir unseal\n3. Restore seal block\n4. vault operator unseal -migrate"]
    fix -->|other unseals automatically| done["Both Vaults unsealed"]
```

Recovery is automated via Taskfile:

```bash
# Recover beelink first (will allow genmachine to auto-unseal)
task vault:break-deadlock:beelink

# Or recover genmachine first
task vault:break-deadlock:genmachine
```

## Seal Migration (Shamir → Transit)

When enabling transit auto-unseal on an existing Vault initialized with Shamir keys, a seal migration is required.

```mermaid
sequenceDiagram
    participant ops as Operator
    participant vault as Vault pod
    participant cm as ConfigMap

    ops->>cm: Add seal "transit" block to config
    ops->>vault: Delete pod (restart with new config)
    Note over vault: Vault starts in migration mode
    ops->>vault: vault operator unseal -migrate <shamir_key>
    Note over vault: Migration complete — sealed with transit
    vault->>vault: Auto-unseal via transit on next restart
```

```bash
vault operator unseal -migrate -address=https://vault.k0s-fullstack.fredcorp.com <shamir_key>
```

> [!NOTE]
> The `-migrate` flag is only accepted once — on the first unseal after the transit seal block is loaded. Subsequent restarts auto-unseal without any manual action.

## Authentication Methods

### Kubernetes Auth

Used by cert-manager and ExternalSecrets to authenticate with Vault using their ServiceAccount tokens:

```mermaid
sequenceDiagram
    participant app as cert-manager / ESO
    participant k8s as Kubernetes API
    participant vault as Vault

    app->>vault: Login with ServiceAccount JWT\n(auth/<cluster>-k8s/login)
    vault->>k8s: TokenReview — validate JWT
    k8s-->>vault: Token valid + bound SA info
    vault-->>app: Vault token (scoped to policy)
    app->>vault: Read secrets / sign certificates
```

Configure with:

```bash
task vault:eso-auth-setup cluster=genmachine
task vault:certmanager-auth-setup cluster=genmachine
```

### OIDC Auth

Human operators authenticate via Authentik SSO. See the [OIDC documentation](../authentication/oidc.md) for setup details.
