
#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class Owner(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Type = (data.get("instance_type") or "").strip().upper()
        assert len(self.Type) > 0, \
            f"Owner instance type is null - {parent}"

        self.Instance = (data.get("instance_name") or "").strip()
        assert len(self.Instance) > 0, \
            f"Owner instance name is null - {parent}"

        self.Owner = (data.get("owner_name") or "").strip()
        assert len(self.Owner) > 0, \
            f"Owner name is null - {parent}"

    def __str__(self):
        return self.GetObjectName()

    def GetObjectType(self):
        return "owner"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.Type}_{self.Instance}"

    def DDL_Create(self):
        return f"ALTER {self.Type} {self.Instance}{Config.NL}{Config.Indent}OWNER TO {self.Owner};"

    def DDL_Drop(self):
        return ""

    def Diff(self, another):
        if self.Owner != another.Owner:
            return [
                self.DDL_Create()
            ]
        else:
            return []
