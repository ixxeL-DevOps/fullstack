
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 4c49fcee21d0f1c994e36eefb0aa1ed593093f5f
helm template . --name-template external-secrets-k0s --include-crds
```