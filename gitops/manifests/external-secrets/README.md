
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout d6aee2928b0b7955452b731d637ec8b0a26f8c0e
helm template . --name-template external-secrets-k0s --include-crds
```