import FreeCAD
import FreeCADGui
import Import
import os

class DXFImporter:
    def __init__(self, file_path):
        self.file_path = file_path

    def import_dxf(self):
        """Imports a DXF file into FreeCAD."""
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        try:
            # Create a new document if none exists
            if FreeCAD.ActiveDocument is None:
                FreeCAD.newDocument()
            
            # Use FreeCAD's import functionality for DXF files
            Import.insert(self.file_path)
            
            # Check if document exists before recomputing
            if FreeCAD.ActiveDocument:
                FreeCAD.ActiveDocument.recompute()
            
            print(f"Successfully imported: {self.file_path}")
        except Exception as e:
            print(f"An error occurred while importing the DXF file: {str(e)}")

if __name__ == "__main__":
    # Example usage: Modify the file path as needed
    dxf_file = "path/to/your/file.dxf"
    importer = DXFImporter(dxf_file)
    try:
        importer.import_dxf()
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except Exception as generic_error:
        print(f"An unexpected error occurred: {generic_error}")

# TODO: Add support for importing specific layers or entities from the DXF file.
# TODO: Implement a more detailed logging mechanism to track import success/failure.
