# NewEnvironment


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**template** | **str** |  | 

## Example

```python
from e2b.api.client.models.new_environment import NewEnvironment

# TODO update the JSON string below
json = "{}"
# create an instance of NewEnvironment from a JSON string
new_environment_instance = NewEnvironment.from_json(json)
# print the JSON string representation of the object
print NewEnvironment.to_json()

# convert the object into a dict
new_environment_dict = new_environment_instance.to_dict()
# create an instance of NewEnvironment from a dict
new_environment_form_dict = new_environment.from_dict(new_environment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


