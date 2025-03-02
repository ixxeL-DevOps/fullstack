
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout fb3e60208e31e682acc2cc2eb30ca0a827227faf
helm template . --name-template external-secrets-k0s --include-crds
```