
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout b45fb7f3ea3245cb7ddbcff27acc98b95187d702
helm template . --name-template external-secrets-k0s --include-crds
```