% define path here

% the template needs to also specify the volume number (,1/2/...) and also must be a cell array

%template = {'C:\Users\huw\OneDrive\Documents\Year 4\Project\templates\Template_FBP_all.nii,1'
%            'C:\Users\huw\OneDrive\Documents\Year 4\Project\templates\Template_FBP_neg.nii,1'
%            'C:\Users\huw\OneDrive\Documents\Year 4\Project\templates\Template_FBP_pos.nii,1'
%            }
% define the function to noramlise to a template(s)
function normalise(coregister_folder, normalised_folder, template)

    spm('defaults', 'PET');     % set up the spm job and batch
    spm_jobman('initcfg');
    matlabbatch = {};

    image_files = dir(fullfile(coregister_folder, '*.nii'));        % list of files in the coregistered folder

    for i = 1:numel(image_files) % loop through each file and set p the bathc structure with source path, weightings and resample 
        matlabbatch{1}.spm.tools.oldnorm.estwrite.subj(i).source = {fullfile(coregister_folder, image_files(i).name)};
        matlabbatch{1}.spm.tools.oldnorm.estwrite.subj(i).wtsrc = '';
        matlabbatch{1}.spm.tools.oldnorm.estwrite.subj(i).resample = {fullfile(coregister_folder, image_files(i).name)};  
    end

    % Dfine the norm parameters which are taken from a foorum suggested for old norm 
    matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.template = template; % template for norm
    matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.weight = ''; % weighting (set to none here)
    matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.smosrc = 8; % smoothing for source
    matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.smoref = 0; % smoothing for reference
    matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.regtype = 'mni'; % reg type
    matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.cutoff = 25; % norm cutoff
    matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.nits = 16; % number of iterations
    matlabbatch{1}.spm.tools.oldnorm.estwrite.eoptions.reg = 1; % number of regularisations
    matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.preserve = 0; % preserve teh original
    matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.bb = [-100 -130 -80
                                                            100 100 110]; % bounding box for normalised image
    matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.vox = [2 2 2]; % voxel size
    matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.interp = 1; % interpolation method
    matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.wrap = [0 0 0]; % wrap around
    matlabbatch{1}.spm.tools.oldnorm.estwrite.roptions.prefix = 'normalised_'; % prefix for file

    % progress message
    disp('Normalization in progress...');
    spm_jobman('run', matlabbatch); % run this
    disp('Normalization completed successfully.');
    
    % move the files to the normalised folder
    for i = 1:numel(image_files)
        old_path = fullfile(coregister_folder, ['normalised_', fileList(i).name]);
        new_path = fullfile(normalised_folder, ['normalised_', fileList(i).name]);
        movefile(old_path, new_path);
    end
end