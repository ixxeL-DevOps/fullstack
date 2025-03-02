
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 039d2dd76f6fa5a11f0ff52156a19c35c29d8d9a
helm template . --name-template external-secrets-k0s --include-crds
```