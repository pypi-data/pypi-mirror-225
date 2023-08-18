#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config():
    Indent = " " * 2
    NL = chr(10)
    FncParamSign = ":="
    IsSeqGrantsInTable = False

    @staticmethod
    def Parse(json):
        Config.Indent = " " * (json.get("indent") or 2)
        Config.NL = json.get("new_line") or chr(10)
        Config.FncParamSign = json.get("fnc_param_sign") or ":="

        style = json.get("style") or []
        Config.IsSeqGrantsInTable = "seq_grants_in_table" in style
        Config.IsHideUserMappings = "hide_user_mappings" in style
