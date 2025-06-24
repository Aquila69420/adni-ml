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

def register_to_mni(img_path, mni_img):
    """Resample a NIfTI image to the MNI template."""
    img = load_img(img_path)
    registered_img = resample_to_img(img, mni_img, copy_header=True)
    return registered_img

def segment_with_atlas(registered_img, atlas_img, labels):
    """Segment a registered image using an atlas."""
    masker = NiftiLabelsMasker(atlas_img, labels=labels)
    segmented = masker.fit_transform(registered_img)
    return masker, segmented

def compute_roi_volumes(registered_img, atlas_img, labels):
    masker = NiftiLabelsMasker(labels_img=atlas_img, labels=labels, standardize=False)
    # Get binary mask for each ROI
    mask_data = masker.labels_img.get_fdata().astype(int)
    unique = np.unique(mask_data)
    unique = unique[unique != 0]  # omit background

    affine = atlas_img.affine
    # Compute voxel volume = |det(affine[:3,:3])|
    voxel_dims = np.abs(np.linalg.det(affine[:3, :3]))

    volumes = {}
    for lab in unique:
        count = np.sum(mask_data == lab)
        volumes[lab] = count * voxel_dims

    # Map label numbers to names
    name_map = {i+1: nm for i, nm in enumerate(labels)}  # assumes background is index 0
    named_volumes = {name_map.get(l, str(l)): volumes[l] for l in volumes}
    return named_volumes
