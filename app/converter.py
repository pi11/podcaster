base_command = (
    f"ffmpeg -i {input_file} -c:a libopus -b:a 32k -application voip {output_file}"
)
