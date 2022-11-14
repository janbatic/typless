# Typless

Setup dnyamob in docker containe 
```shell
sudo docker run -p 7777:8000 -d amazon/dynamodb-local
```
then when container is running, create table
```shell
python dynamodb_migrate.py
```

## APIS's

### Create or update documents
#### Request
> <span style="color:orange;"><strong>[POST]</strong></span> api/documents/

| Parameter     | Type | Description                                   |
|---------------| ------------- |-----------------------------------------------|
| **documents** |list| list of documents with parameters |

|Document parameter|type|description|
|----------|----------|--------|
| **number**    |string| **Required.** number of document.             |
| **type**      |string| Type of document(e.g. "PDF").                 |
| **date**      |date| Document date(format e.g. "2020-06-01")       |

#### Response
 Status code 200, 400
 
### Delete documents
#### Request
> <span style="color:red;"><strong>[DELETE]</strong></span> api/documents/

| Parameter     | Type | Description                                                |
|---------------| ------------- |------------------------------------------------------------|
| **documents** |list| list of documents with parameters that needs to be deleted |

|Document parameter|type|description|
|----------|----------|--------|
| **number**    |string| **Required.** number of document.             |

#### Response
 Status code 200, 400

### Search documents
#### Request
> <span style="color:green;"><strong>[GET]</strong></span> api/documents/

| Parameter            | Type                   | Description                                                                                                                                                                                          |
|----------------------|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **search_type**      | string                 | Parameter to filter documents by "number", "date", "doc_type", "doc_type_and_date".                                                                                                                  |
| **search_data_fun**  |string| When filtering by "date", "number", "doc_type_and_date" add fun you want to filter by possibilities "eq"(data=string), "lte"(data=string), "gte"(data=string), "between"(data=list), "in"(data=list) |
 | **search_data**      | string/list of strings | Data you are filtering by. For type both(by string or list of strings) are possible|
| **search_data_type** |string| Only required when search_type equals to doc_type_and_date and this param filters by doc type|

#### Response
Example

```json
{
    "documents": [
        {
            "number": "2",
            "date": "2020-06-10",
            "type": "PDF"
        }
    ]
}
```
