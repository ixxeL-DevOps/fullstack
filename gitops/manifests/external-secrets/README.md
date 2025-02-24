
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 504182688dbf81d1e71a3076865d2e507ecc4f2d
helm template . --name-template external-secrets-k0s --include-crds
```