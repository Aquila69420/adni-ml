% Define the locaions here 



% Function below
function process_dicom_download(data_folder, destination_root_folder)

    all_sub_folders = dir(data_folder); % returns all the subfolders within the data folder

    participant_ids = all_sub_folders([all_sub_folders.isdir] & ~ismember({all_sub_folders.name}, {'.', '..'}));  % filter out the parent and current folders and return a list of participants

    for i = 1:numel(participant_ids) % loop  through each participant

        participant_folder = fullfile(data_folder, participant_ids(i).name); % participant root folder

        participant_id = participant_ids(i).name; % participant id
        participant_destination_folder = fullfile(destination_root_folder, patient_id); % build destination file path for the participant

        if ~exist(participant_destination_folder, 'dir') % check if it already exists,and if it doesnt create it
            mkdir(participant_destination_folder); 
        end
        copyfile(fullfile(participant_folder, '*.*'), patient_destination_folder); % copy all the contents of original particapant folder to new destintion
        fprintf('Copied for patient %s to %s\n', participant_id, patient_destination_folder); % progress check
 

    end
end    
