# FFmpegTools.py
version = "2.0"
# Max Laurie 13/12/2022

# Provides ffmpeg commands with a main menu for selection
# 1. Muxes in a sub file with a video and rewraps as mkv
# 2. Converts audio track in video file to ac3
# 3. Transcode to an hq h264
# 4. Transcode to an hq h265
# 5. Transcodes to h265 and scales to your chosen width
# 6. Rewraps a video into your chosen wrapper

# 2.0 changelog
# Complete rework

import os
import sys
from art import text2art


############### Classes ###############

class Menu:
    def __init__(self):
        self.items = [
            MenuItem("Add Subs", add_subs_ffmpeg_command, "_SUBS", ".mkv", sort_video_and_subs),
            MenuItem("DTS to AC3", dts_to_ac3_ffmpeg_command, "_AC3", None, None),
            MenuItem("Transcode to HQ H264", h264_ffmpeg_command, None, ".mp4", None),
            MenuItem("Transcode to HQ H265", h265_ffmpeg_command, None, ".mp4", None),
            MenuItem("Transcode to H265 and Scale", h265_and_scale_ffmpeg_command, None, ".mp4", get_desired_resolution),
            MenuItem("Rewrap", rewrap_ffmpeg_command, None, None, get_desired_file_wrapper),
            MenuItem("Exit", None, None, None, None)
                    ]

    def display(self):
        banner("FFmpeg Tools", f"{version} Max Laurie")
        i = 1
        for item in self.items:
            print(f"{i}{(' ' * 8)}{item.title}")
            i += 1
        print("\n")

    def get_user_choice(self):
        while True:
            user_choice = input("- ")
            if user_choice.isnumeric() and int(user_choice) in range(len(self.items) + 1):
                return self.items[(int(user_choice) - 1)]


class MenuItem:
    def __init__(self, title, command, suffix, ext, secondary_function):
        self.title = title
        self.command = command
        self.suffix = suffix
        self.ext = ext
        self.secondary_function = secondary_function


class VideoFile:
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


################ Funcs ################

def clear_screen():
	if sys.platform == "win32":
		os.system("cls")
	else:
		os.system("reset")


def banner(title, subtitle=""):
    clear_screen()
    print(text2art(title))
    print(subtitle + "\n")


def return_video_spec(input_file, spec):
    return os.popen(f'ffprobe -i "{input_file}" -select_streams v:0 -show_entries stream={spec} -v 0 -of compact=p=0:nk=1').read()


def return_available_filename(menu_choice, current_file):
    if menu_choice.suffix is None:
        menu_choice.suffix = ""
    if menu_choice.ext is None:
        menu_choice.ext = current_file.ext

    output_filename = current_file.path + menu_choice.suffix + menu_choice.ext
    numbered_suffix = 2
    while os.path.isfile(output_filename):
        output_filename = current_file.path + menu_choice.suffix + "_" + str(numbered_suffix) + menu_choice.ext
        numbered_suffix += 1
    return output_filename


def file_made_successfully_or_not(filename):
    file_stats = os.stat(filename)
    print(file_stats)
    if os.path.isfile(filename) and file_stats.st_size > 100000: #100kb
        return "Success"
    else:
        return "Failed"


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


def all_done(output_files):
    if len(output_files) < 2:
        plural_or_not = "Files made:"
    else:
        plural_or_not = "File made:"

    banner("All done", plural_or_not)
    for file in output_files:
        print(output_files[file] + "\n" + file)
    script_exit()


def script_exit(exitText=""):
    print("\n" + exitText)
    input("Press enter to exit...")
    sys.exit()


############## Commands ##############

def sort_video_and_subs(menu_choice):
    video_formats = (".mp4", ".mov", ".mkv")
    sub_formats = (".stl", ".srt", ".sub")

    if len(menu_choice.input_files) != 2:
        script_exit("Please provide one video file and one sub file\n")
    
    input_files = menu_choice.input_files
    video_found = False
    subs_found = False
    for file in input_files:
        file_extension = os.path.splitext(file)[1]
        if file_extension.casefold() in video_formats:
            menu_choice.input_files = [file]
            video_found = True
        if file_extension.casefold() in sub_formats:
            menu_choice.sub_file = file
            subs_found = True

    if video_found is False or subs_found is False:
        script_exit("Invalid combination of files provided\n")


def get_desired_resolution(menu_choice):
    menu_choice.output_width = input("Desired width of output files: ")


def get_desired_file_wrapper(menu_choice):
    desired_wrapper = input("New file wrapper: ")
    if desired_wrapper.startswith("."):
        menu_choice.ext = desired_wrapper
    else:
        menu_choice.ext = "." + desired_wrapper


def add_subs_ffmpeg_command(input_filename, output_filename, menu_choice):
    os.system(f'ffmpeg -hide_banner -i "{input_filename}" -i "{menu_choice.sub_file}" -map 0 -map 1 -c copy "{output_filename}"')


def dts_to_ac3_ffmpeg_command(input_filename, output_filename, menu_choice):
    os.system(f'ffmpeg -i "{input_filename}" -map 0 -vcodec copy -scodec copy -acodec ac3 -b:a 640k "{output_filename}"')


def h264_ffmpeg_command(input_filename, output_filename, menu_choice):
    os.system(f'ffmpeg -i "{input_filename}" -map 0 -map -0:d -vcodec libx264 -preset slower -crf 15 -acodec aac -b:a 380k "{output_filename}"')


def h265_ffmpeg_command(input_filename, output_filename, menu_choice):
    os.system(f'ffmpeg -i "{input_filename}" -map 0 -map -0:d -vcodec libx265 -preset slow -crf 26 -acodec aac -b:a 380k "{output_filename}"')


def h265_and_scale_ffmpeg_command(input_filename, output_filename, menu_choice):
    os.system(f'ffmpeg -i "{input_filename}" -vf scale={menu_choice.output_width}:-1 -map 0 -map -0:d -vcodec libx265 -preset slow -crf 26 -acodec copy "{output_filename}"')


def rewrap_ffmpeg_command(input_filename, output_filename, menu_choice):
    os.system(f'ffmpeg -i "{input_filename}" -map 0 -c copy "{output_filename}"')


def ffmpeg_command(menu_choice):
    banner(menu_choice.title)
    if menu_choice.secondary_function is None:
        pass
    else:
        menu_choice.secondary_function(menu_choice)

    shutdown_bool = shutdown_choice()

    files_complete = {}
    for file in menu_choice.input_files:
        current_file = VideoFile(file)

        output_filename = return_available_filename(menu_choice, current_file)
        menu_choice.command(current_file.filepath, output_filename, menu_choice)

        files_complete[output_filename] = file_made_successfully_or_not(output_filename)
        
    if shutdown_bool is True:
        shutdown()
    else:
        all_done(files_complete)


################ Main ################

def main(input_files):
    main_menu = Menu()
    main_menu.display()
    menu_choice = main_menu.get_user_choice()
    menu_choice.input_files = input_files
    if menu_choice.title == "Exit":
        sys.exit()
    else:
        ffmpeg_command(menu_choice)


if __name__ == "__main__":
    sys.argv.pop(0)
    if len(sys.argv) < 1:
        script_exit("Please provide at least one input file")
    main(sys.argv)
