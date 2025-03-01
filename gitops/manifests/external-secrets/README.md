
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout aeaa0bfde2820692d355c5136989625e100071bf
helm template . --name-template external-secrets-k0s --include-crds
```