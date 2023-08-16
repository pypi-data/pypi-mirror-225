# EnvironmentStateUpdate


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**state** | [**EnvironmentState**](EnvironmentState.md) |  | 

## Example

```python
from e2b.api.client.models.environment_state_update import EnvironmentStateUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of EnvironmentStateUpdate from a JSON string
environment_state_update_instance = EnvironmentStateUpdate.from_json(json)
# print the JSON string representation of the object
print EnvironmentStateUpdate.to_json()

# convert the object into a dict
environment_state_update_dict = environment_state_update_instance.to_dict()
# create an instance of EnvironmentStateUpdate from a dict
environment_state_update_form_dict = environment_state_update.from_dict(environment_state_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


