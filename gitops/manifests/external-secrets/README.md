
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ea5818ca8035fdd29a3f28bfca4a1bbc9476ff08
helm template . --name-template external-secrets-k0s --include-crds
```