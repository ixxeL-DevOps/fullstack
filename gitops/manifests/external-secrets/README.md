
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout a7184a0e7ace3692be376318bef15ef3528d6069
helm template . --name-template external-secrets-k0s --include-crds
```