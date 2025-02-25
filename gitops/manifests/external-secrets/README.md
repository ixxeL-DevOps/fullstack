
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout eb5cfa263df0dde71f8700297888728a58f28e5f
helm template . --name-template external-secrets-k0s --include-crds
```