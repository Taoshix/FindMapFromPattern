import os
import io
import zipfile
from datetime import timedelta
from datetime import datetime

osu_directory = 'D:/Spil/osu!/Songs'
#osu_directory = 'D:/Downloads/2015(osu!)'
file_extension = '.osu'
leeway = 1

class HitObject:
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

def parse_reference_to_hitobjects(reference):
    hit_objects = []
    for comment in reference:
        parts = comment.strip().split(',')
        x = int(parts[0])
        y = int(parts[1])
        time = int(parts[2])
        hit_object = HitObject(x, y, time)
        hit_objects.append(hit_object)
    return hit_objects

def calculate_time_differences(hit_objects):
    time_differences = []
    for i in range(1, len(hit_objects)):
        time_differences.append(hit_objects[i].time - hit_objects[i-1].time)
    return time_differences

def traverse_files(directory, extension):
    osu_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                if file.endswith(extension):
                    osu_files.append(os.path.join(root, file))
                elif file.endswith('.osz'):
                    with zipfile.ZipFile(os.path.join(root, file), 'r') as zip_ref:
                        zip_ref.extractall(os.path.join(root, file[:-4]))
                        for extracted_file in os.listdir(os.path.join(root, file[:-4])):
                            if extracted_file.endswith(extension):
                                osu_files.append(os.path.join(root, file[:-4], extracted_file))
            except:
                print(f"Error reading file: {file}")
                continue
    return osu_files

def parse_hitobjects_from_file(file_path):
    hit_objects = []
    with io.open(file_path, 'r', encoding='utf-8') as f:
        try:
            lines = f.readlines()
            hit_objects_section = False 
            for line in lines:
                if line.strip() == '[HitObjects]':
                    hit_objects_section = True
                    continue
                if hit_objects_section:
                    try:
                        parts = line.strip().split(',')
                        x = int(parts[0])
                        y = int(parts[1])
                        time = int(parts[2])
                        hit_object = HitObject(x, y, time)
                        hit_objects.append(hit_object)
                    except:
                        continue
        except:
            print(f"Error parsing file: {file_path}")
    return hit_objects

def find_pattern_in_files(reference):
    print(f"Loading reference pattern with {len(reference)} hit objects...")
    print(f"Timing leeway: {leeway}ms")
    hit_objects_from_reference = parse_reference_to_hitobjects(reference)
    time_differences_from_reference = calculate_time_differences(hit_objects_from_reference)
    
    print(f"Loading all osu files in {osu_directory}...")
    osu_files = traverse_files(osu_directory, file_extension)
    print(f"Scanning {len(osu_files)} osu files for pattern...")
    start_time = datetime.now()
    for i, file_path in enumerate(osu_files):
        if i % 1000 == 0 and i > 0:
            current_time = datetime.now()
            elapsed_time = (current_time - start_time).total_seconds()
            files_per_second = i / elapsed_time
            print(f"Checked {i} maps... ({files_per_second:.2f} maps per second)")
        hit_objects_from_file = parse_hitobjects_from_file(file_path)
        if len(hit_objects_from_file) < len(hit_objects_from_reference):
            continue
        time_differences_from_file = calculate_time_differences(hit_objects_from_file)
        
        for start in range(len(time_differences_from_file) - len(time_differences_from_reference) + 1):
            if all(abs(tc - tf) <= leeway for tc, tf in zip(time_differences_from_reference, time_differences_from_file[start:start + len(time_differences_from_reference)])):
                match_start_time = hit_objects_from_file[start].time
                match_end_time = hit_objects_from_file[start + len(time_differences_from_reference)].time
                start_timestamp = str(timedelta(milliseconds=match_start_time))
                end_timestamp = str(timedelta(milliseconds=match_end_time))
                print(f"Match found in file: {file_path} from {start_timestamp} to {end_timestamp}")
                break
    
    end_time = datetime.now()
    total_elapsed_time = end_time - start_time
    total_seconds = total_elapsed_time.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{int(hours):02}:{int(minutes):02}:{seconds:05.2f}"
    print(f"Done Searching. Time taken: {formatted_time}")

# x, y, time, type, hit_sound, extras we dont care about
reference = [
    "297,189,162,5,0,0:0:0:0:",
    "297,189,243,1,0,0:0:0:0:",
    "297,189,324,1,0,0:0:0:0:",
    "334,159,486,1,0,0:0:0:0:",
    "357,131,648,5,0,0:0:0:0:",
    "357,131,810,1,0,0:0:0:0:",
    "277,137,972,2,0,L|361:183,1,70",
    "357,131,1297,1,0,0:0:0:0:",
    "357,131,1459,1,0,0:0:0:0:",
    "277,137,1621,2,0,L|350:175,1,70",
    "357,131,1945,1,0,0:0:0:0:",
    "376,107,2107,1,0,0:0:0:0:",
    "376,107,2270,1,0,0:0:0:0:",
    "376,107,2432,1,0,0:0:0:0:",
    "277,137,2594,2,0,L|356:177,1,70",
    "376,107,2918,1,0,0:0:0:0:",
    "376,107,3080,1,0,0:0:0:0:",
    "277,137,3243,2,0,L|369:180,1,70",
    "376,107,3567,1,0,0:0:0:0:",
    "389,104,3729,1,0,0:0:0:0:",
    "389,104,3810,1,0,0:0:0:0:",
    "389,104,3891,1,0,0:0:0:0:",
    "391,105,4053,1,0,0:0:0:0:",
    "277,137,4216,2,0,L|359:182,1,70",
    "277,137,4540,2,0,L|359:175,1,70",
    "420,109,4783,1,0,0:0:0:0:",
    "412,104,4864,1,0,0:0:0:0:",
    "420,109,5026,1,0,0:0:0:0:",
    "420,109,5189,1,0,0:0:0:0:",
    "420,109,5351,1,0,0:0:0:0:"
]


cut_reference = reference[:15]

middle_reference = reference[10:20]

find_pattern_in_files(reference)