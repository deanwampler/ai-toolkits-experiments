# README for `ai-toolkits-experiments`

My private repo for experimenting with different Gen AI toolkits, especially for local execution on systems like Apple Silicon, application patterns like RAG and agents, etc.

This repo uses [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) of other repos, such as the toolkits themselves. Hence, to get those submdules, you can pass `--recurse-submodules` when you clone this repo or initialize them seperately.

All at once:

```shell
git clone --recurse-submodules https://github.com/deanwampler/ai-toolkits-experiments
```

Or after cloning the repo, do the following:

```shell
git submodule update --init --recursive
```

## Notes on Particular Projects

Most of the project subfolders have their own READMEs. In a few cases, additional commands are required to get started, which are documented in the corresponding README.
