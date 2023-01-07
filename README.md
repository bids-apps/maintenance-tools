# maintenance-tools

## using all-repos

https://github.com/asottile/all-repos

```bash
pip install all-repos
```

### other commands

- `all-repos-grep`

```bash
all-repos-grep ':image' -- .circleci/config.yml
```

- `all-repos-sed`

```bash
all-repos-sed \
    "s@image: circleci/buildpack-deps:stretch@image: ubuntu-2204:2022.10.2@g" \
    .circleci/config.yml \
    --commit-msg "use ubuntu image"
```

- `all-repos-find-files`
- `all-repos-list-repos`
- `all-repos-manual`

### Cloning all the repos

```bash
all-repos-clone -C all-repos.json
```

### Configuration

Currently, the config file is set to no to anything on the repo

```json
"push": "all_repos.push.readonly",
```

See the all-repos doc to see how to change this.

You can filter the repos to clone by adding a `include` or `exclude` key to the
`all-repos.json` file.
