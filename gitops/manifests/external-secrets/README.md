
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout aa4db9a7f7a5cfb923f16b49c216e15a94267cbe
helm template . --name-template external-secrets-k0s --include-crds
```