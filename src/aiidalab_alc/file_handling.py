"""Module for providing functionality to deal with files."""

from io import BytesIO

from aiida.orm import SinglefileData
from ipywidgets import FileUpload, HBox, Text


class FileUploadWidget(HBox):
    """A widget for uploading files."""

    def __init__(self, description: str = "File: ", **kwargs):
        """
        FileUploadWidget constructor.

        Parameters
        ----------
        **kwargs :
            Keyword arguments passed to the parent class's constructor.
        """
        super().__init__(**kwargs)
        self.file = None

        self.file_upload = FileUpload(
            accept="",
            multiple=False,
            description="Upload",
            layout={"width": "20%"},
        )
        self.file_handle = Text(
            value="",
            placeholder="",
            description=description,
            disabled=True,
            layout={"width": "70%"},
        )
        self.children = [self.file_handle, self.file_upload]

        self.file_upload.observe(self._on_file_upload, names="value")

        return

    def _on_file_upload(self, _):
        """Handle file upload events."""
        if self.file_upload.value:
            self.file = self.file_upload.value[list(self.file_upload.value.keys())[0]]
            self.file_handle.value = self.file["metadata"]["name"]
        else:
            self.file_handle.value = ""
        return

    def get_file_contents(self) -> BytesIO:
        """Get the contents of the uploaded file as a BytesIO object."""
        if self.file is not None:
            return BytesIO(self.file["content"])
        return None

    def filename(self) -> str:
        """Get the name of the uploaded file."""
        if self.file is not None:
            return self.file["metadata"]["name"]
        return ""

    def get_aiida_file_object(self):
        """Get the uploaded file as an AiiDA SinglefileData object."""
        if self.file is not None:
            return SinglefileData(
                file=self.get_file_contents(), filename=self.filename()
            )
        return None
