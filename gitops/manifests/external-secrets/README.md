
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 04eb18072b68bf398078882bc175a5502ca3eb8e
helm template . --name-template external-secrets-k0s --include-crds
```