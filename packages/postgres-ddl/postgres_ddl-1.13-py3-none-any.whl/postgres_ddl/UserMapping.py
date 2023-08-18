
#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.DDL import DDL
from postgres_ddl.Config import Config
from postgres_ddl.System import ParseOptions

class UserMapping(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Type = (data.get("instance_type") or "").strip().upper()
        assert len(self.Type) > 0, \
            f"UserMapping instance type is null - {parent}"

        self.Instance = (data.get("instance_name") or "").strip()
        assert len(self.Instance) > 0, \
            f"UserMapping instance name is null - {parent}"

        self.Role = (data.get("role") or "").strip().lower()

        self.Options = sorted(data.get("options") or [])

    def __str__(self):
        return self.GetObjectName()

    def GetObjectType(self):
        return "user_mapping"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.Instance}_{self.Role}"

    def GetTag(self):
        return "USER MAPPING"

    def DDL_Create(self):
        return f"CREATE {self.GetTag()} FOR {self.Role} {self.Type} {self.Instance} OPTIONS({self.DDL_Options()});"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS FOR {self.Role} {self.Type} {self.Instance};"

    def DDL_Options(self):
        result = []

        for o in self.Options:
            o = ParseOptions(o, ["password"])
            if o is not None:
                result.append(o)

        return f",{Config.NL}".join(sorted(result))

    def Diff(self, another):
        if self.Options != another.Options:
            return [
                another.DDL_Drop(),
                self.DDL_Create()
            ]
        else:
            return []
