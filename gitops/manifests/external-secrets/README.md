
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 1d4695015aa546bc8f3aea16ae152c8e32589453
helm template . --name-template external-secrets-k0s --include-crds
```