# OIDC

## Reverse-Proxy setup : Traefik

### In-cluster setup

Traefik needs to be configured to act as a reverse proxy with Authentik. Use this `Middleware` with the added `authorization` header from the official documentation to be able to pass **Basic Auth** headers in case you need to login transparently to non OIDC servers.

```yaml
---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: authentik
spec:
  forwardAuth:
    address: http://ak-outpost-authentik-embedded-outpost.authentik:9000/outpost.goauthentik.io/auth/traefik
    trustForwardHeader: true
    authResponseHeaders:
      - X-authentik-username
      - X-authentik-groups
      - X-authentik-entitlements
      - X-authentik-email
      - X-authentik-name
      - X-authentik-uid
      - X-authentik-jwt
      - X-authentik-meta-jwks
      - X-authentik-meta-outpost
      - X-authentik-meta-provider
      - X-authentik-meta-app
      - X-authentik-meta-version
      - authorization
```

The field `address` should point to your authentik outpost service inside the cluster:

```console
NAME                                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
ak-outpost-authentik-embedded-outpost   ClusterIP   10.96.153.169    <none>        9000/TCP,9300/TCP,9443/TCP   5d16h
authentik-k0s-postgresql                ClusterIP   10.97.192.194    <none>        5432/TCP                     4d15h
authentik-k0s-postgresql-hl             ClusterIP   None             <none>        5432/TCP                     4d15h
authentik-k0s-redis-headless            ClusterIP   None             <none>        6379/TCP                     4d15h
authentik-k0s-redis-master              ClusterIP   10.101.158.29    <none>        6379/TCP                     4d15h
authentik-k0s-server                    ClusterIP   10.111.223.218   <none>        80/TCP,443/TCP               4d15h
```

You also need to add annotation to Traefik `Ingress`. The pattern here is
`<namespace>-<middleware-name>@kubernetescrd` :

```yaml
annotations:
  traefik.ingress.kubernetes.io/router.middlewares: traefik-authentik@kubernetescrd
```

For `IngressRoute` you have to specify differently :

```yaml
---
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: traefik-k0s-dashboard
spec:
  entryPoints:
    - web
    - websecure
  routes:
    - kind: Rule
      match: Host(`traefik.k0s-fullstack.fredcorp.com`)
      middlewares:
        - name: authentik
          namespace: traefik
      priority: 10
      services:
        - kind: TraefikService
          name: api@internal
          namespace: traefik
    - kind: Rule
      match: Host(`traefik.k0s-fullstack.fredcorp.com`) && PathPrefix(`/outpost.goauthentik.io/`)
      priority: 15
      services:
        - kind: Service
          name: ak-outpost-authentik-embedded-outpost
          namespace: authentik
          port: 9000
```

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
