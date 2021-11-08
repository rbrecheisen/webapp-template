import pydicom
import pydicom.errors


class DicomChecker:

    def __init__(self, files):
        self.files = files
        self.required_tags = []
        self.required_dimensions = [512, 512]

    def set_required_tags(self, required_tags):
        self.required_tags = required_tags

    def set_required_dimensions(self, rows, columns):
        self.required_dimensions = [rows, columns]

    def execute(self):
        errors = []
        for f in self.files:
            try:
                p = pydicom.dcmread(f.path, stop_before_pixels=True)
            except pydicom.errors.InvalidDicomError:
                errors.append('{}: invalid DICOM'.format(f.path))
                continue
            for tag in self.required_tags:
                if tag not in p:
                    errors.append('{}: missing tag "{}"'.format(f.path, tag))
                    continue
            if p.Rows != self.required_dimensions[0] and p.Columns != self.required_dimensions[1]:
                errors.append('{}: wrong dimensions ({})'.format(f.path, [p.Rows, p.Columns]))
                continue
        return errors
