import os
import pandas as pd
from django.conf import settings

class Meta:
    """A Sigleton class keeps data
    """

    __instance = None
    __inited = False
    path: str = os.path.join(settings.STATICFILES_DIRS[0], "files", "AKBNK.E.csv")
    df_lob: pd.DataFrame

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if type(self).__inited:
            return
        type(self).__inited = True

        
