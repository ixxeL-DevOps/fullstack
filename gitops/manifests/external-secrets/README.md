
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 146de9e379d9606a421e6164ce3011db7ff795e8
helm template . --name-template external-secrets-k0s --include-crds
```