clc;close all;clear;
image = imread('p1_image3.png');

% Convert to grayscale
image_gray = rgb2gray(image);

% Apply a binary threshold
thresh = imbinarize(image_gray, 150/255);

% Read the original image for drawing
image_rgb = imread('p1_image3.png');

% Calculate the bounding box size (assuming image is evenly divisible by 4)
boundingBox = [size(image, 1)/4, size(image, 2)/4];

% Initialize the result variable
result = cell(4,4);

% Loop through each grid segment
for i = 1:4
    for j = 1:4
        % Extract the segment of the image
        img = image_gray((boundingBox(1)*(i-1) + 1):(boundingBox(1)*i), ...
                        (boundingBox(2)*(j-1) + 1):(boundingBox(2)*j), :);

        % Use OCR to find text in the image segment
        ocrResults = ocr(img);

        % Loop through each word detected by OCR
        for k = 1:numel(ocrResults.Words)
            wordBox = ocrResults.WordBoundingBoxes(k,:);

            % Adjust the box coordinates based on the grid segment
            wordBox(1) = wordBox(1) + boundingBox(2)*(j-1);
            wordBox(2) = wordBox(2) + boundingBox(1)*(i-1);

            % Draw rectangles around each word
            image_rgb = insertShape(image_rgb, 'Rectangle', wordBox, ...
                                    'Color', 'red', 'LineWidth', 2);
        end
    end
end

% Display the result
imshow(image_rgb);
imwrite(image_rgb, 'p1_image3_with_boxes.png')