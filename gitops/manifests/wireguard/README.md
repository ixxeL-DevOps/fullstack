
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 832917c084d713062fd70a20cf307eb97b1838f6
helm template . --name-template wireguard-k0s --include-crds
```