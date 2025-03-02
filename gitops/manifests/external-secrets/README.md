
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 736aff835da8bab5bba24a7a5c5a746eaddf496f
helm template . --name-template external-secrets-k0s --include-crds
```