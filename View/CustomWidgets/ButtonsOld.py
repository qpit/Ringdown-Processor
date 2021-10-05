from PyQt5.QtWidgets import QPushButton


class AddButton(QPushButton):
    """
    '+' button
    """
    label = '+'
    def __init__(self,*args,**kwargs):
        super().__init__(self.label,*args,**kwargs)
        self.resize(5, 5)


class DeleteButton(AddButton):
    """
    'X' button
    """
    label = 'X'
