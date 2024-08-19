from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

# 특정 그룹만 뷰에 접근할 수 있는 권한을 주는 커스텀 믹스인
class GroupRequiredMixin(UserPassesTestMixin):
    group_name = None

    def test_func(self):
        if self.group_name:
            return self.request.user.groups.filter(name=self.group_name).exists()
        return False

    def handle_no_permission(self):
        raise PermissionDenied("이 작업을 수행할 권한이 없습니다.")