from PyQt5 import QtCore
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager

class ConsoleWidget(RichJupyterWidget):
    """Rich python interpreter console thing."""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Create an in-process kernel
        kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel(show_banner=False)

        # Set the kernel data
        self.kernel = kernel_manager.kernel
        self.kernel.gui = 'qt'

        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        self.kernel_manager = kernel_manager
        self.kernel_client = kernel_client


    def sizeHint(self):
        """Overloading this so it doesn't appear huge in the qdockwidget."""
        return QtCore.QSize(300, 75)
