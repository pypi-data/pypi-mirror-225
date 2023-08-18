#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.Owner import Owner

class Subscription(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Oid = data.get("oid")
        assert (self.Oid or 0) > 0, \
            "Subscription oid is null"

        self.Name = (data.get("name") or "").strip()
        assert len(self.Name) > 0, \
            "Subscription name is null"

        self.IsEnabled = bool(data.get("is_enabled") or False)

        self.Connect = (data.get("connect") or "").strip()
        assert len(self.Connect) > 0, \
            "Subscription connect is null"

        self.Slot = (data.get("slot") or "").strip()
        assert len(self.Slot) > 0, \
            "Subscription slot is null"

        self.SyncCommit = (data.get("sync_commit") or "").strip()
        assert len(self.SyncCommit) > 0, \
            "Subscription sync_commit is null"

        self.Publications = (data.get("publications") or [])
        assert len(self.Publications) > 0, \
            "Subscription publications is null"

        self.Tables = (data.get("tables") or [])

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
        return "subscription"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return self.Name

    def GetTag(self):
        return "SUBSCRIPTION"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def DDL_Create(self):
        r = f"-- Subscription: {self.GetFullName()}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += f"CREATE {self.GetTag()} {self.GetFullName()}"
        r += Config.NL
        r += f"CONNECTION '{self.Connect}'"
        r += Config.NL
        r += f"PUBLICATION {self.GetPublications()}"
        r += Config.NL
        r += "WITH ("
        r += Config.NL
        r += f"{Config.Indent}enabled = {str(self.IsEnabled).upper()},"
        r += Config.NL
        r += f'{Config.Indent}slot_name = "{self.Slot}",'
        r += Config.NL
        r += f"{Config.Indent}synchronous_commit = '{self.SyncCommit}'"
        r += Config.NL
        r += ");"
        r += Config.NL + Config.NL
        r += self.Owner.DDL_Create() + Config.NL

        if len(self.Tables) > 0:
            r += Config.NL
            r += '-- Tables:' + Config.NL
            for t in self.Tables:
                r += f'--   {t}'
                r += Config.NL

        return r.strip() + Config.NL

    def GetPath(self):
        return ["_logical"]

    def GetFileName(self):
        return f"{self.Name}.sql"

    def GetPublications(self):
        return ", ".join(self.Publications)

    def Export(self):
        result = {}
        result[self.GetObjectName()] = self
        result[self.Owner.GetObjectName()] = self.Owner
        return result

    def Diff(self, another):
        result = []

        if self.IsEnabled != another.IsEnabled:
            if self.IsEnabled:
                result.append(f"ALTER {self.GetTag()} {self.GetFullName()} ENABLE;")
            else:
                result.append(f"ALTER {self.GetTag()} {self.GetFullName()} DISABLE;")

        if self.Connect != another.Connect:
            result.append(f"ALTER {self.GetTag()} {self.GetFullName()} CONNECTION '{self.Connect}';")

        if self.Publications != another.Publications:
            result.append(f"ALTER {self.GetTag()} {self.GetFullName()} SET PUBLICATION {self.GetPublications()};")

        if self.Slot != another.Slot:
            result.append(f'ALTER {self.GetTag()} {self.GetFullName()} SET(slot_name = "{self.Slot}");')

        if self.Slot != another.Slot:
            result.append(f"ALTER {self.GetTag()} {self.GetFullName()} SET(synchronous_commit = '{self.SyncCommit}');")

        if len(result) > 0:
            result.append(f"ALTER {self.GetTag()} {self.GetFullName()} REFRESH PUBLICATION;")

        return result
