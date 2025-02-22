
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout e236a71da251ee2bccbcdb580d3c28822a37a9d3
helm template . --name-template external-secrets-k0s --include-crds
```