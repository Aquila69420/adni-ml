% define paths here 



% function defined below for coregistering the image with the template. THis doesnt change the acc image only the metadata
function coregister(nifti_folder)
    spm('defaults', 'PET');
    spm_jobman('initcfg');
    matlabbatch = {};

    image_files = dir(fullfile(nifti_folder, '*.nii'));

    % set the origin to the centre of the image, taken from external source (https://www.nemotos.net/scripts/acpc_coreg.m_)
    for i = 1:numel(image_files)
        file = fullfile(nifti_folder, image_files(i).name);
        st.vol = spm_vol(file);
        vs = st.vol.mat\eye(4);
        vs(1:3, 4) = (st.vol.dim+1)/2;
        spm_get_space(st.vol.fname, inv(vs));
    end

    spm('CreateIntWin', 'on');
    spm_figure('Create', 'Graphics', 'on')

    % co-register with the template image
    for i = 1:numel(image_files)
        matlabbatch{i}.spm.spatial.coreg.estimate.ref = {fullfile(spm('dir'),'toolbox','DARTEL','icbm152.nii,1')};
        matlabbatch{i}.spm.spatial.coreg.estimate.source = {fullfile(folder_path, img_files(i).name)};
        matlabbatch{i}.spm.spatial.coreg.estimate.other = {''};
        matlabbatch{i}.spm.spatial.coreg.estimate.eoptions.cost_fun = 'nmi';
        matlabbatch{i}.spm.spatial.coreg.estimate.eoptions.sep = [4 2];
        matlabbatch{i}.spm.spatial.coreg.estimate.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
        matlabbatch{i}.spm.spatial.coreg.estimate.eoptions.fwhm = [7 7];
    end
    spm_jobman('run', matlabbatch);
end

