
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 1019f7b1a2eb7eb2152189be76a275ad1d306a92
helm template . --name-template external-secrets-k0s --include-crds
```