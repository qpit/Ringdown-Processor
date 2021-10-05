from PyQt5.QtWidgets import QSpacerItem,QSizePolicy

class Spacer(QSpacerItem):
    def __init__(self,*args,axis='both',**kwargs):
        hPolicy = QSizePolicy.Fixed
        vPolicy = QSizePolicy.Fixed
        if axis.lower().strip() == 'h':
            hPolicy = QSizePolicy.Expanding
        elif axis.lower().strip() == 'v':
            vPolicy = QSizePolicy.Expanding
        elif axis.lower().strip() == 'both':
            hPolicy = QSizePolicy.Expanding
            vPolicy = QSizePolicy.Expanding

        super().__init__(1,1,hPolicy=hPolicy,vPolicy=vPolicy)