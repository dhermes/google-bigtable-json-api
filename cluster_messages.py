from protorpc import messages


class ListZonesRequest(messages.Message):
    pass


class ListZonesResponse(messages.Message):
    pass


class GetClusterRequest(messages.Message):
    pass


class ListClustersRequest(messages.Message):
    pass


class ListClustersResponse(messages.Message):
    pass


class CreateClusterRequest(messages.Message):
    pass


class CreateClusterMetadata(messages.Message):
    pass


class UpdateClusterMetadata(messages.Message):
    pass


class DeleteClusterRequest(messages.Message):
    pass


class UndeleteClusterRequest(messages.Message):
    pass


class UndeleteClusterMetadata(messages.Message):
    pass
