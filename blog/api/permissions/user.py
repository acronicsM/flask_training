from combojsonapi.permission import PermissionMixin, PermissionForGet, PermissionUser, PermissionForPatch
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user
from blog.models.user import User


class UserPermission(PermissionMixin):
    ALL_AVAILABLE_FIELDS = [
        "id",
        "email",
    ]
    PATCH_AVAILABLE_FIELDS = [
        "email",
    ]

    def get(self, *args, many=True, user_permission: PermissionUser = None, **kwargs) -> PermissionForGet:
        if not current_user.is_authenticated:
            raise AccessDenied("no access")

        self.permission_for_get.allow_columns = (self.ALL_AVAILABLE_FIELDS, 10)
        return self.permission_for_get

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:
        self.permission_for_patch.allow_columns = (self.PATCH_AVAILABLE_FIELDS, 10)

        return self.permission_for_patch

    def patch_data(self, *args, data: dict = None, obj: User = None, user_permission: PermissionUser = None, **kwargs):
        permission_for_patch = user_permission.permission_for_patch_permission(model=User)

        return {k: v for k, v in data.items() if k in permission_for_patch.columns}
