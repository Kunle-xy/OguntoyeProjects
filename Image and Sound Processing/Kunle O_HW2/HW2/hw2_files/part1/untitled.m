close all;
img = imread('image_part1a.png');


kernel_erode = strel('rectangle', [1, 50]);
kernel_dilate = strel('rectangle', [1, 90]);

img_gray = (im2gray(img) == 255);

result_horizontal = imerode(img_gray, kernel_erode);
result_horizontal = imdilate(result_horizontal, kernel_dilate);

% figure;
% imshow(result_horizontal)
% filename = 'part1_a';
% saveas(gcf, filename, 'jpg');

kernel_dilate = strel('rectangle', [50, 1]);
kernel_erode = strel('rectangle', [90, 2]);

img_gray = (im2gray(img) == 255);

result_vertical = imdilate(img_gray, kernel_dilate);
result_vertical = imerode(result_vertical, kernel_erode);

figure;
imshow(result_vertical)
% imshowpair(result_vertical, img_gray, 'montage')
filename = 'part1_b';
saveas(gcf, filename, 'jpg');
