# maintenance-tools

## using all-repos

https://github.com/asottile/all-repos

```bash
pip install all-repos
```

### other commands

- all-repos-find-files
- all-repos-grep
- all-repos-list-repos
- all-repos-manual
- all-repos-sed

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
