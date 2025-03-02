
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout e92c563398cd70cc7a93a29cc81b4ed9b225a046
helm template . --name-template external-secrets-k0s --include-crds
```