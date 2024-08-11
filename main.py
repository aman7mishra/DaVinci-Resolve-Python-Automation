import os

#Media Settings:
mediaPath = "/Users/amanmishra/upwork/Python_Script_for_DaVinci_Resolve/media"            #Update the path 
render_folder = os.path.join(mediaPath, "rendered_videos")
clips_info = [
    {
        "file": "bernie.jpg", 
        "start": "00:00:00,000", 
        "end": "00:00:12,500", 
        "text": "Hello, and welcome back to our podcast! Im your host, Bernie."
    },
    {
        "file": "jessica_zoom_out.mp4", 
        "start": "00:00:12,500", 
        "end": "00:00:16,114", 
        "text": "And Im Jessica, here to crack the tough codes!"
    },
    {
        "file": "bernie_zoom_out.mp4", 
        "start": "00:00:16,114", 
        "end": "00:00:18,177", 
        "text": "Dont forget about me, Frank, with the latest gadget news.",
    },
    {
        "file": "all_slide_right.mp4", 
        "start": "00:00:18,177", 
        "end": "00:00:25,217", 
        "text": "Together, we bring you the latest and greatest in tech!"
    }]

# Project Settings:
projectName = "test2"
framerate = "60"
width = "1920"
height = "1080"


# Creating SRT file for captions
def create_srt(clips_info, output_file):
    with open(output_file, 'w') as f:
        for i, clip in enumerate(clips_info, start=1):
            f.write(f"{i}\n")
            f.write(f"{clip['start']} --> {clip['end']}\n")
            f.write(f"{clip['text']}\n\n")

output_file = mediaPath + "/captions.srt"
create_srt(clips_info, output_file)

# Create project and set parameters:
projectManager = resolve.GetProjectManager()
project = projectManager.CreateProject(projectName)

if not project:
    print("Unable to create a project '" + projectName + "'")
    sys.exit()

# Apply Project settings:
project.SetSetting("timelineFrameRate", str(framerate))
project.SetSetting("timelineResolutionWidth", str(width))
project.SetSetting("timelineResolutionHeight", str(height))

# Add folder contents to Media Pool:
mediapool = project.GetMediaPool()
rootFolder = mediapool.GetRootFolder()
clips = resolve.GetMediaStorage().AddItemListToMediaPool(mediaPath)

# Create timeline:
timelineName = "Timeline 1"
timeline = mediapool.CreateEmptyTimeline(timelineName)
if not timeline:
    print("Unable to create timeline '" + timelineName + "'")
    sys.exit()

mediapool_file_titles_and_index = {}
for idx, clip in enumerate(clips):
    mediapool_file_titles_and_index[clip.GetName()] = idx


for clip in clips_info:
    try:
        mediapool.AppendToTimeline(clips[mediapool_file_titles_and_index[clip["file"]]])
    except KeyError:
        print("Media file by the name - {} is missing".format(clip["file"]))
        sys.exit()

mediapool.AppendToTimeline(clips[mediapool_file_titles_and_index["captions.srt"]])

# Saving the project:
projectManager.SaveProject()
print("'" + projectName + "' has been saved")

print("Please validate the media files in the timeline. To re-position the media files, simply drag them.!!")

print("To render the video, please open the render_video.py file")