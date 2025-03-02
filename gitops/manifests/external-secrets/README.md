
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout e5af31b57a8d0acd3b05af30fb04267d3aeafdd5
helm template . --name-template external-secrets-k0s --include-crds
```