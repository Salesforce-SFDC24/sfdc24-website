# summary

Execute a GraphQL statement.

# description

Specify the GraphQL statement with the "--body" flag, either directly at the command line or with a file that contains the statement. You can query Salesforce records using a "query" statement or use mutations to modify Salesforce records.

This command uses the GraphQL API to query or modify Salesforce objects. For details about the API, and examples of queries and mutations, see https://developer.salesforce.com/docs/platform/graphql/guide/graphql-about.html.

# examples

- Execute a GraphQL query on the Account object by specifying the query directly to the "--body" flag; the command uses your default org:

  <%= config.bin %> <%= command.id %> --body "query accounts { uiapi { query { Account { edges { node { Id \n Name { value } } } } } } }"

- Read the GraphQL statement from a file called "example.txt" and execute it on an org with alias "my-org":

  <%= config.bin %> <%= command.id %> --body example.txt --target-org my-org

- Pipe the GraphQL statement that you want to execute from standard input to the command:

  $ echo graphql | sf api request graphql --body -

- Write the output of the command to a file called "output.txt" and include the HTTP response status and headers:

  <%= config.bin %> <%= command.id %> --body example.txt --stream-to-file output.txt --include

# flags.body.summary

File or content with the GraphQL statement. Specify "-" to read from standard input.
