param aksName string = 'agenticAksCluster'
param location string = resourceGroup().location
param agentCount int = 3

resource aks 'Microsoft.ContainerService/managedClusters@2023-01-01' = {
  name: aksName
  location: location
  properties: {
    dnsPrefix: '${aksName}-dns'
    agentPoolProfiles: [
      {
        name: 'agentpool'
        count: agentCount
        vmSize: 'Standard_DS2_v2'
        osType: 'Linux'
        type: 'VirtualMachineScaleSets'
        mode: 'System'
      }
    ]
    identity: {
      type: 'SystemAssigned'
    }
  }
}