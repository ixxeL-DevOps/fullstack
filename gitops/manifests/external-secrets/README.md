
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3776673e5d11064edf36d4c66ff38b37f55af88f
helm template . --name-template external-secrets-k0s --include-crds
```