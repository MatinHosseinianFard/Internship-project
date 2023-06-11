from rest_framework.permissions import IsAuthenticated


class IsBenefactor(IsAuthenticated):
    pass


class IsCharityOwner(IsAuthenticated):
    pass