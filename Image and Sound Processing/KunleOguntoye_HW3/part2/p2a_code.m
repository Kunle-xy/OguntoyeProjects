% Assuming 'p2_image1.png' is in the current directory
imageName = 'p2_image3.png';

% Read the image and convert it to grayscale
image = imread(imageName);
imageGray = rgb2gray(image);

% Apply binary thresholding
thresh = imbinarize(imageGray, 150/255);

% Convert image to RGB (if it's not already)
imageRGB = im2uint8(image); % If the image is already RGB, this step can be skipped.
if size(imageRGB, 3) == 1
    imageRGB = cat(3, imageRGB, imageRGB, imageRGB); % Convert grayscale to RGB
end

% Apply inverse binary thresholding
imageInv = imbinarize(imageGray, 230/255);
imageInv = imcomplement(imageInv);

% Calculate the bounding box size based on the image dimensions
[rows, cols, ~] = size(imageRGB);
boundingBoxRow = floor(rows / 4);
boundingBoxCol = floor(cols / 4);

% Loop through each segment of the image
for i = 1:4
    for j = 1:4
        % Extract the current block of the image
        block = imageInv((boundingBoxRow*(i-1) + 1):(boundingBoxRow*i), ...
                         (boundingBoxCol*(j-1) + 1):(boundingBoxCol*j));
        
        % Check if the current block contains significant white pixels
        if sum(block(:), 'all') > 1e4
            % Perform OCR on the block
            textStruct = ocr(block);
            text = textStruct.Text;
            fprintf('Detected text at (%d,%d): %s\n', i, j, text);
            
            % Define the position for the text annotation
            position = [(boundingBoxCol*(j-1) + 1), (boundingBoxRow*i) - 35]; % Adjusted for visibility
            
            % Insert text into the RGB image
            imageRGB = insertText(imageRGB, position, sprintf('(%d,%d)', i, j), 'FontSize', 18, 'BoxOpacity', 0, 'TextColor', 'red');
        end
    end
end

% Display the resulting image
figure;
imshow(imageRGB);
imwrite(imageRGB, "p2_image3_with_text.png")
title('Image with Text Annotations');
