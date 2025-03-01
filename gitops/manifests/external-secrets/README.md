
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9a0c786c52ac9dfdadea555d951ad68ef6bd84dd
helm template . --name-template external-secrets-k0s --include-crds
```