% define paths here


% function below 
function segmentation(normalised_folder, output_folder, output_file_name, atlas_names, atlas_masks)
    image_files = dir(fullfile(normalised_folder, '*.nii'));

    [ ~ , ~ , raw] = xlsread(atlas_names); % splits into the data type
    regions = raw(:, 3) % get list of region names

    results = cell(length(image_files) + 1, length(regions) * 3 + 1); % define the structure of the results, with rows for all patients + header, and columns for each region's sum, mean, and std + var name

    results{1, 1} = 'File'; % first column is the file name
    for col = 1: numel(regions) % loop through the regions and create headers for each region's statistics
        results{1, col * 3} = ['Sum_' regions{col}]; % sum
        results{1, col * 3 + 1} = ['Mean_' regions{col}]; % mean    
        results{1, col * 3 + 2} = ['Std_' regions{col}]; % std
    end

    for i = 1:numel(image_files) % loop through each file
        scan_file = fullfile(normalised_folder, image_files(i).name); % get the full file path
        scan = single(niftiread(scan_file)); % read the scan file

        for j = 1:numel(regions) % loop through each region
            region_file = fullfile(atlas_masks, [regions{j}]); % get the region mask for that region from the atlas masks folder

            mask = single(niftiread(region_file)); % read it in as an nifti file

            mask = imresize(mask, size(scan), 'linear'); % resize to match the san size

            masked_scan = scan .* mask; % apply the mask to the scan

            non_zero_masked_scan = masked_scan(~isnan(masked_scan(:))); % extract all non-zero values and store in array

            % caclulate the relevant statistice we need 
            sum_value = sum(non_zero_masked_scan);
            mean_value = mean(non_zero_masked_scan);
            std_value = std(non_zero_masked_scan);

            % store in respective rows and cols in results
            results(i + 1, 1) = {image_files(i).name};
            results{i + 1, j * 3} = sum_value;
            results{i + 1, j * 3 + 1} = mean_value;
            results{i + 1, j * 3 + 2} = std_value;
        end
    end

    % convert nums to str to avoind issue sin table
    results = cellfun(@num2str, results, 'UniformOutput', false);

    % create and write the output tabkle and save in the specified folder
    var_names = results(1, :)

    output_table = cell2table(results(2:end, :), 'VariableNames', var_names);
    
    writetable(output_table, fullfile(output_folder, output_file_name), 'WriteVariableNames', true);

end