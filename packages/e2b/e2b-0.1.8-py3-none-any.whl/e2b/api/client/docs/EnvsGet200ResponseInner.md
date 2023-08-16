# EnvsGet200ResponseInner


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**template** | **str** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from e2b.api.client.models.envs_get200_response_inner import EnvsGet200ResponseInner

# TODO update the JSON string below
json = "{}"
# create an instance of EnvsGet200ResponseInner from a JSON string
envs_get200_response_inner_instance = EnvsGet200ResponseInner.from_json(json)
# print the JSON string representation of the object
print EnvsGet200ResponseInner.to_json()

# convert the object into a dict
envs_get200_response_inner_dict = envs_get200_response_inner_instance.to_dict()
# create an instance of EnvsGet200ResponseInner from a dict
envs_get200_response_inner_form_dict = envs_get200_response_inner.from_dict(envs_get200_response_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


