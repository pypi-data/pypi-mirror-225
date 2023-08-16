GET_ASSETS = """ 
query (
  $id: ID!,
  $page: Int,
  $limit: Int
) {
  assets(
    id: $id
    page: $page
    limit: $limit
  ) {
    collection {
      id
      name
      createdAt
    }
    
    metadata {
      currentPage
      limitValue
      totalCount
      totalPages
    }
  }
}
"""
