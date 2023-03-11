from enum import Enum


class UserRole(Enum):
    admin: str = "admin"
    doctor: str = "doctor"
    staff: str = "staff"

    # NOTE: this is for oauth security scope.
    # @classmethod
    # def get_all_scopes(cls) -> dict[str, str]:
    #     return {
    #         cls.admin.value: "This is admin",
    #         cls.doctor.value: "This is doctor",
    #         cls.staff.value: "This is staff",
    #     }
