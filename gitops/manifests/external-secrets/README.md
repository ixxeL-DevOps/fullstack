
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 347bdc99e4a41eab0659e7e6929241b4fd699e80
helm template . --name-template external-secrets-k0s --include-crds
```