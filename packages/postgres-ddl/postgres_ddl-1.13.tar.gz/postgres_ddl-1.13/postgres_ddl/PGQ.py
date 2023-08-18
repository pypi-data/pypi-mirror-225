#!/usr/bin/python
# -*- coding: utf-8 -*-

from postgres_ddl.Config import Config
from postgres_ddl.DDL import DDL

class PGQ(DDL):
    def __init__(self, parent, data):
        super().__init__(parent, data)

        self.Name = (data.get("queue_name") or "").strip()
        assert len(self.Name or 0) > 0, \
            "PGQ name is null"

        self.IsPaused = data.get("queue_ticker_paused") is True

        self.MaxCount = data.get("queue_ticker_max_count") or 0
        assert self.MaxCount > 0, \
            "PGQ ticker_max_count is null"

        self.MaxLag = (data.get("queue_ticker_max_lag") or "0").strip()
        assert len(self.MaxLag) > 0, \
            "PGQ ticker_max_lag is null"

        self.IdlePeriod = (data.get("queue_ticker_idle_period") or "0").strip()
        assert len(self.IdlePeriod) > 0, \
            "PGQ ticker_idle_period is null"

        self.Consumers = (data.get("consumers") or [])

    def __str__(self):
        return self.GetFullName()

    def GetObjectType(self):
        return "pgq"

    def GetObjectName(self):
        return f"{self.GetObjectType()}_{self.GetFullName()}"

    def GetFullName(self):
        return self.Name

    def GetTag(self):
        return "PGQ"

    def DDL_Drop(self):
        r = "--SELECT pgq.drop_queue("
        r += Config.NL
        r += f"--{Config.Indent}x_queue_name := '{self.Name}'"
        r += Config.NL
        r += "--);"
        return r.strip()

    def DDL_Create(self):
        r = f"-- PGQ Queue: {self.GetFullName()}"
        r += Config.NL + Config.NL
        r += self.DDL_Drop()
        r += Config.NL + Config.NL
        r += "SELECT pgq.create_queue("
        r += Config.NL
        r += f"{Config.Indent}i_queue_name := '{self.Name}'"
        r += Config.NL
        r += ");"
        r += Config.NL + Config.NL
        r += f"UPDATE pgq.queue SET"
        r += Config.NL
        r += f"{Config.Indent}-- Тикер остановлен"
        r += Config.NL
        r += f"{Config.Indent}queue_ticker_paused = {str(self.IsPaused).upper()},"
        r += Config.NL
        r += f"{Config.Indent}-- Макс. время простоя для тика"
        r += Config.NL
        r += f"{Config.Indent}queue_ticker_idle_period = '{self.IdlePeriod}',"
        r += Config.NL
        r += f"{Config.Indent}-- Макс. кол-во событий для тика"
        r += Config.NL
        r += f"{Config.Indent}queue_ticker_max_count = {self.MaxCount},"
        r += Config.NL
        r += f"{Config.Indent}-- Макс. время с пред. тика"
        r += Config.NL
        r += f"{Config.Indent}queue_ticker_max_lag = '{self.MaxLag}'"
        r += Config.NL
        r += f"WHERE queue_name = '{self.Name}';"
        r += Config.NL + Config.NL

        for cns in sorted(self.Consumers):
            r += "-- SELECT pgq.unregister_consumer("
            r += Config.NL
            r += f"-- {Config.Indent}x_queue_name := '{self.Name}',"
            r += Config.NL
            r += f"-- {Config.Indent}x_consumer_name := '{cns}'"
            r += Config.NL
            r += "-- );"
            r += Config.NL + Config.NL

            r += "SELECT pgq.register_consumer("
            r += Config.NL
            r += f"{Config.Indent}x_queue_name := '{self.Name}',"
            r += Config.NL
            r += f"{Config.Indent}x_consumer_id := '{cns}'"
            r += Config.NL
            r += ");"
            r += Config.NL

        return r.strip() + Config.NL

    def GetPath(self):
        return ["_pgq"]

    def GetFileName(self):
        return f"{self.GetFullName()}.sql"

    def Export(self):
        return { self.GetObjectName() : self }

    def Diff(self, another):
        if self.DDL_Create() != another.DDL_Create():
            return [
                another.DDL_Drop(),
                self.DDL_Create()
            ]

        return []
