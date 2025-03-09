# Encryption

## SOPS

Using SOPS in combination with HC Vault to encrypt/decrypt sensitive files:

Login to Vault:

```yaml
vault login -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com
```

Enable `transit` engine for SOPS:

```yaml
vault secrets enable -tls-skip-verify \
-address=https://vault.k0s-fullstack.fredcorp.com \
-path=sops transit
```

Create a key to encrypt/decrypt files:

```yaml
vault write -tls-skip-verify \
-address=https://vault.k0s-fullstack.fredcorp.com \
sops/keys/talos \
type=rsa-4096
```

You can use SOPS CLI to encrypt/decrypt files :

```bash
sops encrypt --hc-vault-transit https://vault.k0s-fullstack.fredcorp.com/v1/sops/keys/talos vault_example.yml
```

And also use a config file `.sops.yaml` :

```yaml
---
creation_rules:
  - path_regex: .*\.sops\.ya?ml$
    hc_vault_transit_uri: 'https://vault.k0s-fullstack.fredcorp.com/v1/sops/keys/talos'
```

then just use :

```bash
sops decrypt --in-place test.yaml
```

If you need to delete the transit key, you must enable it in the UI first and then execute :

```bash
vault delete -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com sops/keys/talos
```
