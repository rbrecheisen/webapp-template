import os
import pydicom
import numpy as np

from django import forms
from barbell2light.dicom import is_dicom_file, tag2numpy

from ..basetask import Task
from ...models import FilePathModel, DataSetModel


class Numpy2DcmTask(Task):

    @staticmethod
    def apply_ct_window(pixels, window):
        result = (pixels - window[1] + 0.5 * window[0])/window[0]
        result[result < 0] = 0
        result[result > 1] = 1
        return result

    @staticmethod
    def get_color_map():
        color_map = []
        for i in range(256):
            if i == 1:
                color_map.append([255, 0, 0])
            elif i == 5:
                color_map.append([0, 255, 0])
            elif i == 7:
                color_map.append([0, 0, 255])
            else:
                color_map.append([0, 0, 0])
        return color_map

    def execute_base(self, task_model):
        # https://medium.com/analytics-vidhya/how-to-convert-grayscale-dicom-file-to-rgb-dicom-file-with-python-df86ac055bd
        # https://stackoverflow.com/questions/65439230/convert-grayscale-2d-numpy-array-to-rgb-image
        dataset = task_model.dataset
        files = FilePathModel.objects.filter(dataset=dataset).all()
        output_dataset = self.create_output_dataset_model(task_model)
        for f in files:
            if is_dicom_file(f.path):
                p = pydicom.dcmread(f.path)
                pixels = p.pixel_array
                pixels = pixels.astype(float)
                pixels = pixels * p.RescaleSlope + pixels * p.RescaleIntercept
                pixels = self.apply_ct_window(pixels, [400, 50])
                converter = tag2numpy.Tag2NumPy(pixels.shape)
                converter.set_input_tag_file_path(os.path.splitext(f.path)[0] + '.tag')
                converter.execute()
                tag_pixels = converter.get_output_numpy_array()
                new_pixels = np.zeros((*tag_pixels.shape, 3), dtype=np.uint8)
                np.take(self.get_color_map(), tag_pixels, axis=0, out=new_pixels)
                p.PhotometricInterpretation = 'RGB'
                p.SamplesPerPixel = 3
                p.BitsAllocated = 8
                p.BitsStored = 8
                p.HighBit = 7
                p.add_new(0x00280006, 'US', 0)
                p.is_little_endian = True
                p.fix_meta_info()
                p.PixelData = new_pixels.tobytes()
                output_file = os.path.splitext(f.path)[0] + '.tag.dcm'
                p.save_as(output_file)
                self.create_output_file_model(output_file, output_dataset)


class Numpy2DcmTaskForm(forms.Form):
    pass
