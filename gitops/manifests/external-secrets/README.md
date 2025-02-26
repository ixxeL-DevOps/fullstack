
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 090e50100c01f9e235232496d455195beed88307
helm template . --name-template external-secrets-k0s --include-crds
```