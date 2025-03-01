
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 7bdf7956a8e6e6b8d46034c8057cbd74ceae9bff
helm template . --name-template external-secrets-k0s --include-crds
```