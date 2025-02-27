
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 45587903b94ae0bb3f2680ff8ab3cc149b9163e3
helm template . --name-template external-secrets-k0s --include-crds
```