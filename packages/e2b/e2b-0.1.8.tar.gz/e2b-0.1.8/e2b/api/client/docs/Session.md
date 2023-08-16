# Session


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code_snippet_id** | **str** | Identifier of a code snippet which which is the environment associated | 
**edit_enabled** | **bool** | Information if the session is a shared persistent edit session | 
**session_id** | **str** | Identifier of the session | 
**client_id** | **str** | Identifier of the client | 

## Example

```python
from e2b.api.client.models.session import Session

# TODO update the JSON string below
json = "{}"
# create an instance of Session from a JSON string
session_instance = Session.from_json(json)
# print the JSON string representation of the object
print Session.to_json()

# convert the object into a dict
session_dict = session_instance.to_dict()
# create an instance of Session from a dict
session_form_dict = session.from_dict(session_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


