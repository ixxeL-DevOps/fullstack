
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 828f5016b6496c0b1391e6dbf313cb215c814b1f
helm template . --name-template external-secrets-k0s --include-crds
```