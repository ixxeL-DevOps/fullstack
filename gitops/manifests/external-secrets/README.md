
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout aa26298571ff27030e27f93215f2fe04074b92e0
helm template . --name-template external-secrets-k0s --include-crds
```