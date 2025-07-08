import os
import numpy as np
from nilearn.maskers import NiftiLabelsMasker
from nilearn.image import load_img, resample_to_img
from nilearn.datasets import fetch_atlas_aal

def find_nifti_files(n3_dir):
    """Find all NIfTI files in subsubdirectories under n3_dir."""
    subdirs = [os.path.join(n3_dir, d) for d in os.listdir(n3_dir) if os.path.isdir(os.path.join(n3_dir, d))]
    subsubdirs = []
    for subdir in subdirs:
        subsubdirs.extend([os.path.join(subdir, d) for d in os.listdir(subdir) if os.path.isdir(os.path.join(subdir, d))])
    files = []
    for subsubdir in subsubdirs:
        files.extend([os.path.join(subsubdir, f) for f in os.listdir(subsubdir) if f.endswith('.nii')])
    return files

def register_image_to_template(img_path, mni_img):
    """Resample a NIfTI image to the MNI template."""
    img = load_img(img_path)
    registered_img = resample_to_img(img, mni_img, copy_header=True)
    return registered_img

def segment_with_atlas(registered_img, atlas_img, labels):
    """Segment a registered image using an atlas."""
    masker = NiftiLabelsMasker(atlas_img, labels=labels)
    segmented = masker.fit_transform(registered_img)
    return masker, segmented

def compute_suvr(registered_img, atlas_img):
    masker = NiftiLabelsMasker(labels_img=atlas_img, standardize=True, strategy='sum')
    masked_image = masker.fit_transform(registered_img)
    global_suv = np.sum(masked_image)
    suvrs = {region: region/global_suv for region in masked_image}
    return suvrs