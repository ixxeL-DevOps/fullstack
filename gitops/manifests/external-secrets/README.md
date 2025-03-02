
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 7cf83a4d9be15120532d2f8406c6a822865cf24b
helm template . --name-template external-secrets-k0s --include-crds
```