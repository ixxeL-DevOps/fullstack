
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 37092787ee8319521c5b9b721cc103f1a1db9f92
helm template . --name-template external-secrets-k0s --include-crds
```