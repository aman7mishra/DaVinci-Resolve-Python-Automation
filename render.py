# Rendering:
import time

def add_timeline_to_render( project, timeline, presetName, targetDirectory, filename, renderFormat, renderCodec ):
    project.SetCurrentTimeline(timeline)
    project.LoadRenderPreset(presetName)

    if not project.SetCurrentRenderFormatAndCodec(renderFormat, renderCodec):
        return False
    
    if with_subtitles:
        print("To enable Caption/Subtitle in the video! \n -> Please check the 'Export Subtitle' and select 'Burn into Video' in the  'Subtitle Setting' on Left bottom")
        print("The program will give you 10 seconds to perform this manual action")
        time.sleep(10)

    project.SetRenderSettings({"SelectAllFrames" : 1, 
                               "TargetDir" : targetDirectory,
                               "CustomName": filename
                               })
    return project.AddRenderJob()

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

def is_rendering_in_progress(resolve):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    if not project:
        return False

    return project.IsRenderingInProgress()

def wait_for_rendering(resolve):
    while is_rendering_in_progress(resolve):
        time.sleep(1)
    return

#Cleanup:
def delete_all_rendering_jobs( resolve ):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    project.DeleteAllRenderJobs()
    return


if not render_all_timelines(resolve, renderPresentName, render_folder, render_filename, renderFormat, renderCodec):
    print("Unable to set all timelines for rendering")
    sys.exit()

wait_for_rendering(resolve)

delete_all_rendering_jobs(resolve)

print("Rendering is completed.")