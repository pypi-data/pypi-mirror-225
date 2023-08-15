from threemystic_cloud_data_client.cloud_providers.azure.client.actions.base_class.base import cloud_data_client_azure_client_action_base as base
import asyncio
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


class cloud_data_client_azure_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="vmss", 
      logger_name= "cloud_data_client_azure_client_action_vmss",  
      *args, **kwargs)
  
  
    
  async def __process_get_resources_vmss(self, account, *args, **kwargs):
    resource_client = ResourceManagementClient(credential= self.get_cloud_client().get_tenant_credential(tenant= self.get_cloud_client().get_tenant_id(tenant= account, is_account= True)), subscription_id= self.get_cloud_client().get_account_id(account= account))
    try:
      return { self.get_cloud_client().get_resource_id(resource= resource): resource for resource in self.get_cloud_client().sdk_request(
          tenant= self.get_cloud_client().get_tenant_id(tenant= account, is_account= True), 
          lambda_sdk_command=lambda: resource_client.resources.list(filter="resourceType eq 'Microsoft.Compute/virtualMachineScaleSets'", expand="createdTime,changedTime,provisioningState")
        )
      }
    except:
      return []
        
  async def _process_account_data(self, account, loop, *args, **kwargs):
    client = ComputeManagementClient(credential= self.get_cloud_client().get_tenant_credential(tenant= self.get_cloud_client().get_tenant_id(tenant= account, is_account= True)), subscription_id= self.get_cloud_client().get_account_id(account= account))
    tasks = {
      "resource": loop.create_task(self.__process_get_resources_vmss(account= account))
    }

    await asyncio.wait(tasks.values())

    return {
      "account": account,
      "data": [ self.get_common().helper_type().dictionary().merge_dictionary([
          {},
          await self.get_base_return_data(
            account= self.get_cloud_client().serialize_resource(resource= account),
            resource_id= self.get_cloud_client().get_resource_id(resource= item),
            resource= item,
            region= self.get_cloud_client().get_resource_location(resource= item),
            resource_groups= [self.get_cloud_client().get_resource_group_from_resource(resource= item)],
          ),
          {
            "extra_resource": self.get_cloud_client().serialize_resource(tasks["resource"].result().get(self.get_cloud_client().get_resource_id(resource= item))),
            "extra_vmss_vms": [ self.get_cloud_client().serialize_resource(vm) for vm in client.virtual_machine_scale_set_vms.list(resource_group_name= self.get_cloud_client().get_resource_group_from_resource(item), virtual_machine_scale_set_name= item.name) ]
          },
          ]) for item in self.get_cloud_client().sdk_request(
          tenant= self.get_cloud_client().get_tenant_id(tenant= account, is_account= True), 
          lambda_sdk_command=lambda: client.virtual_machine_scale_sets.list_all()
        )
      ]
    }