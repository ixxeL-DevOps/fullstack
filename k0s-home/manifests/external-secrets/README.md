
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 581642ccb2340af83c07a94e7f863a2ef4aba0d7
helm template . --name-template external-secrets-k0s --include-crds
```