# ffmpeg Tools.py
version = "1.4"
# Max Laurie 14/02/2021

# Provides ffmpeg commands with a main menu for selection
# 1. Muxes in a sub file with a video and rewraps as mkv
# 2. Converts audio track in video file to ac3
# 3. Transcode to an hq h264
# 4. Transcode to an hq h265
# 5. Transcodes to h265 and scales to your chosen width
# 6. Rewraps a video into your chosen wrapper

# 1.4 changelog
# Complete rework

import os
import sys
from art import text2art


# Funcs

class video_file:
    def __init__(self, file):
        self.codec = return_video_spec(file, "codec_name")
        self.profile = return_video_spec(file, "profile")
        self.width = return_video_spec(file, "width")
        self.height = return_video_spec(file, "height")
        self.field_order = return_video_spec(file, "field_order")
        self.frame_rate = return_video_spec(file, "r_frame_rate")
        self.filepath = file
        self.path = os.path.splitext(file)[0]
        self.ext = os.path.splitext(file)[1]


def banner(title, subtitle=""):
    print(text2art(title))
    print(subtitle + "\n")


def script_exit(exitText):
    print("\n" + exitText)
    input("Press enter to exit...")
    sys.exit()


def return_video_spec(input_file, spec):
    return os.popen(f'ffprobe -i "{input_file}" -select_streams v:0 -show_entries stream={spec} -v 0 -of compact=p=0:nk=1').read()


def return_available_filename(file_path, desired_ext):
    output_filename = file_path + desired_ext
    i = 2
    while os.path.isfile(output_filename):
        output_filename = file_path + "_" + str(i) + desired_ext
        i += 1
    return output_filename


def shutdown_choice():
    user_choice = ""
    while user_choice not in ["y", "n"]:
        user_choice = input("Shutdown computer after? [y/n]: ")
    if user_choice == "y":
        return True
    else:
        return False


def shutdown():
    os.system("shutdown -s")


# Commands

def add_subs_ffmpeg_command(video_file, sub_file, output_file):
    os.system(f'ffmpeg -i "{video_file}" -i "{sub_file}" -map 0 -map 1 -c copy "{output_file}"')


def add_subs(input_files):
    video_formats = (".mp4", ".mov", ".mkv")
    sub_formats = (".stl", ".srt", ".sub")

    if len(input_files) != 2:
        script_exit("Please provide one video file and one sub file")

    for file in input_files:
        file_extension = os.path.splitext(file)[1]
        if file_extension.casefold() in video_formats:
            video_file = video_file(file)
        if file_extension.casefold() in sub_formats:
            sub_file = file

    if video_file in locals() and sub_file in locals():
        shutdown_bool = shutdown_choice()
        output_file = return_available_filename(video_file.path, "_SUBS.mkv")
        add_subs_ffmpeg_command(video_file.filepath, sub_file, output_file)
        
        if os.path.isfile(output_file):
            banner("File made:", output_file)
        else:
            banner("Failed", output_file)

        if shutdown_bool is True:
            shutdown()
        else:
            script_exit("Script complete")
    else:
        script_exit("Invalid combination of files provided")


def dts_to_ac3(input_files):
    files_complete = []
    shutdown_bool = shutdown_choice()

    for file in input_files:
        current_file = video_file(file)
        output_file = return_available_filename(current_file.path, "_AC3" + current_file.ext)

        dts_to_ac3_ffmpeg_command(current_file.filepath, output_file)

        if os.path.isfile(output_file):
            files_complete.append(output_file)
        else:
            files_complete.append("FAILED - " + output_file)

    if shutdown_bool is True:
            shutdown()
    else:    
        banner("Files converted:")
        for file in files_complete:
            print(file)
        script_exit("Script complete")


def dts_to_ac3_ffmpeg_command(input_file, output_file):
    os.system(f'ffmpeg -i "{input_file}" -map 0 -vcodec copy -scodec copy -acodec ac3 -b:a 640k "{output_file}"')


def h264_transcode(input_files):
    files_complete = []
    shutdown_bool = shutdown_choice()

    for file in input_files:
        current_file = video_file(file)
        output_file = return_available_filename(current_file.path, ".mp4")

        h264_ffmpeg_command(current_file.filepath, output_file)

        if os.path.isfile(output_file):
            files_complete.append(output_file)
        else:
            files_complete.append("FAILED - " + output_file)

    if shutdown_bool is True:
            shutdown()
    else:    
        banner("Files converted:")
        for file in files_complete:
            print(file)
        script_exit("Script complete")


def h264_ffmpeg_command(input_file, output_file):
    os.system(f'ffmpeg -i "{input_file}" -map 0 -map -0:d -vcodec libx264 -preset slower -crf 15 -acodec aac -b:a 380k "{output_file}"')


def h265_transcode(input_files):
    files_complete = []
    shutdown_bool = shutdown_choice()

    for file in input_files:
        current_file = video_file(file)
        output_file = return_available_filename(current_file.path, ".mp4")

        h265_ffmpeg_command(current_file.filepath, output_file)

        if os.path.isfile(output_file):
            files_complete.append(output_file)
        else:
            files_complete.append("FAILED - " + output_file)

    if shutdown_bool is True:
            shutdown()
    else:    
        banner("Files converted:")
        for file in files_complete:
            print(file)
        script_exit("Script complete")


def h265_ffmpeg_command(input_file, output_file):
    os.system(f'ffmpeg -i "{input_file}" -map 0 -map -0:d -vcodec libx265 -preset slow -crf 26 -acodec aac -b:a 380k "{output_file}"')


def h265_transcode_and_scale(input_files):
    output_width = input("Width of output file(s): ")
    files_complete = []
    shutdown_bool = shutdown_choice()

    for file in input_files:
        current_file = video_file(file)
        output_file = return_available_filename(current_file.path, ".mp4")

        h265_and_scale_ffmpeg_command(current_file.filepath, output_file, output_width)

        if os.path.isfile(output_file):
            files_complete.append(output_file)
        else:
            files_complete.append("FAILED - " + output_file)

    if shutdown_bool is True:
            shutdown()
    else:    
        banner("Files converted:")
        for file in files_complete:
            print(file)
        script_exit("Script complete")


def h265_and_scale_ffmpeg_command(input_file, output_file, output_width):
    os.system(f'ffmpeg -i "{input_file}" -vf scale={output_width}:-1 -map 0 -map -0:d -vcodec libx265 -preset slow -crf 26 -acodec copy "{output_file}"')


def rewrap(input_files):
    new_extension = input("New file wrapper: ")
    files_complete = []
    shutdown_bool = shutdown_choice()

    for file in input_files:
        current_file = video_file(file)
        output_file = return_available_filename(current_file.path, "." + new_extension)

        rewrap_ffmpeg_command(current_file.filepath, output_file)

        if os.path.isfile(output_file):
            files_complete.append(output_file)
        else:
            files_complete.append("FAILED - " + output_file)

    if shutdown_bool is True:
            shutdown()
    else:    
        banner("Files rewrapped:")
        for file in files_complete:
            print(file)
        script_exit("Script complete")


def rewrap_ffmpeg_command(input_file, output_file):
    os.system(f'ffmpeg -i "{input_file}" -map 0 -c copy "{output_file}"')


# Main

sysargs = sys.argv
input_files = []
# keep all but the script sysarg
for file in sysargs:
    path_and_ext = os.path.splitext(file)
    if path_and_ext[1].casefold() != ".py" and path_and_ext[1].casefold() != ".exe":
        input_files.append(file)

os.system('cls')
banner("FFmpeg Tools", f"{version} Max Laurie")

if len(input_files) < 1:
        script_exit("Please provide at least one video file")

print("1        Add Subs")
print("2        DTS to AC3")
print("3        Transcode to HQ H264")
print("4        Transcode to HQ H265")
print("5        Transcode to HQ H265 and scale")
print("6        Rewrap")
print("0        Exit")

while True:
    user_selection = input("\n- ")
    if user_selection.isnumeric() and int(user_selection) in range(0, 7):
        if int(user_selection) == 1:
            os.system('cls')
            banner("Add Subs")
            add_subs(input_files)
        if int(user_selection) == 2:
            os.system('cls')
            banner("DTS to AC3")
            dts_to_ac3(input_files)
        if int(user_selection) == 3:
            os.system('cls')
            banner("H264 Transcode")
            h264_transcode(input_files)
        if int(user_selection) == 4:
            os.system('cls')
            banner("H265 Transcode")
            h265_transcode(input_files)
        if int(user_selection) == 5:
            os.system('cls')
            banner("H265 Scaled Transcode")
            h265_transcode_and_scale(input_files)
        if int(user_selection) == 6:
            os.system('cls')
            banner("Rewrap")
            rewrap(input_files)
        if int(user_selection) == 0:
            sys.exit()
    else:
        continue
