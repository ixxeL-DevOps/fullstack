
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout cd23e3570c7c1852179cd26a7954191c2b61a51f
helm template . --name-template external-secrets-k0s --include-crds
```