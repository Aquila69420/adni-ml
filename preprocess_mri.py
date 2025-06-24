import os
import nilearn as nil

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
    img = nil.image.load_img(img_path)
    registered_img = nil.image.resample_to_img(img, mni_img, copy_header=True, force_resample=True)
    return registered_img

def segment_with_atlas(registered_img, atlas_img, labels):
    """Segment a registered image using an atlas."""
    masker = nil.maskers.NiftiLabelsMasker(atlas_img, labels=labels, standardize=True)
    segmented = masker.fit_transform(registered_img)
    return segmented