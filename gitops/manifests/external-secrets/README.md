
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout bf2d2fcc58a841e75ce44711dbf8cbb4f47e86e3
helm template . --name-template external-secrets-k0s --include-crds
```