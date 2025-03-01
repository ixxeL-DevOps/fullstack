
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 715131dcb44b296a45197f842827ac1cacc7b084
helm template . --name-template external-secrets-k0s --include-crds
```