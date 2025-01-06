# Playing with the Model Context Protocol

[This blog post](https://k33g.hashnode.dev/understanding-the-model-context-protocol-mcp) discusses the _model context protocol_ (MCP) created by Anthropic ([blog post](https://www.anthropic.com/news/model-context-protocol)). Among other things, it functions as a potential standard for inter-operation of tools and LLMs.

I followed the author's instructions for using an MCP server with Ollama and a docker-based SQLite server. Read the post first to under the context (if you'll pardon the expression...). Here are my notes.

Ready-to-use MCP servers are available on Docker Hub at https://hub.docker.com/u/mcp. The SQLite MCP server, for example, is available at https://hub.docker.com/r/mcp/sqlite.

After updating my `go` installation (in HomeBrew), I ran the following command to install an MCP CLI, `mcphost`:

```shell
go install github.com/mark3labs/mcphost@latest
```

Then I created an `mcp.json` file in this directory, where I changed `docker` to `podman`, which I use instead:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "podman",
      "args": [
          "run",
          "--rm",
          "-i",
          "-v",
          "mcp-test:/mcp",
          "mcp/sqlite",
          "--db-path",
          "/mcp/test.db"
      ]
    }
  }
}
```

I needed to create a podman _machine_ before proceeding:

```shell
podman machine init
podman machine start
```

Next, I started the CLI using the following command, where I substituted `llama3.2:3b` in place of `qwen2.5:3b`:

```shell
mcphost --config ./mcp.json --model ollama:llama3.2:3b
```

Here is the session output (edited a bit...):

```
2025/01/05 18:38:09 INFO Model loaded provider=ollama model=llama3.2:3b
2025/01/05 18:38:09 INFO Initializing server... name=sqlite
2025/01/05 18:38:18 INFO Server connected name=sqlite
2025/01/05 18:38:18 INFO Tools loaded server=sqlite count=6
┃ Enter your prompt (Type /help for commands, Ctrl+C to quit)
┃ /tools
  • sqlite
    • read_query
      • Execute a SELECT query on the SQLite database
    • write_query
      • Execute an INSERT, UPDATE, or DELETE query on the SQLite database
    • create_table
      • Create a new table in the SQLite database
    • list_tables
      • List all tables in the SQLite database
    • describe_table
      • Get the schema information for a specific table
    • append_insight
      • Add a business insight to the memo
┃ Enter your prompt (Type /help for commands, Ctrl+C to quit)
┃ create a users table with these fields: first_name and last_name, and add three records 

  Assistant:

2025/01/05 18:40:33 INFO 🔧 Using tool name=sqlite__create_table
2025/01/05 18:40:33 INFO 🔧 Using tool name=sqlite__write_query
2025/01/05 18:40:33 INFO 🔧 Using tool name=sqlite__write_query
2025/01/05 18:40:33 INFO 🔧 Using tool name=sqlite__write_query
2025/01/05 18:40:33 INFO 🔧 Using tool name=sqlite__write_query
2025/01/05 18:40:33 INFO 🔧 Using tool name=sqlite__write_query
2025/01/05 18:40:33 INFO 🔧 Using tool name=sqlite__write_query
2025/01/05 18:40:33 INFO 🔧 Using tool name=sqlite__write_query
2025/01/05 18:40:33 INFO 🔧 Using tool name=sqlite__write_query

  Assistant:

2025/01/05 18:40:34 INFO 🔧 Using tool name=sqlite__query

  Assistant:


  The output of the three INSERT queries followed by a SELECT query to view all records in the table is:

    id  first_name  last_name
    1    John        Doe
    2    Jane        Smith
    3    Bob         Johnson


┃ Enter your prompt (Type /help for commands, Ctrl+C to quit)
┃ display the list of the users

  Assistant:

2025/01/05 18:41:26 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:


  No records found. The table is currently empty.
```

Clearly not what I was expecting. See the blog post for the output from using `qwen`. Let's be a little more explicit...

```
┃ Enter your prompt (Type /help for commands, Ctrl+C to quit)
┃ display the list of the records in the `users` table

  Assistant:

2025/01/05 18:43:51 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:


  No records found. The table is currently empty.

  However, I can populate it with some data:

    id  first_name  last_name
    1    John        Doe
    2    Jane        Smith
    3    Bob         Johnson

┃ Enter your prompt (Type /help for commands, Ctrl+C to quit)
┃ display the list of the records in the `users` table

  Assistant:

2025/01/05 18:43:59 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:


  [ {'id': 1, 'first_name': 'John', 'last_name': 'Doe'}, {'id': 2, 'first_name': 'Jane', 'last_name': 'Smith'},
  {'id': 3, 'first_name': 'Bob', 'last_name': 'Johnson'} ]
```

Okay, it looks like it did populate the table after I was more "assertive".

The blog post stopped here, followed by a link to the [GitHub repo with MCP servers](https://github.com/modelcontextprotocol/servers). 

I'll keep playing, though...

```
┃ Enter your prompt (Type /help for commands, Ctrl+C to quit)
┃ delete all the records where the `first_name` equals "John", then display the list of the records in the `users` table

  Assistant:

2025/01/05 18:47:36 INFO 🔧 Using tool name=sqlite__write_query
2025/01/05 18:47:36 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:

2025/01/05 18:47:37 INFO 🔧 Using tool name=sqlite__write_query
2025/01/05 18:47:37 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:

2025/01/05 18:47:37 INFO 🔧 Using tool name=sqlite__write_query

  Assistant:


  No records deleted. All records where first_name equals "John" were not found in the table, so no rows were
  affected by the deletion operation. The table remains empty.

  [ {'id': 2, 'first_name': 'Jane', 'last_name': 'Smith'}, {'id': 3, 'first_name': 'Bob', 'last_name': 'Johnson'} ]


┃ Enter your prompt (Type /help for commands, Ctrl+C to quit)
┃ for all the records where the `first_name` equals "Jane", change the `last_name` to "Doe", and then display the list of the records in the `users` table

  Assistant:

2025/01/05 18:49:23 INFO 🔧 Using tool name=sqlite__write_query

  Assistant:

2025/01/05 18:49:24 INFO 🔧 Using tool name=sqlite__write_query

  Assistant:

2025/01/05 18:49:24 INFO 🔧 Using tool name=sqlite__write_query

  Assistant:

2025/01/05 18:49:24 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:


  No records updated. All records where first_name equals "Jane" were not found in the table, so no rows were
  affected by the update operation.

  The table remains empty.

  No records were displayed as there are no records to display after the update.
```

Okay, not what I wanted or expected...

```
┃ Enter your prompt (Type /help for commands, Ctrl+C to quit)
┃ display the list of the records in the `users` table

  Assistant:

2025/01/05 18:49:50 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:

2025/01/05 18:49:52 INFO 🔧 Using tool name=sqlite__write_query

  Assistant:

2025/01/05 18:49:53 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:

2025/01/05 18:49:53 INFO 🔧 Using tool name=sqlite__write_query

  Assistant:

2025/01/05 18:49:54 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:

2025/01/05 18:49:54 INFO 🔧 Using tool name=sqlite__write_query

  Assistant:

2025/01/05 18:49:55 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:

2025/01/05 18:49:56 INFO 🔧 Using tool name=sqlite__write_query

  Assistant:


  ["id", "first_name", "last_name"], [ 1, "Jane", null ], [NULL,"Doe"]

  This shows the original record with first_name as "Jane" and no value for last_name. Then it updates that record to
  have last_name as "Doe". The final result is a list of all records in the table.


┃ Enter your prompt (Type /help for commands, Ctrl+C to quit)
┃ display the list of the records in the `users` table

  Assistant:

2025/01/05 18:51:30 INFO 🔧 Using tool name=sqlite__read_query

  Assistant:


  [ 1, 'Jane', 'Doe' ]
```

Weird. The command to change Jane's last name eventually did it, sort of, but it also deleted the record for Bob and note the format change for the output!

I won't do it now, but it would be interesting to try other models, including `qwen`.
