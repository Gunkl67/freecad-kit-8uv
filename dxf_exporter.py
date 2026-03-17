import FreeCAD
try:
    import FreeCADGui
except ImportError:
    pass  # GUI not available in headless mode
import Part
import Draft
import os

class DXFExporter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = FreeCAD.ActiveDocument

    def export(self):
        # Check if the document is active
        if not self.doc:
            raise RuntimeError("No active FreeCAD document to export.")
        
        # Check file extension
        if not self.file_path.lower().endswith('.dxf'):
            raise ValueError("File must have a .dxf extension.")
        
        # Create a temp file for the export
        temp_file = self.create_temp_file()

        try:
            # Filter objects that can be exported to DXF
            exportable_objects = [obj for obj in self.doc.Objects 
                                if hasattr(obj, 'Shape') or 
                                obj.TypeId.startswith('Draft::') or
                                obj.TypeId.startswith('Part::')]
            
            if not exportable_objects:
                raise RuntimeError("No exportable objects found in document")
            
            # Use Draft module to export to DXF
            Draft.export(exportable_objects, temp_file, 'dxf')
            
            # Check if export was successful
            if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
                raise RuntimeError("Export failed - no output file created or file is empty")
            
            # Rename temp file to final file
            os.rename(temp_file, self.file_path)
            print(f"Successfully exported to {self.file_path}")
        except Exception as e:
            # Clean up temp file on error, but only if it exists
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise RuntimeError(f"Failed to export to DXF: {str(e)}")

    def create_temp_file(self):
        # Create a temporary file path in the same directory
        temp_file_path = f"{os.path.splitext(self.file_path)[0]}_temp.dxf"
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)  # Remove if it exists to prevent conflicts
        return temp_file_path

# Usage example (this part would be in main.py, but included for clarity):
if __name__ == "__main__":
    try:
        exporter = DXFExporter("output_file.dxf")
        exporter.export()
    except Exception as e:
        print(f"Error: {e}")

# TODO: Add support for exporting specific object types or layers.
# TODO: Implement a GUI dialog for file selection and options.
# Limitations: Only exports visible objects in the active document.
