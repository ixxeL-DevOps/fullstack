
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout aeccb037e382394210d077b8ce58feb9034005a7
helm template . --name-template external-secrets-k0s --include-crds
```