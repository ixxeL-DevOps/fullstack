
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 29654235a0c120f6d6ae047201bcbb9f513380da
helm template . --name-template external-secrets-k0s --include-crds
```