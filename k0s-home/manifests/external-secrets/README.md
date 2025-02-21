
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout a78a261b239b0b0e5e9ad2c945859ee449d6045a
helm template . --name-template external-secrets-k0s --include-crds
```