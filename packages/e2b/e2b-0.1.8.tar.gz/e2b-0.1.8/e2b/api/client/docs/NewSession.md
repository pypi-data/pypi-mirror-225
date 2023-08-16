# NewSession


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**edit_enabled** | **bool** | Option determining if the session is a shared persistent edit session | [optional] [default to False]
**code_snippet_id** | **str** | Identifier of a code snippet which which is the environment associated | 

## Example

```python
from e2b.api.client.models.new_session import NewSession

# TODO update the JSON string below
json = "{}"
# create an instance of NewSession from a JSON string
new_session_instance = NewSession.from_json(json)
# print the JSON string representation of the object
print NewSession.to_json()

# convert the object into a dict
new_session_dict = new_session_instance.to_dict()
# create an instance of NewSession from a dict
new_session_form_dict = new_session.from_dict(new_session_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


