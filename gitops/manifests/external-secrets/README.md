
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout a631a5ada319cc1e19474819076be1c0d561d574
helm template . --name-template external-secrets-k0s --include-crds
```