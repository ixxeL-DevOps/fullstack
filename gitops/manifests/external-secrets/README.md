
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ef7b2aee3c96fa307461f96fa2051b463b34dbe8
helm template . --name-template external-secrets-k0s --include-crds
```