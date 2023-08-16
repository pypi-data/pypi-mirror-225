# SessionsGet200ResponseInner


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code_snippet_id** | **str** | Identifier of a code snippet which which is the environment associated | 
**edit_enabled** | **bool** | Information if the session is a shared persistent edit session | 
**session_id** | **str** | Identifier of the session | 
**client_id** | **str** | Identifier of the client | 

## Example

```python
from e2b.api.client.models.sessions_get200_response_inner import SessionsGet200ResponseInner

# TODO update the JSON string below
json = "{}"
# create an instance of SessionsGet200ResponseInner from a JSON string
sessions_get200_response_inner_instance = SessionsGet200ResponseInner.from_json(json)
# print the JSON string representation of the object
print SessionsGet200ResponseInner.to_json()

# convert the object into a dict
sessions_get200_response_inner_dict = sessions_get200_response_inner_instance.to_dict()
# create an instance of SessionsGet200ResponseInner from a dict
sessions_get200_response_inner_form_dict = sessions_get200_response_inner.from_dict(sessions_get200_response_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


