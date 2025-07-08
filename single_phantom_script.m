dicom_file = 'phantom_spect\phantom.dcm';  % single DICOM file
output_file = 'phantom_spect';  % desired NIfTI output path

spm('defaults', 'PET');

% Set up batch for single DICOM conversion
matlabbatch{1}.spm.util.import.dicom.data = {dicom_file};  % single file in a cell
matlabbatch{1}.spm.util.import.dicom.root = 'flat';
matlabbatch{1}.spm.util.import.dicom.outdir = output_file;
matlabbatch{1}.spm.util.import.dicom.protfilter = '.*';
matlabbatch{1}.spm.util.import.dicom.convopts.format = 'nii';

% Run the job
spm_jobman('run', matlabbatch);

