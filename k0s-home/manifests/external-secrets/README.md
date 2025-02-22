
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout eecd1ba30a9029ec516f63ff464e842f2c26926f
helm template . --name-template external-secrets-k0s --include-crds
```