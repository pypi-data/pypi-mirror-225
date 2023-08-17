PolyRepo
========

Manage a collection of repos in a directory/subdirectory structure that matches the group/subgroup structure in GitLab.

Installation and Use
--------------------

As a WIP, PolyRepo supports only the `groups` command, which lists a group and all its subgroups.

To install: `pipx install polyrepo`

To configure, create a `~/.polyrepo.yml` file that looks like this:

```yaml
gitlab:
  host: gitlab.com
  token: glpat-aaaaaaaaaaaaaaaaaaaa
```

(The token is optional if you're just pulling public groups/subgroups)

Then:

```bash
polyrepo groups gitlab-org
```

... with the path to the group you want to examine.

Proposed functionality
----------------------

```
polyrepo sync steampunk-wizard
```

In a subdirectory called steampunk-wizard, clone all its subgroups and projects.

If a subdirectory doesn't exist, create it to hold the clone.

If a subdirectory exists for a project:

1. Confirm that the default git remote points to the correct path in GitLab
2. Optionally, fetch everything, including tags

If a subdirectory exists that does NOT correspond to a GitLab repo, remove it?

Output in text

```
/steampunk-wizard/busy                 Created
/steampunk-wizard/labcrawler           Disjoin
/steampunk-wizard/mypyref              Correct  Changed  
/steampunk-wizard/sandbox/ci-sandbox   Fetched
/steampunk-wizard/sandbox/play-around  Missing
```

Statuses:

- **Created** The repo did not previously exist locally, and now has been cloned and fetched.
- **Fetched** The repo did exist, and has been fetched
- **Correct** Was already up to date; no changes
- **Missing** There is no repo in GitLab, but there's a local folder with content
- **Disjoin** A local directory exists, but either isn't a git repo or has the wrong default remote

Then **Changed** means local changes exist, which could include

- Local branches still to be pushed
- Commits in a branch beyond what was fetched
- Local changes to be committed

Note that PolyRepo doesn't pull or merge anything, doesn't touch the working directory except in the case of creation, and ...

There's a .polyrepo file (optional) to specify the subgroups/repos to consider.

Questions

- How to handle moves of repos between namespaces?
- Any operation to polyrepo every namespace the user can access?
