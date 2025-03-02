
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 20e06b72faa236e3f2999e0948e035c3646785a3
helm template . --name-template external-secrets-k0s --include-crds
```