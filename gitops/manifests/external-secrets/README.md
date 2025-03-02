
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout f772b5345d2c608cffc9e4d493fb3186c047b184
helm template . --name-template external-secrets-k0s --include-crds
```