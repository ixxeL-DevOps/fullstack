
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 28972702fa34ec141a1eeefbe8715ed9f40b744f
helm template . --name-template external-secrets-k0s --include-crds
```