
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout efb55c67ea5d569a2b35a630b8753e53545def1f
helm template . --name-template external-secrets-k0s --include-crds
```