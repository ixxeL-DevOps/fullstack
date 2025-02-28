
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout e1fb791b7125b61aeda9d2707b1ad035e1e86945
helm template . --name-template external-secrets-k0s --include-crds
```