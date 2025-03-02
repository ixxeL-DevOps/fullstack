
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 62920e7121b21f4bfe46894a79af37b4c00f5413
helm template . --name-template external-secrets-k0s --include-crds
```