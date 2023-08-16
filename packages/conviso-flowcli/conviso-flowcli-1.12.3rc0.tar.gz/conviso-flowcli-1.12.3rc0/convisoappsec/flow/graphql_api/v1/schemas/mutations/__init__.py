CREATE_ASSET = """ 
mutation (
  $companyId: Int!, 
  $name: String!, 
  $scanType: AssetScan!
) {
  createAsset(
    input: { 
      companyId: $companyId, 
      name: $name, 
      scanType: $scanType
    }
  ) {
    asset {
      id
      name
      createdAt
    }
    errors
  }
}
"""
