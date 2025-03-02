
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 979fec551277d1697049f5e9ab32b9183c27ca94
helm template . --name-template external-secrets-k0s --include-crds
```