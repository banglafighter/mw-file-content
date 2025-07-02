from dataclasses import dataclass


@dataclass(kw_only=True)
class FindReplaceData:
    find: any
    replace: any
