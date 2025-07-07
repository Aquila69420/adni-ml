
dicom_folder = 'adni-ml/data/phantom_spect/phantom.dcm'
nifti_folder = 'adni-ml/data/phantom_spect_nifti'

dicom_to_nifti(dicom_folder, nifti_folder)
function dicom_to_nifti(dicom_file, nifti_folder)

    spm('defaults', 'PET'); % initiate SPM with PET settings

    % Ensure output directory exists
    if ~exist(nifti_folder, 'dir')
        mkdir(nifti_folder);
    end

    % Create the SPM batch for DICOM import
    matlabbatch{1}.spm.util.import.dicom.data = {dicom_file}; % single DICOM file
    matlabbatch{1}.spm.util.import.dicom.root = 'flat';
    matlabbatch{1}.spm.util.import.dicom.outdir = {nifti_folder};
    matlabbatch{1}.spm.util.import.dicom.protfilter = '.*';
    matlabbatch{1}.spm.util.import.dicom.convopts.format = 'nii';

    spm_jobman('run', matlabbatch); % run the batch

    % Get filename without extension to name the output
    [~, name, ~] = fileparts(dicom_file);

    % Get the converted NIfTI file
    output_files = dir(fullfile(nifti_folder, '*.nii'));
    
    if ~isempty(output_files)
        old_file_path = fullfile(nifti_folder, output_files(1).name);
        new_file_path = fullfile(nifti_folder, sprintf('%s.nii', name));
        movefile(old_file_path, new_file_path); % rename the NIfTI file
    else
        warning('No NIfTI file was created for %s', dicom_file);
    end
end