
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3595cec82410921bfdd27734784e4bed48a7d494
helm template . --name-template wireguard-k0s --include-crds
```