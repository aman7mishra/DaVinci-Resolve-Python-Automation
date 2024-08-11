
# DaVinci Resolve Python Automation

This project contains Python scripts to automate the process of creating, configuring, and rendering video projects in DaVinci Resolve. The scripts handle media import, timeline creation, caption generation, and rendering.

## Project Overview
This project aims to streamline the video editing process by automating repetitive tasks in DaVinci Resolve using Python scripts. The automation includes:

- Setting up project settings like resolution and frame rate.
- Importing media files into the media pool.
- Creating timelines and adding media clips.
- Generating SRT files for captions.
- Rendering the final video with optional burned-in subtitles.


## Table of Contents

- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Script 1: `main.py`](#script-1-mainpy)
  - [Script 2: `render.py`](#script-2-renderpy)
- [Configuration](#configuration)
- [Notes](#notes)
- [License](#license)

## Project Overview

This project aims to streamline the video editing process by automating repetitive tasks in DaVinci Resolve using Python scripts. The automation includes:

- Setting up project settings like resolution and frame rate.
- Importing media files into the media pool.
- Creating timelines and adding media clips.
- Generating SRT files for captions.
- Rendering the final video with optional burned-in subtitles.

## Usage

### Script 1: `main.py`

This script is used to set up the DaVinci Resolve project, import media files, create timelines, and generate captions.

1. **Update Media Settings:**

   In `main.py`, update the `mediaPath` variable with the path to your media files.

    ```python
    mediaPath = "/path/to/your/media/files"
    ```

2. **Output:**

   - Creates a DaVinci Resolve project with the specified settings.
   - Imports media files and adds them to the timeline.
   - Generates an SRT file for captions.

### Script 2: `render.py`

This script handles rendering the project timelines with optional subtitles.

1. **Output:**

   - Adds the timelines to the render queue.
   - Starts the rendering process.
   - Deletes all render jobs after rendering is complete.

## Configuration

- **Project Settings:** In `main.py`, you can adjust the project settings like frame rate, resolution, and project name.

    ```python
    projectName = "MyProject"
    framerate = "24"
    width = "1920"
    height = "1080"
    ```

- **Render Settings:** In `render.py`, you can configure the render format, codec, and output file name.

    ```python
    renderPresentName = "ProRes Master"
    renderFormat = "mov"
    renderCodec = "ProRes422HQ"
    render_filename = "output_video.mov"
    ```

## Notes

- **Trim/Cut clips:** The current version of DaVinci Resolve API only supports trimming or cutting clips. Please ensure the clips follow the timestamps mentioned in the clips_info.

- **Positioning of clips:** The current version of DaVinci Resolve API only supports appending clips to the timeline. There is no option to move the clips around. 

- **Subtitles:** If you want to burn subtitles into the video, the script will pause for 10 seconds, allowing you to manually enable subtitles in the DaVinci Resolve UI. Follow the on-screen instructions.

- **File Paths:** Ensure all file paths are correctly set according to your environment.

### Script: `main.py`

This script automates the creation of a video project in DaVinci Resolve, setting up timelines, adding media files, and generating captions in SRT format.

#### **Sections Overview:**

1. **Media Settings:**
    - Defines paths and media clips to be used in the project.

2. **Project Settings:**
    - Configures project-specific parameters such as frame rate and resolution.

3. **Creating SRT File for Captions:**
    - Generates a subtitle file in SRT format using the provided clip information.

4. **Creating and Configuring the Project:**
    - Sets up the DaVinci Resolve project, applies settings, and imports media files.

5. **Creating the Timeline and Adding Media Clips:**
    - Creates a timeline in DaVinci Resolve and appends the media files to it.

6. **Saving the Project:**
    - Saves the project and instructs the user to verify the timeline.

---

#### **1. Media Settings:**

```python
mediaPath = "<Folder path>"
render_folder = os.path.join(mediaPath, "rendered_videos")
```

- **`mediaPath`:** Directory containing media files.
- **`render_folder`:** Path where rendered videos will be saved.

```python
clips_info = [
    {"file": "bernie.jpg", "start": "00:00:00,000", "end": "00:00:12,500", "text": "Hello, and welcome back to our podcast! I'm your host, Bernie."},
    {"file": "jessica_zoom_out.mp4", "start": "00:00:12,500", "end": "00:00:16,114", "text": "And I'm Jessica, here to crack the tough codes!"},
    {"file": "bernie_zoom_out.mp4", "start": "00:00:16,114", "end": "00:00:18,177", "text": "Don't forget about me, Frank, with the latest gadget news."},
    {"file": "all_slide_right.mp4", "start": "00:00:18,177", "end": "00:00:25,217", "text": "Together, we bring you the latest and greatest in tech!"}
]
```

- **`clips_info`:** List of dictionaries containing information about each media file, including start and end times for captions and the caption text.

---

#### **2. Project Settings:**

```python
projectName = "Test"
framerate = "60"
width = "1920"
height = "1080"
```

- **`projectName`:** Name of the project.
- **`framerate`:** Frame rate of the video.
- **`width`:** Width of the video resolution.
- **`height`:** Height of the video resolution.

---

#### **3. Creating SRT File for Captions:**

```python
def create_srt(clips_info, output_file):
    with open(output_file, 'w') as f:
        for i, clip in enumerate(clips_info, start=1):
            f.write(f"{i}\n")
            f.write(f"{clip['start']} --> {clip['end']}\n")
            f.write(f"{clip['text']}\n\n")
```

- **`create_srt()`:** Generates a `.srt` subtitle file using the clip information provided in `clips_info`.
- **`output_file`:** Path where the `.srt` file will be saved.

---

#### **4. Creating and Configuring the Project:**

```python
projectManager = resolve.GetProjectManager()
project = projectManager.CreateProject(projectName)

if not project:
    print("Unable to create a project '" + projectName + "'")
    sys.exit()
```

- **`CreateProject()`:** Creates a new project in DaVinci Resolve.

```python
project.SetSetting("timelineFrameRate", str(framerate))
project.SetSetting("timelineResolutionWidth", str(width))
project.SetSetting("timelineResolutionHeight", str(height))
```

- **`SetSetting()`:** Applies project settings for frame rate and resolution.

---

#### **5. Creating the Timeline and Adding Media Clips:**

```python
timelineName = "Timeline 1"
timeline = mediapool.CreateEmptyTimeline(timelineName)
if not timeline:
    print("Unable to create timeline '" + timelineName + "'")
    sys.exit()
```

- **`CreateEmptyTimeline()`:** Creates an empty timeline in the project.

```python
for clip in clips_info:
    try:
        mediapool.AppendToTimeline(clips[mediapool_file_titles_and_index[clip["file"]]])
    except KeyError:
        print("Media file by the name - {} is missing".format(clip["file"]))
        sys.exit()
```

- **`AppendToTimeline()`:** Adds each media file to the timeline based on the clip information provided.

---

#### **6. Saving the Project:**

```python
projectManager.SaveProject()
print("'" + projectName + "' has been saved")
```

- **`SaveProject()`:** Saves the project in DaVinci Resolve.

---

### Script: `render.py`

This script handles the rendering process for the DaVinci Resolve project, including adding timelines to the render queue, managing render settings, and starting the render process.

#### **Sections Overview:**

1. **Render Settings:**
    - Configures rendering parameters like format, codec, and output file name.

2. **Adding Timelines to Render:**
    - Adds the current timeline to the render queue.

3. **Rendering All Timelines:**
    - Iterates through all timelines and renders them.

4. **Render Job Management:**
    - Functions to check the render status, wait for completion, and delete render jobs.

---

#### **1. Render Settings:**

```python
renderPresentName = "ProRes Master"
renderFormat = "mov"
renderCodec = "ProRes422HQ"
render_filename = "test_video.mov"
with_subtitles = 1
```

- **`renderPresentName`:** Name of the render preset to be used.
- **`renderFormat`:** Format of the output video (e.g., `mov`).
- **`renderCodec`:** Codec to be used for rendering (e.g., `ProRes422HQ`).
- **`render_filename`:** Name of the output video file.
- **`with_subtitles`:** Flag to determine if subtitles should be burned into the video.

---

#### **2. Adding Timelines to Render:**

```python
def add_timeline_to_render( project, timeline, presetName, targetDirectory, filename, renderFormat, renderCodec ):
    project.SetCurrentTimeline(timeline)
    project.LoadRenderPreset(presetName)
    # Enable subtitles manually
    if with_subtitles:
        time.sleep(10)
    project.SetRenderSettings({
        "SelectAllFrames" : 1,
        "TargetDir" : targetDirectory,
        "CustomName": filename
    })
    return project.AddRenderJob()
```

- **`add_timeline_to_render()`:** Adds the timeline to the render queue with the specified settings. It also includes a delay to allow the user to manually enable subtitles.

---

#### **3. Rendering All Timelines:**

```python
def render_all_timelines( resolve, presetName, targetDirectory, filename, renderFormat, renderCodec ):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    if not project:
        return False

    resolve.OpenPage("Deliver")
    timelineCount = project.GetTimelineCount()

    for index in range (0, int(timelineCount)):
        if not add_timeline_to_render(project, project.GetTimelineByIndex(index + 1), presetName, targetDirectory, filename, renderFormat, renderCodec):
            return False
    return project.StartRendering()
```

- **`render_all_timelines()`:** Loops through all timelines in the project and adds them to the render queue. Then, it starts the rendering process.

---

#### **4. Render Job Management:**

```python
def wait_for_rendering(resolve):
    while is_rendering_in_progress(resolve):
        time.sleep(1)
    return
```

- **`wait_for_rendering()`:** Waits for the rendering process to complete by repeatedly checking the status.

```python
def delete_all_rendering_jobs( resolve ):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    project.DeleteAllRenderJobs()
    return
```

- **`delete_all_rendering_jobs()`:** Deletes all render jobs from the queue after rendering is complete.

---

This documentation should provide a clear understanding of how the scripts work and how to use them in the DaVinci Resolve project.