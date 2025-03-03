# Forward Auth

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

You also need to add annotation to Traefik `Ingress`. The pattern here is `<namespace>-<middleware-name>@kubernetescrd` :

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
