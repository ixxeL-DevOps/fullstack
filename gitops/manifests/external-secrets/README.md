
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 242d45b6da9b492c5bfab20eac502127b57097de
helm template . --name-template external-secrets-k0s --include-crds
```