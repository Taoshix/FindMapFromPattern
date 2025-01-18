import os
import io
import zipfile
from datetime import timedelta
from datetime import datetime

osu_directory = os.path.join(os.getenv('APPDATA'), 'osu!/Songs')
#osu_directory = 'D:/Spil/osu!/Songs'
file_extension = '.osu'
leeway = 1

class HitObject:
    def __init__(self, x, y, time):
        self.x = x
        self.y = y
        self.time = time

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

def load_reference_from_file(file_path):
    return parse_hitobjects_from_file(file_path)

def find_pattern_in_files(reference):
    print(f"Loading reference pattern with {len(reference)} hit objects...")
    print(f"Timing leeway: {leeway}ms")
    time_differences_from_reference = calculate_time_differences(reference)
    
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
        if len(hit_objects_from_file) < len(reference):
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

# Load reference from file
reference_file_path = 'reference.osu'
reference_hit_objects = load_reference_from_file(reference_file_path)

find_pattern_in_files(reference_hit_objects)