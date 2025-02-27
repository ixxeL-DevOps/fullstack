
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 093d2d0d791bafd71a03feedde72d78f83eb664d
helm template . --name-template external-secrets-k0s --include-crds
```