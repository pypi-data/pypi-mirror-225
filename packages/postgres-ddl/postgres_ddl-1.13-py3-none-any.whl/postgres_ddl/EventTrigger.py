#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.Owner import Owner

class EventTrigger(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Oid = data.get("oid")
        assert (self.Oid or 0) > 0, \
            "Event trigger oid is null"

        self.Name = (data.get("name") or "").strip()
        assert len(self.Name) > 0, \
            "Event trigger name is null"

        self.Status = (data.get("status") or "").strip()
        assert len(self.Status) > 0, \
            "Event trigger status is null"

        self.Event = (data.get("event") or "").strip()
        assert len(self.Event) > 0, \
            "Event trigger event is null"

        self.Function = (data.get("fnc") or "").strip()
        assert len(self.Function) > 0, \
            "Event trigger function is null"

        self.Tags = (data.get("tags") or [])

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.GetFullName(),
                "owner_name"    : data.get("owner")
            }
        )

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "event_trigger"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return self.Name

    def GetTag(self):
        return "EVENT TRIGGER"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def DDL_Create(self):
        r = f"-- Event trigger: {self.GetFullName()}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += f"CREATE {self.GetTag()} {self.GetFullName()}"
        r += Config.NL
        r += f"{Config.Indent}ON {self.Event}"
        r += Config.NL

        if len(self.Tags) > 0:
            tags = ", ".join([f"'{i}'" for i in sorted(self.Tags)])
            r += f"{Config.Indent}WHEN TAG IN ({tags})"
            r += Config.NL

        r += f"{Config.Indent}EXECUTE PROCEDURE {self.Function};"
        r += Config.NL + Config.NL
        r += self.Owner.DDL_Create()
        r += Config.NL + Config.NL
        r += self.DDL_Status()
        return r.strip() + Config.NL

    def DDL_Status(self):
        return f"ALTER {self.GetTag()} {self.GetFullName()} {self.Status};"

    def GetPath(self):
        return ["_event_trigger"]

    def GetFileName(self):
        return f"{self.Name}.sql"

    def Export(self):
        result = {}
        result[self.GetObjectName()] = self
        result[self.Owner.GetObjectName()] = self.Owner
        return result

    def Diff(self, another):
        if (
            self.Event != another.Event or
            self.Function != another.Function or
            self.Tags != another.Tags
        ):
            return [self.DDL_Drop(), self.DDL_Create()]

        if self.Status != another.Status:
            return [self.DDL_Status()]
