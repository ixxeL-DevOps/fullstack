
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 5639e1554a7a59d39604dde99393e703b7c8440f
helm template . --name-template external-secrets-k0s --include-crds
```