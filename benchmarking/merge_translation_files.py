import os

# Directory containing .txt files
txt_dir = 'translate-xl8-th'

# Output file path
output_file = 'translate-xl8-th/merged_translation.txt'

# List of .txt files in the order to be merged
txt_files = [
    'audio_0.txt',
    'audio_1.txt',
    'audio_2.txt',
    'audio_3.txt',
    'audio_4.txt',
    'audio_5.txt',
    'audio_6.txt',
    'audio_7.txt',
    'audio_8.txt',
    'audio_9.txt',
    'audio_10.txt',
    'audio_11.txt'
]

# Open the output file in write mode
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Loop through the .txt files and concatenate their contents
    for file in txt_files:
        file_path = os.path.join(txt_dir, file)
        with open(file_path, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
            outfile.write(' ')  # Add a newline between files

print(f"All .txt files have been merged into {output_file}")
