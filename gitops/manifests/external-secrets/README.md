
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout c669a89163e339825160fce4cf51818f5bc20d96
helm template . --name-template external-secrets-k0s --include-crds
```