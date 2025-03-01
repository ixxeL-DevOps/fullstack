
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9880f0e55e49262fd83c06ca5ab0f1dec4d0a4a3
helm template . --name-template external-secrets-k0s --include-crds
```