# Jira-Select: Easily export issues from Jira to CSV

## Quickstart

First, you need to configure `jira-csv` to connect to your jira instance:

```
jira-csv configure
```

Then, you'll need to create a yaml file describing your query and save it
somewhere; example:

```yaml
select:
  - key
  - summary
  - timetracking.originalEstimate as "Hours Estimate"
  - customfield_10048 as "My Important Field"
from: issues
where:
  - labels = "frontend"
  - assignee = "me@adamcoddington.net"
  - resolution is null
```

Now you can run your query:

```
jira-csv run /path/to/query.yaml
```

& it'll hand you back a CSV document with the fields you've selected.

See the built-in help (`--help`) for more options.

## Future Goals

- SQlite support: Instead of exporting a CSV, exporting an SQLite database.
- XLSX support: Instead of exporting a CSV, exporing an XLSX document.
- Output formatting: Support for output formatting functions so you can
  do things like look up the name of a sprint instead of just showing the
  ID. This will probably take the form of a function call wrapping the
  field name that matches the name of an entrypoint in `jira_csv_functions`.
- Python filtering: Support for filtering rows to ones that meet specific
  conditions using python code. I'm imagining being represented in a
  `having:` section of the query yaml.
