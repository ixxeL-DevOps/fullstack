
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9de70700db2be2155e546baa56208d09bf18240d
helm template . --name-template external-secrets-k0s --include-crds
```