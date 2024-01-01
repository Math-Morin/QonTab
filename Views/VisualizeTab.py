from PyQt5.QtWidgets import QWidget, QLineEdit, QFormLayout


class VisualizeTab(QWidget):
    def __init__(self, parent):
        super(VisualizeTab, self).__init__(parent)
        visualizeTabLayout = QFormLayout()
        self.setLayout(visualizeTabLayout)

        # Visualize tab : Groups
        visualizeTabLayout.addRow('First Name:', QLineEdit(self))
        visualizeTabLayout.addRow('Last Name:', QLineEdit(self))
