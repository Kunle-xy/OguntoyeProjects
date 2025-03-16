video_path = 'p5b_video3_result.mp4';
videoReader = VideoReader(video_path);
videoWriter = VideoWriter('p5b_video3_result1.mp4', 'MPEG-4');
videoWriter.FrameRate = videoReader.FrameRate;

open(videoWriter);

while hasFrame(videoReader)
    frame = readFrame(videoReader);

    % Write the frame
    writeVideo(videoWriter, frame); % Convert back to BGR for consistency
end

close(videoWriter);
