# ffmpeg Tools.py
version = "1.5"
# Max Laurie 13/12/2021

# Provides ffmpeg commands with a main menu for selection
# 1. Muxes in a sub file with a video and rewraps as mkv
# 2. Converts audio track in video file to ac3
# 3. Transcode to an hq h264
# 4. Transcode to an hq h265
# 5. Transcodes to h265 and scales to your chosen width
# 6. Rewraps a video into your chosen wrapper

# 1.5 changelog
# Fixed add subs, checking for variables in locals() was giving the wrong result
# and causing the script to throw an unboundvariable error
# Packed all the separate ffmpeg command funcs in to a single function with a switch statement

import os
import sys
from art import text2art


# Funcs
class Menu:
    def __init__(self):
        self.items = [
                        MenuItem("Add Subs", add_subs_ffmpeg_command, "_SUBS", None),
                        MenuItem("DTS to AC3", dts_to_ac3_ffmpeg_command, "_AC3", None),
                        MenuItem("Transcode to HQ H264", h264_ffmpeg_command, ".mp4", None),
                        MenuItem("Transcode to HQ H265", h265_ffmpeg_command, ".mp4", None),
                        MenuItem("Transcode to H265 and Scale", h265_and_scale_ffmpeg_command, ".mp4", "Desired Horizontal Resolution"),
                        MenuItem("Rewrap", rewrap_ffmpeg_command, "_REWRAP", "New File Wrapper"),
                        MenuItem("Exit", sys.exit, None, None)
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
    def __init__(self, title, command, suffix_andor_ext, extra_option):
        self.title = title
        self.command = command
        self.suffix_andor_ext = suffix_andor_ext
        self.extra_option = extra_option

    def get_extra_user_option(self):
        if self.extra_option is not None:
            return input(f"{self.extra_option}: ")
        else:
            return None


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


def banner(title, subtitle=""):
    os.system("cls")
    print(text2art(title))
    print(subtitle + "\n")


def files_made(output_files):
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

def add_subs(input_files):

    if len(input_files) != 2:
        script_exit("Please provide one video file and one sub file")

    video_formats = (".mp4", ".mov", ".mkv")
    sub_formats = (".stl", ".srt", ".sub")

    video_found = False
    subs_found = False
    for file in input_files:
        file_extension = os.path.splitext(file)[1]
        if file_extension.casefold() in video_formats:
            video = VideoFile(file)
            video_found = True
        if file_extension.casefold() in sub_formats:
            subs = file
            subs_found = True

    if video_found is False or subs_found is False:
        script_exit("Invalid combination of files provided")
    
    shutdown_bool = shutdown_choice()

    output_file = return_available_filename(video.path, "_SUBS.mkv")
    add_subs_ffmpeg_command(video.filepath, subs, output_file)

    if os.path.isfile(output_file):
        status = "Success"
    else:
        status = "Failed"
    
    output_file = {output_file: status}

    if shutdown_bool is True:
        shutdown()
    else:
        files_made(output_file)


def add_subs_ffmpeg_command(video_file, sub_file, output_file):
    os.system(f'ffmpeg -hide_banner -i "{video_file}" -i "{sub_file}" -map 0 -map 1 -c copy "{output_file}"')


def ffmpeg_command(input_files, menu_choice):
    banner(menu_choice.title)
    extra_option = menu_choice.get_extra_user_option()

    files_complete = {}
    shutdown_bool = shutdown_choice()

    for file in input_files:
        current_file = VideoFile(file)
        if "." in menu_choice.suffix_andor_ext:
            pass
        else:
            menu_choice.suffix_andor_ext = menu_choice.suffix_andor_ext + current_file.ext

        output_file = return_available_filename(current_file.path, menu_choice.suffix_andor_ext)

        menu_choice.command(input_file=current_file.filepath, output_file=output_file, extra_option=extra_option)


        # match menu_choice:
        #     case "dts_to_ac3":
        #         output_file = return_available_filename(current_file.path, "_AC3" + current_file.ext)
        #         dts_to_ac3_ffmpeg_command(current_file.filepath, output_file)
        #     case "h264_transcode":
        #         output_file = return_available_filename(current_file.path, ".mp4")
        #         h264_ffmpeg_command(current_file.filepath, output_file)
        #     case "h265_transcode":
        #         output_file = return_available_filename(current_file.path, ".mp4")
        #         h265_ffmpeg_command(current_file.filepath, output_file)
        #     case "h265_transcode_and_scale":
        #         output_file = return_available_filename(current_file.path, ".mp4")
        #         h265_and_scale_ffmpeg_command(current_file.filepath, output_file, extra_option)
        #     case "rewrap":
        #         output_file = return_available_filename(current_file.path, "." + extra_option)
        #         rewrap_ffmpeg_command(current_file.filepath, output_file)
        #     case _:
        #         script_exit("ERROR", ":/")

        if os.path.isfile(output_file):
            status = "Success"
        else:
            status = "Failed"
        files_complete[output_file] = status

    if shutdown_bool is True:
        shutdown()
    else:
        files_made(output_file)


def dts_to_ac3_ffmpeg_command(**kwargs):
    input_file = kwargs["input_file"]
    output_file = kwargs["output_file"]
    os.system(f'ffmpeg -i "{input_file}" -map 0 -vcodec copy -scodec copy -acodec ac3 -b:a 640k "{output_file}"')


def h264_ffmpeg_command(**kwargs):
    input_file = kwargs["input_file"]
    output_file = kwargs["output_file"]
    os.system(f'ffmpeg -i "{input_file}" -map 0 -map -0:d -vcodec libx264 -preset slower -crf 15 -acodec aac -b:a 380k "{output_file}"')
    input("")


def h265_ffmpeg_command(**kwargs):
    input_file = kwargs["input_file"]
    output_file = kwargs["output_file"]
    os.system(f'ffmpeg -i "{input_file}" -map 0 -map -0:d -vcodec libx265 -preset slow -crf 26 -acodec aac -b:a 380k "{output_file}"')


def h265_and_scale_ffmpeg_command(**kwargs):
    input_file = kwargs["input_file"]
    output_file = kwargs["output_file"]
    output_width = kwargs["extra_option"]
    os.system(f'ffmpeg -i "{input_file}" -vf scale={output_width}:-1 -map 0 -map -0:d -vcodec libx265 -preset slow -crf 26 -acodec copy "{output_file}"')


def rewrap_ffmpeg_command(**kwargs):
    input_file = kwargs["input_file"]
    output_file = kwargs["output_file"]
    os.system(f'ffmpeg -i "{input_file}" -map 0 -c copy "{output_file}"')


def main(input_files):

    main_menu = Menu()
    main_menu.display()
    menu_choice = main_menu.get_user_choice()
    ffmpeg_command(input_files, menu_choice)


    # banner("FFmpeg Tools", f"{version} Max Laurie")
    # print("1        Add Subs")
    # print("2        DTS to AC3")
    # print("3        Transcode to HQ H264")
    # print("4        Transcode to HQ H265")
    # print("5        Transcode to HQ H265 and scale")
    # print("6        Rewrap")
    # print("0        Exit")

    # while True:
    #     user_selection = input("\n- ")
    #     if user_selection.isnumeric() and int(user_selection) in range(0, 7):
    #         if int(user_selection) == 1:
    #             banner("Add Subs")
    #             add_subs(input_files)

    #         if int(user_selection) == 2:
    #             banner("DTS to AC3")
    #             ffmpeg_command(input_files, "dts_to_ac3")

    #         if int(user_selection) == 3:
    #             banner("H264 Transcode")
    #             ffmpeg_command(input_files, "h264_transcode")

    #         if int(user_selection) == 4:
    #             banner("H265 Transcode")
    #             ffmpeg_command(input_files, "h265_transcode")

    #         if int(user_selection) == 5:
    #             banner("H265 Scaled Transcode")
    #             output_width = input("Desired width of output files: ")
    #             ffmpeg_command(input_files, "h265_transcode_and_scale", output_width)

    #         if int(user_selection) == 6:
    #             banner("Rewrap")
    #             new_extension = input("New file wrapper: ")
    #             ffmpeg_command(input_files, "rewrap", new_extension)
                
    #         if int(user_selection) == 0:
    #             sys.exit()
    #     else:
    #         continue


if __name__ == "__main__":
    sys.argv.pop(0)
    if len(sys.argv) < 1:
        script_exit("Please provide at least one input file")
    main(sys.argv)
