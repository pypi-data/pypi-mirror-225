#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL
from postgres_ddl.System import SEP

RE_NEWLINE = re.compile("[\r\n]{1,}", re.MULTILINE|re.IGNORECASE)

class Comment(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Type = (data.get("instance_type") or "").strip().upper()
        assert len(self.Type) > 0, \
            f"Comment instance type is null - {parent}"

        self.Instance = (data.get("instance_name") or "").strip()
        assert len(self.Instance) > 0, \
            f"Comment instance name is null - {parent}"

        self.Comment = re.sub(RE_NEWLINE, SEP, (data.get("comment") or "").strip())

        self.IsExists = len(self.Comment) > 0

    def __str__(self):
        return self.GetObjectName()

    def GetObjectType(self):
        return "comment"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.Type}_{self.Instance}"

    def DDL_Create(self):
        return f"COMMENT ON {self.Type} {self.Instance}{Config.NL}{Config.Indent}IS '{self.Comment}';"

    def DDL_Drop(self):
        return f"COMMENT ON {self.Type} {self.Instance} IS '';"

    def Diff(self, another):
        if self.Comment != another.Comment:
            return [
                self.DDL_Create()
            ]
        else:
            return []
