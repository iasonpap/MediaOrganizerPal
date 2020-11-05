import os, re, time
import logging
import utilities as ut

# Setting up logging info 
##################################
logger = logging.getLogger(__name__)
# create handler
io_stream_h = logging.StreamHandler()
file_h = logging.FileHandler("organiser.log")
# level and format
io_stream_h.setLevel(logging.INFO)
file_h.setLevel(logging.DEBUG)
# setting up the format for the log file and the console logging in real time
io_stream_formatter = logging.Formatter('[%(name)s:%(lineno)s - %(funcName)20s() ]:%(levelname)s: %(message)s')
file_formatter = logging.Formatter('%(asctime)s - [%(filename)s:%(lineno)s - %(funcName)15s() ] - %(levelname)s - %(message)s')
io_stream_h.setFormatter(io_stream_formatter)
file_h.setFormatter(file_formatter)
######################################################
# SUPPORTED FILE TYPES. To add more types, just edit this directory 
types_of_files = {"IMAGES":[".jpg",".jpeg",".png",".tiff"],
				"VIDEOS":[".mov",".gif",".avi",".mp4",".flv",".3gp",".3g2",".webm"]}
# snippet of code to check if ALL the extensions on the above directory start with a dot.
right_pattern_for_ext = r"\.\w+"
for key in types_of_files.keys():
	for item in types_of_files[key]:
		if not re.match(right_pattern_for_ext,item):
			logger.debug(f"Extension {item} is not correct. Correcting...")
			types_of_files[key]=f".{item}"

def FindFileInDir(dir_path):
	# Given a directory, walks through it to find all types of the files 
	# inside the directory  
	# Input: 	dir_path: path to the directory
	# Output:	files_in_working_dir: a list that contains all paths to the files in the dir_path
	###################################################
	files_found=[]
	logger.info(f"Finding all the files in directory {dir_path}")
	for dirs,_,files in os.walk(dir_path):
		files_found += [os.path.join(dirs,file) for file in files]
	return files_found

def OrganiseByType(working_dir,output_dir):
	# Organises the photos in the photos directory given by their type (images,videos)
	# Input:    working_dir: the directory where the photos to be organised are
	#           output_dir: the directory where the folders containing the seperate files will go
	#####################################
	
	####################################################
	images_dir = os.path.join(output_dir,"IMAGES")
	videos_dir = os.path.join(output_dir,"VIDEOS")
	
	# create the output directory or delete every file that already exists in the photo directory from the output directory
	files_in_working_dir = FindFileInDir(working_dir)
	if not os.path.isdir(output_dir):
		logger.info(f"Dir:{output_dir} DOESN'T EXIST. Creating it...")
		os.mkdir(output_dir)
	else: 
		logging.info(f"Dir:{output_dir} Already exists. Deleting any copies existing in it...")
		files_in_output_dir = FindFileInDir(output_dir)

		for file in files_in_output_dir:
			if file in files_in_working_dir:
				os.remove(file)
		
	# creating the images folder
	if not os.path.isdir(images_dir):
		os.mkdir(images_dir)
	# creating the videos folder
	if not os.path.isdir(videos_dir):
		os.mkdir(videos_dir)

	for dirs,_,files in os.walk(working_dir):
		for file in files:
			file_ext = os.path.splitext(file)[1]
			if file_ext in types_of_files["IMAGES"]:
				logger.info(f"Copying image {file} from {dir} to {images_dir}")
				old_file_dir = os.path.join(dirs,file)
				new_file_dir = os.path.join(images_dir,file)
				os.system(f"copy {old_file_dir} {new_file_dir}")
			else:
				logger.error(f"~!~!~!~~ File {file} is of type that is not supported as an IMAGE")
			if file_ext in types_of_files["VIDEOS"]:
				logger.info(f"Copying Video {file} from {dir} to {videos_dir}")
				old_file_dir = os.path.join(dirs,file)
				new_file_dir = os.path.join(videos_dir,file)
				os.system(f"copy {old_file_dir} {new_file_dir}")
			else:
				logger.error(f"~!~!~!~~ File {file} is of type that is not supported as a VIDEO")

def OrganiseByDate(working_dir,output_dir):
	# Year, Month, Day, Hour, Mins, Secs, _* = time.localtime(os.path.getmtime(path_to_file))
	# gives the date of the time that the photo was taken
	# TODO: 1)  make this function
	#       2)  create logs for this function
	#       3)  use int2string to turn single digits to double digits with zero in front. 
	#           e.g. int:5 -> string:"05"
	import calendar 
	# calendar.month_name :An array that represents the months of the year in the current locale. 
	#                      This follows normal convention of January being month number 1, 
	#                      so it has a length of 13 and month_name[0] is the empty string.
	# create the output directory or delete every file that already exists in the photo directory from the output directory
	
	files_in_working_dir = FindFileInDir(working_dir)
	if not os.path.isdir(output_dir):
		logger.info(f"Dir:{output_dir} DOESN'T EXIST. Creating it...")
		os.mkdir(output_dir)
	else: 
		logging.info(f"Dir:{output_dir} Already exists. \n\tDeleting any copies of files to be copied existing in it...")
		files_in_output_dir = FindFileInDir(output_dir)

		for file in files_in_output_dir:
			if file in files_in_working_dir:
				os.remove(file)
				
	
	logger.debug(files_in_working_dir)
	#iterating through all the files that we want to organise
	for old_file_full_path in files_in_working_dir:
		# getting the modified time of the file, which is the time that it was created 
		# (at least that is what I found for the photo files I checked)
		year, month, day, hour, mins, secs, *_ = time.localtime(os.path.getmtime(old_file_full_path))
		# getting the month name from the month number 
		month_name = calendar.month_name[month]
		# making the format for the directories in the form: <year>_<name_of_month> i.g. 2020_November
		year_month_str = f"{year}_{month_name}"
		# Creating the directory with the above name if it doesn't exist
		if not os.path.isdir(os.path.join(output_dir, year_month_str)):
			os.mkdir(os.path.join(output_dir, year_month_str))
		# turning the integers of the date for the file into strings with 0 in front if they are single-digits
		month_str = ut.int2string(month)
		day_str = ut.int2string(day)
		hour_str = ut.int2string(hour)
		mins_str = ut.int2string(mins)
		secs_str = ut.int2string(secs)
		# copying the file with new name base on the time of its creation
		logger.info(f"Copying {file} from {working_dir} to {output_dir}")	
		old_filename, ext = os.path.splitext(os.path.basename(old_file_full_path))
		new_file_basename = f"{year}-{month_str}-{day_str}-{hour_str}:{mins_str}:{secs_str}{ext}"
		new_file_dir = os.path.join(output_dir,year_month_str,new_file_basename)
		os.system(f"copy {old_file_full_path} {new_file_dir}")

			

	

