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

## WireGuard Portal

Wiregard portal relies on `is_admin` property to make user admin of the server. This property can be passed as an OIDC claim with a specific script in `Scope Mapping` and then added to the provider:

```py
return {
  "is_admin": ak_is_group_member(request.user, name="Wireguard admins")
}
```

The configuration need to be made as OIDC :

```yaml
config:
  core:
    admin_user: '${ADMIN_USER}'
    admin_password: '${ADMIN_PASSWORD}'
    import_existing: false
    create_default_peer: true
    self_provisioning_allowed: true

  auth:
    callback_url_prefix: https://wireguard.k0s-fullstack.fredcorp.com/api/v0
    oidc:
      - id: Authentik
        provider_name: Authentik
        display_name: OIDC Authentik
        base_url: https://authentik.k0s-fullstack.fredcorp.com/application/o/fullstack-wireguard/
        client_id: '${OIDC_CLIENT_ID}'
        client_secret: '${OIDC_CLIENT_SECRET}'
        extra_scopes:
          - profile
          - email
          - openid
          - is_admin
        field_map:
          email: email
          user_identifier: email
          is_admin: is_admin
        registration_enabled: true
        log_user_info: false
```

The variables here can be injected with kubernetes `Secret` in `values.yaml` file:

```yaml
# OIDC secret config
envFrom:
  - secretRef:
      name: oidc-wireguard
  - secretRef:
      name: admin-wireguard
```

In Authentik, you need to specify the `is_admin` in the provider properties:

```yaml
- id: provider
  model: authentik_providers_oauth2.oauth2provider
  state: present
  identifiers:
    name: fullstack-wireguard
  attrs:
    authorization_flow: !Find [authentik_flows.flow, [slug, default-provider-authorization-implicit-consent]]
    invalidation_flow: !Find [authentik_flows.flow, [slug, default-invalidation-flow]]
    signing_key: !Find [authentik_crypto.certificatekeypair, [name, authentik Self-signed Certificate]]
    client_type: confidential
    redirect_uris:
      - url: https://wireguard.k0s-fullstack.fredcorp.com/api/v0/auth/login/authentik/callback
        matching_mode: strict

    access_code_validity: minutes=1
    access_token_validity: hours=1
    refresh_token_validity: hours=1

    sub_mode: hashed_user_id
    property_mappings:
      - !Find [authentik_core.propertymapping, [name, "authentik default OAuth Mapping: OpenID 'openid'"]]
      - !Find [authentik_core.propertymapping, [name, "authentik default OAuth Mapping: OpenID 'profile'"]]
      - !Find [authentik_core.propertymapping, [name, "authentik default OAuth Mapping: OpenID 'email'"]]
      - !Find [authentik_core.propertymapping, [name, "OAuth mapping: OpenID 'is_admin' for Wireguard"]]

  - model: authentik_providers_oauth2.scopemapping
    identifiers:
      name: "OAuth mapping: OpenID 'is_admin' for Wireguard"
    attrs:
      description: is_admin claim for Wireguard Portal OIDC
      expression: |
        return {
          "is_admin": ak_is_group_member(request.user, name="Wireguard admins")
        }
      name: wireguard-is-admin
      scope_name: is_admin
```

## Homarr

Homarr is easy to integrate with OIDC. You just need to specify some variables in the `env` key from `values.yaml` file:

```yaml
env:
  AUTH_PROVIDERS: credentials,oidc
  AUTH_SESSION_EXPIRY_TIME: 1h
  AUTH_OIDC_AUTO_LOGIN: 'false'
  AUTH_OIDC_ISSUER: https://authentik.k0s-fullstack.fredcorp.com/application/o/fullstack-homarr/
  AUTH_OIDC_URI: 'https://authentik.k0s-fullstack.fredcorp.com/application/o/authorize/'
  AUTH_OIDC_CLIENT_NAME: Authentik
  AUTH_OIDC_SCOPE_OVERWRITE: openid email profile groups
  AUTH_OIDC_GROUPS_ATTRIBUTE: groups
  AUTH_LOGOUT_REDIRECT_URL: https://homarr.k0s-fullstack.fredcorp.com/auth/login
```

And you can used `Secret` to inject ClientID and ClientSecret for OIDS auth:

```yaml
envSecrets:
  authOidcCredentials:
    existingSecret: auth-oidc-secret
    oidcClientId: oidc-client-id
    oidcClientSecret: oidc-client-secret
```

Variable `NODE_TLS_REJECT_UNAUTHORIZED: '0'` can be used in case certificates are not recognized. Th
