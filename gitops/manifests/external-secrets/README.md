
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 229a370cf3aa2e8c48bb7739e50a7bc632abedfb
helm template . --name-template external-secrets-k0s --include-crds
```