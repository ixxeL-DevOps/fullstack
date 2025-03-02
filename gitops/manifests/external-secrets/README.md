
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9c7c4527da501ecacc3b7d008843b58dd7864cf3
helm template . --name-template external-secrets-k0s --include-crds
```