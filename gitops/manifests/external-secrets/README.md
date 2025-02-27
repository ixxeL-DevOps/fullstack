
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 671b6a5ae4802eec417a341f7aa873dffed74d6e
helm template . --name-template external-secrets-k0s --include-crds
```