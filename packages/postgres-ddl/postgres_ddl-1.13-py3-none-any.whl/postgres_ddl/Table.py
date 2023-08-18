#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Comment import Comment
from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.Grant import Grant
from postgres_ddl.Owner import Owner
from postgres_ddl.System import ParseACL
from postgres_ddl.TableColumn import TableColumn
from postgres_ddl.TableConstraint import TableConstraint
from postgres_ddl.TableIndex import TableIndex
from postgres_ddl.TablePolicy import TablePolicy
from postgres_ddl.TableSequence import TableSequence
from postgres_ddl.TableSettings import TableSettings
from postgres_ddl.TableTrigger import TableTrigger
from postgres_ddl.TSDB_HyperTable import TSDB_HyperTable

class Table(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Oid = (data.get("oid") or 0)
        assert self.Oid > 0, \
            "Table oid is null"

        self.Schema = (data.get("schema") or "").strip()
        assert len(self.Schema) > 0, \
            "Table schema is null"

        self.Name = (data.get("name") or "").strip()
        assert len(self.Name) > 0, \
            "Table name is null"

        self.Settings = []
        for o in (data.get("reloptions") or []):
            self.Settings.append(TableSettings(self.GetObjectName(), {
                "schema"    : self.Schema,
                "table"     : self.Name,
                "setting"   : o
            }))

        self.HasOids = (data.get("has_oids") or "").strip()
        assert len(self.HasOids) > 0, \
            "Table has oids is null"

        self.HasOids = f"OIDS={str(self.HasOids).upper()}"
        self.Settings.append(TableSettings(self.GetObjectName(), {
            "schema"    : self.Schema,
            "table"     : self.Name,
            "setting"   : self.HasOids
        }))

        self.Inherits = (data.get("parent_table") or "").strip()

        self.Inherits = data.get("parent_table")
        if self.Inherits is not None and self.Inherits != "":
            self.Inherits = self.Inherits.strip()
        else:
            self.Inherits = None

        self.PartKey = data.get("part_key")
        if self.PartKey is not None and self.PartKey != "":
            self.PartKey = self.PartKey.strip()
        else:
            self.PartKey = None

        self.PartBorder = data.get("part_border")

        self.Owner = Owner(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.GetFullName(),
                "owner_name"    : data.get("owner")
            }
        )

        self.Comment = Comment(
            self.GetObjectName(),
            {
                "instance_type" : self.GetTag(),
                "instance_name" : self.GetFullName(),
                "comment"       : data.get("comment")
            }
        )

        self.Grants = []
        for grant in ParseACL(data.get("acl"), self.Owner.Owner):
            grant["instance_type"] = self.GetTag()
            grant["instance_name"] = self.GetFullName()
            self.Grants.append(Grant(self.GetObjectName(), grant))

        self.Columns = []
        for column in (data.get("columns") or []):
            column["schema"] = self.Schema
            column["table"] = self.Name
            column = TableColumn(self.GetObjectName(), column)
            self.Columns.append(column)

        self.Constraints = []
        for cons in (data.get("constraints") or []):
            cons["schema"] = self.Schema
            cons["table"] = self.Name
            cons = TableConstraint(self.GetObjectName(), cons)
            self.Constraints.append(cons)

        self.Indexes = []
        for idx in (data.get("indexes") or []):
            idx["schema"] = self.Schema
            idx["table"] = self.Name
            idx = TableIndex(self.GetObjectName(), idx)
            self.Indexes.append(idx)

        self.Triggers = []
        for trg in (data.get("triggers") or []):
            trg["schema"] = self.Schema
            trg["table"] = self.Name
            trg = TableTrigger(self.GetObjectName(), trg)
            self.Triggers.append(trg)

        self.Sequence = None
        if data.get("sequence") is not None:
            self.Sequence = TableSequence(self.GetFullName(), data.get("sequence") or [])

        self.Policies = []
        for plc in (data.get("policies") or []):
            plc["schema"] = self.Schema
            plc["table"] = self.Name
            plc = TablePolicy(self.GetObjectName(), plc)
            self.Policies.append(plc)

        self.TSDB_HyperTable = None
        if data.get("tsdb_hypertable") is not None:
            self.TSDB_HyperTable = TSDB_HyperTable(self.GetFullName(), data.get("tsdb_hypertable") or [])

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "table"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return f"{self.Schema}.{self.Name}"

    def GetTag(self):
        return "TABLE"

    def DDL_Drop(self):
        return f"DROP {self.GetTag()} IF EXISTS {self.GetFullName()};"

    def DDL_Settings(self):
        r = []

        for sts in sorted(self.Settings, key=lambda x: x.GetFullName()):
            r.append(sts.DDL_Inner())

        return (f",{Config.NL}").join(r)

    def DDL_Create(self):
        is_last_comma = len(self.Constraints) > 0

        r = f"-- Table: {self.GetFullName()}"
        r += Config.NL + Config.NL
        r += f"-- {self.DDL_Drop()}"
        r += Config.NL + Config.NL
        r += f"CREATE {self.GetTag()} {self.GetFullName()}("
        r += Config.NL

        for col in sorted(self.Columns, key=lambda x: x.OrderNum):
            r += col.DDL_Inner(add_comma=is_last_comma, add_comment=True)
            r += Config.NL

        self.Constraints = sorted(self.Constraints, key=lambda x: x.SortKey)
        if len(self.Constraints) > 0:
            cns = [c.DDL_Inner() for c in self.Constraints]
            cns_NL = f",{Config.NL}"
            r += cns_NL.join(cns)
            r += Config.NL

        r += ")"
        r += Config.NL

        if self.PartKey is not None:
            r += f"PARTITION BY {self.PartKey}"
            r += Config.NL

        if self.Inherits is not None:
            if self.PartBorder is not None:
                r += f"PARTITION OF {self.Inherits}"
                r += Config.NL
            else:
                r += f"INHERITS ( {self.Inherits} )"
                r += Config.NL

        if self.PartBorder is not None:
            r += self.PartBorder
            r += Config.NL

        r += "WITH ("
        r += Config.NL
        r += self.DDL_Settings()
        r += Config.NL
        r += ");"
        r += Config.NL + Config.NL
        r += self.Owner.DDL_Create()
        r += Config.NL

        if len(self.Grants) > 0:
            r += Config.NL
            for grant in self.Grants:
                r += grant.DDL_Create()
                r += Config.NL
        r += Config.NL

        if self.Comment.IsExists:
            r += self.Comment.DDL_Create()
            r += Config.NL + Config.NL

        for col in self.Columns:
            cmt = col.DDL_Comment()
            if cmt is not None:
                r += col.DDL_Comment()
                r += Config.NL
        r += Config.NL

        if Config.IsSeqGrantsInTable and self.Sequence is not None:
            r += self.Sequence.DDL_Create()
            r += Config.NL

        for ind in sorted(self.Indexes, key=lambda x: x.GetFullName()):
            r += ind.DDL_Create(f"{Config.NL}{Config.Indent}")
            r += Config.NL + Config.NL

        for trg in sorted(self.Triggers, key=lambda x: x.GetFullName()):
            r += trg.DDL_Create()
            r += Config.NL + Config.NL

        for plc in sorted(self.Policies, key=lambda x: x.GetFullName()):
            r += plc.DDL_Create()
            r += Config.NL + Config.NL

        if self.TSDB_HyperTable is not None:
            r += self.TSDB_HyperTable.DDL_Create()
            r += Config.NL

        return r.strip() + Config.NL

    def GetPath(self):
        return [self.Schema, "table"]

    def GetFileName(self):
        return f"{self.Name}.sql"

    def Export(self):
        result = {}
        result[self.GetObjectName()] = self
        result[self.Comment.GetObjectName()] = self.Comment
        result[self.Owner.GetObjectName()] = self.Owner
        for v in self.Grants:
            result[v.GetObjectName()] = v
        for v in self.Columns:
            result[v.GetObjectName()] = v
        for v in self.Settings:
            result[v.GetObjectName()] = v
        for v in self.Constraints:
            result[v.GetObjectName()] = v
        for v in self.Indexes:
            result[v.GetObjectName()] = v
        for v in self.Triggers:
            result[v.GetObjectName()] = v
        for v in self.Policies:
            result[v.GetObjectName()] = v
        return result
