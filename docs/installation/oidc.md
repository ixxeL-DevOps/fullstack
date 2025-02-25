# OIDC

## Vault

Blueprint for Vault OIDC auth :

```yaml
---
version: 1
metadata:
  name: fullstack-vault
entries:
  - id: provider
    model: authentik_providers_oauth2.oauth2provider
    state: 'present'
    identifiers:
      name: fullstack-vault
    attrs:
      authorization_flow: !Find [authentik_flows.flow, [slug, default-provider-authorization-implicit-consent]]
      invalidation_flow: !Find [authentik_flows.flow, [slug, default-invalidation-flow]]
      signing_key: !Find [authentik_crypto.certificatekeypair, [name, authentik Self-signed Certificate]]
      client_type: confidential
      redirect_uris:
        - url: https://vault.k0s-fullstack.fredcorp.com/oidc/callback
          matching_mode: strict
        - url: https://vault.k0s-fullstack.fredcorp.com/ui/vault/auth/oidc/oidc/callback
          matching_mode: strict

      access_code_validity: minutes=1
      access_token_validity: hours=1
      refresh_token_validity: days=30

      sub_mode: hashed_user_id
      property_mappings:
        - !Find [authentik_core.propertymapping, [name, "authentik default OAuth Mapping: OpenID 'openid'"]]
        - !Find [authentik_core.propertymapping, [name, "authentik default OAuth Mapping: OpenID 'profile'"]]
        - !Find [authentik_core.propertymapping, [name, "authentik default OAuth Mapping: OpenID 'email'"]]

  - id: application
    model: authentik_core.application
    state: 'present'
    identifiers:
      name: 'fullstack-vault'
    attrs:
      name: fullstack-vault
      group: Infrastructure
      meta_description: HashiCorp Vault
      provider: !Find [authentik_providers_oauth2.oauth2provider, [name, fullstack-vault]]
      policy_engine_mode: any
      slug: fullstack-vault
```

Vault must be configured for OIDC provider with Authentik :

- `ca.pem` : is the CA chain for the Authentik certificate
- `fullstack-vault` : is the Authentik application slug

```bash
vault login -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com

vault write -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com auth/oidc/config oidc_discovery_url="https://authentik.k0s-fullstack.fredcorp.com/application/o/fullstack-vault/" oidc_client_id="<authentik-provider-client-id>" oidc_client_secret="<authentik-provider-client-secret>" default_role="reader" oidc_discovery_ca_pem=@ca.pem

vault write -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com auth/oidc/role/reader bound_audiences="<authentik-provider-client-id>" allowed_redirect_uris="https://vault.k0s-fullstack.fredcorp.com/ui/vault/auth/oidc/oidc/callback" allowed_redirect_uris="https://vault.k0s-fullstack.fredcorp.com/oidc/callback" user_claim="sub" policies="reader"
```

To manage groups, you can configure following:

```bash
vault write -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com auth/oidc/role/reader bound_audiences="<authentik-provider-client-id>" allowed_redirect_uris="https://vault.k0s-fullstack.fredcorp.com/ui/vault/auth/oidc/oidc/callback" allowed_redirect_uris="https://vault.k0s-fullstack.fredcorp.com/oidc/callback" us
er_claim="sub" policies="reader" groups_claim="groups" oidc_scopes=[ "openid profile email" ]

vault write -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com identity/group name="administrator" policies="administrator" type="external" metadata=responsibility="Manage Vault instance"
```

Access information with:

```bash
vault auth list -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com
vault read -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com identity/group/name/administrator
```

Link to Authentik:

```bash
vault write -tls-skip-verify -address=https://vault.k0s-fullstack.fredcorp.com identity/group-alias mount_accessor="auth_oidc_b59bc9a6" canonical_id="cbd6e4ac-e516-4424-742a-41a978252bb6" name="group name in authentik"
```

You need to Create an Authentik group named `group name in authentik` and a Vault policy for admins like that :

```hcl
path "*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
```
