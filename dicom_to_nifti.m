% Define the locations here


% dicome to nifti function laid out below
function dicom_to_nifti(dicom_folder, nifti_folder)

    spm('defaults', 'PET'); % intiatiate SPM with PET settings
    
    sub_folders = dir(dicom_folder); % list of all the subfolders n the dicom folder path that is given
    participant_ids = sub_folders([sub_folders.isdir] & ~ismember({sub_folders.name}, {'.', '..'}));  %  list of all the subfolders that are not the parent or current folder

    for i = numel(participant_ids); % loop through each participant folder
        current_folder = fullfile(dicom_folder, participant_ids(i).name);

        patient_id = participant_ids(i).name;

        matlabbatch{1}.spm.util.import.dicom.data = cellstr(spm_select('FPList', current_folder, '.*\.dcm$')); % input data that is a list of all the DICOM (DCM) files in the current folder
        matlabbatch{1}.spm.util.import.dicom.root = 'flat'; % flat pathstructure
        matlabbatch{1}.spm.util.import.dicom.outdir = {nifti_folder}; % ouput path for the converted files
        matlabbatch{1}.spm.util.import.dicom.protfilter = '.*'; % protocal settings
        matlabbatch{1}.spm.util.import.dicom.convopts.format = 'nii'; % NifTi format for the output

        spm_jobman('run', matlabbatch); % run the bathc

        output_files = dir(fullfile(nifti_folder,'*.nii')); % list all the output files in the nifti folder (this is within the loop so it will only be one)

        old_file_path = fullfile(nifti_folder, output_files(1).name); % get the path of the converted nifti file
        new_file_path = fullfile(nifti_folder, sprintf('%s.nii', patient_id)); % in effect renames the file

        movefile(old_file_path, new_file_path);
    end
end