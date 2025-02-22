
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 65b48639b988eacd407a320a08fb7d5b0cee264e
helm template . --name-template external-secrets-k0s --include-crds
```