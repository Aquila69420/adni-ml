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
    registered_img = resample_to_img(img, mni_img)
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
    suvrs = {masker.region_names_[region_id]: region_value/global_suv for region_id, region_value in zip(masker.region_names_, masked_image)}
    return suvrs


def compute_roi_volumes(registered_img, atlas_img):
    cerebellum_region_ids = [95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]
    masker = NiftiLabelsMasker(labels_img=atlas_img, standardize=True, strategy='sum')
    masked_image = masker.fit_transform(registered_img)
    # Compute the volumes of each region in the masked image
    affine = masker.labels_img_.affine
    voxel_volume = abs(np.linalg.det(affine[:3, :3]))  # mm³ per voxel

    # Raw volumes per region_id
    raw_volumes = {
        region_id: voxel_sum * voxel_volume
        for region_id, voxel_sum in zip(masker.region_names_, masked_image)
    }

    # Total cerebellum volume
    cereb_vol = sum(
        raw_volumes[rid]
        for rid in cerebellum_region_ids
        if rid in raw_volumes
    )
    if cereb_vol == 0:
        raise ValueError("Cerebellum volume is zero, cannot normalize.")

    # Normalize by cerebellum
    norm_volumes = {
        masker.region_names_[rid]: vol / cereb_vol
        for rid, vol in raw_volumes.items()
    }

    return norm_volumes