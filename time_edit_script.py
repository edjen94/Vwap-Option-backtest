from datetime import time, timedelta, datetime
import csv
import os

input_dir = 'input'
output_dir = 'output'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

if not os.path.exists(input_dir):
    os.mkdir(input_dir)

for file in os.listdir(input_dir):
    with open(input_dir+'/'+file,'r', newline='') as f_in, open(output_dir+'/'+file,'w') as f_out:
        readfile = csv.reader(f_in)
        headings = next(readfile)
        for row in readfile:
            # split hour and minute
            split_values = row[2].split(":")
            hour = int(split_values[0])
            minute = int(split_values[1])
            
            # Get today datetime
            today_date = datetime.today()
            # Replace it with the hour minute we want
            modified_today_date = today_date.replace(hour=hour, minute=minute, second=00, microsecond=00)
            # one minute value
            one_minute = timedelta(minutes=1)
            date_time_value_deducted = modified_today_date - one_minute
            time_value_deducted = date_time_value_deducted.strftime("%H:%M")
            # replace the old time with updated time
            row[2] = time_value_deducted

            #write the output to new file
            output_writer = csv.writer(f_out)
            output_writer.writerow(row)

        print("Processed file: ", file)

print("Completed all!")

