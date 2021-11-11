import os
import json
import zipfile
import pydicom
import matplotlib.pyplot as plt

from django import forms

from ..basetask import Task, TaskExecutionError
from ...models import FilePathModel, DataSetModel
from ..checkdicomfile.dicom_checker import DicomChecker
from .utils import *

from barbell2light.dicom import get_pixels


class PredictBodyCompositionScoresTask(Task):

    model_dir = '/tmp/webapp-template/tensorflow'

    def load_model(self, zip_file_path):
        import tensorflow as tf
        with zipfile.ZipFile(zip_file_path) as zip_obj:
            zip_obj.extractall(path=self.model_dir)
        return tf.keras.models.load_model(self.model_dir)

    def load_contour_model(self, zip_file_path):
        import tensorflow as tf
        with zipfile.ZipFile(zip_file_path) as zip_obj:
            zip_obj.extractall(path=self.model_dir)
        return tf.keras.models.load_model(self.model_dir)

    @staticmethod
    def load_params(file_path):
        with open(file_path) as f:
            return json.load(f)

    def load_tensorflow_models(self, dataset):
        files = FilePathModel.objects.filter(dataset=dataset).all()
        model, contour_model, params = None, None, None
        for f in files:
            file_name = os.path.split(f.path)[1]
            if file_name == 'model.zip':
                model = self.load_model(f.path)
            elif file_name == 'contour_model.zip':
                contour_model = self.load_contour_model(f.path)
            elif file_name == 'params.json':
                params = self.load_params(f.path)
            else:
                raise TaskExecutionError('Not a TensorFlow model file {}'.format(f.path))
        assert model and params
        return model, contour_model, params

    @staticmethod
    def predict_contour(contour_model, src_img, params):
        ct = np.copy(src_img)
        ct = normalize(
            ct, params['min_bound_contour'], params['max_bound_contour'])
        img2 = np.expand_dims(ct, 0)
        img2 = np.expand_dims(img2, -1)
        pred = contour_model.predict([img2])
        pred_squeeze = np.squeeze(pred)
        pred_max = pred_squeeze.argmax(axis=-1)
        mask = np.uint8(pred_max)
        return mask

    @staticmethod
    def create_png(f):
        image_file_path = f.path
        image_file_dir = os.path.split(image_file_path)[0]
        image_id = os.path.splitext(os.path.split(image_file_path)[1])[0]
        prediction_file_name = '{}_pred.npy'.format(image_id)
        prediction_file_path = os.path.join(image_file_dir, prediction_file_name)
        if not os.path.isfile(prediction_file_path):
            return None
        prediction = np.load(prediction_file_path)
        image = pydicom.read_file(image_file_path)
        image = get_pixels(image, normalize=True)
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(1, 2, 1)
        plt.imshow(image, cmap='gray')
        ax.axis('off')
        ax = fig.add_subplot(1, 2, 2)
        plt.imshow(prediction, cmap='viridis')
        ax.axis('off')
        png_file_name = '{}.png'.format(image_id)
        png_file_path = os.path.join(image_file_dir, png_file_name)
        plt.savefig(png_file_path, bbox_inches='tight')
        plt.close('all')
        return png_file_name, png_file_path

    def execute_base(self, task_model):

        errors = []
        tensorflow_models_dataset = DataSetModel.objects.get(pk=task_model.parameters['tensorflow_models_dataset_id'])
        try:
            model, contour_model, params = self.load_tensorflow_models(tensorflow_models_dataset)
        except TaskExecutionError as e:
            errors.append('Error loading TensorFlow models')
            task_model.errors = errors
            task_model.job_status = 'failed'
            task_model.save()
            return
        dataset = task_model.dataset
        files = FilePathModel.objects.filter(dataset=dataset).all()
        dicom_checker = DicomChecker(files)
        dicom_checker.set_required_tags(['PixelSpacing, Rows, Columns'])
        dicom_checker.set_required_dimensions(512, 512)
        errors = dicom_checker.execute()
        if len(errors) > 0:
            task_model.errors = errors
            task_model.job_status = 'failed'
            task_model.save()
            return
        output_dataset = self.create_output_dataset_model(task_model)
        for f in files:
            try:
                p = pydicom.dcmread(f.path)
                img1 = get_pixels(p, normalize=True)
                if contour_model:
                    mask = self.predict_contour(contour_model, img1, params)
                    img1 = normalize(img1, params['min_bound'], params['max_bound'])
                    img1 = img1 * mask
                else:
                    img1 = normalize(img1, params['min_bound'], params['max_bound'])
                img1 = img1.astype(np.float32)
                img2 = np.expand_dims(img1, 0)
                img2 = np.expand_dims(img2, -1)
                pred = model.predict([img2])
                pred_squeeze = np.squeeze(pred)
                pred_max = pred_squeeze.argmax(axis=-1)
                pred_file_name = os.path.split(f.path)[1]
                pred_file_name = os.path.splitext(pred_file_name)[0] + '_pred.npy'
                pred_file_path = os.path.join(os.path.split(f.path)[0], pred_file_name)
                np.save(pred_file_path, pred_max)
                self.create_output_file_model(pred_file_path, output_dataset)
            except TaskExecutionError as e:
                errors.append('{}: general error ({})'.format(f.path, e))

            _, png_file_path = self.create_png(f)
            self.create_output_file_model(png_file_path, output_dataset)


class PredictBodyCompositionScoresTaskForm(forms.Form):
    pass
