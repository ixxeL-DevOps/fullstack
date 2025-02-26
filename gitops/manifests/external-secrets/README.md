
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout a22fbe7b5bce6ea4dbf02a7dd6355fa86cbd1b8e
helm template . --name-template external-secrets-k0s --include-crds
```