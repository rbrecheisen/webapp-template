import numpy as np


def normalize(img, min_bound, max_bound):
    img = (img - min_bound) / (max_bound - min_bound)
    img[img > 1] = 0
    img[img < 0] = 0
    c = (img - np.min(img))
    d = (np.max(img) - np.min(img))
    img = np.divide(c, d, np.zeros_like(c), where=d != 0)
    return img


def calculate_area(labels, label, pixel_spacing):
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    area = np.sum(mask) * (pixel_spacing[0] * pixel_spacing[1]) / 100.0
    return area


def calculate_smra(image, label, labels):
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    subtracted = image * mask
    smra = np.sum(subtracted) / np.sum(mask)
    return smra


def convert_labels_to_123(ground_truth):
    new_ground_truth = np.copy(ground_truth)
    new_ground_truth[new_ground_truth == 1] = 1
    new_ground_truth[new_ground_truth == 5] = 2
    new_ground_truth[new_ground_truth == 7] = 3
    return new_ground_truth


def calculate_dice_score(ground_truth, prediction, label):
    numerator = prediction[ground_truth == label]
    numerator[numerator != label] = 0
    n = ground_truth[prediction == label]
    n[n != label] = 0
    if np.sum(numerator) != np.sum(n):
        raise RuntimeError('Mismatch in Dice score calculation!')
    denominator = (np.sum(prediction[prediction == label]) + np.sum(ground_truth[ground_truth == label]))
    dice_score = np.sum(numerator) * 2.0 / denominator
    return dice_score
