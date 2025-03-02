
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 656ea117c6d7e3012fc145c324037d170f537f88
helm template . --name-template external-secrets-k0s --include-crds
```