
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 4abbb42b6a83415681e69681f563a1f499d07c38
helm template . --name-template external-secrets-k0s --include-crds
```