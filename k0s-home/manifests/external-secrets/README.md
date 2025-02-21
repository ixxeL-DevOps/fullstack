
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ec0cae89376ecd96a3a96a29a1d7c9a0aa02a72e
helm template . --name-template external-secrets-k0s --include-crds
```