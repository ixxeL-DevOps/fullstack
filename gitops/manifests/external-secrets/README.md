
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout dcca9225f473b7f0185268709452db7442ae214d
helm template . --name-template external-secrets-k0s --include-crds
```