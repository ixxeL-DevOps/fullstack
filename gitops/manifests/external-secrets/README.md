
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3e7d8ed4315c2fdf90e812f5a553f476285c0a24
helm template . --name-template external-secrets-k0s --include-crds
```