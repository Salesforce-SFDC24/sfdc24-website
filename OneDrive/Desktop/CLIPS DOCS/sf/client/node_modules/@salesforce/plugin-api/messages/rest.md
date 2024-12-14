# summary

Make an authenticated HTTP request using the Salesforce REST API.

# description

When sending the HTTP request with the "--body" flag, you can specify the request directly at the command line or with a file that contains the request.

For a full list of supported REST endpoints and resources, see https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_list.htm.

# examples

- List information about limits in the org with alias "my-org":

  <%= config.bin %> <%= command.id %> 'services/data/v56.0/limits' --target-org my-org

- List all endpoints in your default org; write the output to a file called "output.txt" and include the HTTP response status and headers:

  <%= config.bin %> <%= command.id %> '/services/data/v56.0/' --stream-to-file output.txt --include

- Get the response in XML format by specifying the "Accept" HTTP header:

  <%= config.bin %> <%= command.id %> '/services/data/v56.0/limits' --header 'Accept: application/xml'

- Create an account record using the POST method; specify the request details directly in the "--body" flag:

  <%= config.bin %> <%= command.id %> /services/data/v56.0/sobjects/account --body "{\"Name\" : \"Account from REST API\",\"ShippingCity\" : \"Boise\"}" --method POST

- Create an account record using the information in a file called "info.json" (note the @ prefixing the file name):

  <%= config.bin %> <%= command.id %> '/services/data/v56.0/sobjects/account' --body @info.json --method POST

- Update an account record using the PATCH method:

  <%= config.bin %> <%= command.id %> '/services/data/v56.0/sobjects/account/<Account ID>' --body "{\"BillingCity\": \"San Francisco\"}" --method PATCH

- Store the values for the request header, body, and so on, in a file, which you then specify with the --file flag; see the description of --file for more information:

  <%= config.bin %> <%= command.id %> --file myFile.json

# flags.method.summary

HTTP method for the request.

# flags.file.summary

JSON file that contains values for the request header, body, method, and URL.

# flags.file.description

Use this flag instead of specifying the request details with individual flags, such as --body or --method. This schema defines how to create the JSON file:

{
url: { raw: string } | string;
method: 'GET', 'POST', 'PUT', 'PATCH', 'HEAD', 'DELETE', 'OPTIONS', 'TRACE';
description?: string;
header: string | Array<Record<string, string>>;
body: { mode: 'raw' | 'formdata'; raw: string; formdata: FormData };
}

Salesforce CLI defined this schema to be mimic Postman schemas; both share similar properties. The CLI's schema also supports Postman Collections to reuse and share requests. As a result, you can build an API call using Postman, export and save it to a file, and then use the file as a value to this flag. For information about Postman, see https://learning.postman.com/.

Here's a simple example of a JSON file that contains values for the request URL, method, and body:

{
"url": "sobjects/Account/<Account ID>",
"method": "PATCH",
"body" : {
"mode": "raw",
"raw": {
"BillingCity": "Boise"
}
}
}

See more examples in the plugin-api test directory, including JSON files that use "formdata" to define collections: https://github.com/salesforcecli/plugin-api/tree/main/test/test-files/data-project.

# flags.header.summary

HTTP header in "key:value" format.

# flags.body.summary

File or content for the body of the HTTP request. Specify "-" to read from standard input or "" for an empty body. If passing a file, prefix the filename with '@'. 
