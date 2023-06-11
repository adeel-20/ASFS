from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 1, 1),
}

dag = DAG('python_functions_dag', default_args=default_args, schedule_interval=None)


def unessecary():
    image_folder = "yolo_coco/train/images"
    text_folder = "yolo_coco/train/labels"

    # Get a set of existing image and text file names
    image_files = set(os.path.splitext(file)[0] for file in os.listdir(image_folder) if file.endswith(".jpg"))
    text_files = set(os.path.splitext(file)[0] for file in os.listdir(text_folder) if file.endswith(".txt"))

    # Find the image files without corresponding text files
    files_without_text = image_files - text_files

    # Delete the image files without corresponding text files
    for file_name in files_without_text:
        image_path = os.path.join(image_folder, file_name + ".jpg")
        os.remove(image_path)
        print(f"Deleted {file_name}.jpg as no corresponding text file found.")

def keep_specific():
    text_folder = "yolo_coco/train/labels"
    classes_to_keep = [1]

    # Get a list of text files
    text_files = os.listdir(text_folder)

    # Iterate over the text files
    for text_file in text_files:
        # Read the contents of the text file
        with open(os.path.join(text_folder, text_file), "r") as file:
            lines = file.readlines()

        # Check if any line contains a class to keep
        keep_file = any(any(int(line.split()[0]) == cls for cls in classes_to_keep) for line in lines)

        if not keep_file:
            # Delete the text file
            os.remove(os.path.join(text_folder, text_file))
            print(f"Deleted {text_file} as it does not contain the specified classes.")
        else:
            # Filter the lines to keep only the specified classes' annotations
            filtered_lines = [line for line in lines if int(line.split()[0]) in classes_to_keep]

            # Write the filtered lines back to the text file
            with open(os.path.join(text_folder, text_file), "w") as file:
                file.writelines(filtered_lines)
                print(f"Kept {text_file} and filtered the annotations to contain only the specified classes.")

def load_images_from_folder(folder):
  count = 0
  for filename in os.listdir(folder):
        source = os.path.join(folder,filename)
        destination = f"{output_path}images/img{count}.jpg"

        try:
            shutil.copy(source, destination)
            print("File copied successfully.")
        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        file_names.append(filename)
        count += 1

def get_img_ann(image_id):
    img_ann = []
    isFound = False
    for ann in data['annotations']:
        #print('img_id: ',image_id)
        if ann['image_id'] == image_id:
            img_ann.append(ann)
            isFound = True
    if isFound:
        return img_ann
    else:
        #print(isFound)
        return None
    

def get_img(filename):
  for img in data['images']:
    if img['file_name'] == filename:
      print('Hello')

with dag:
    t1 = PythonOperator(
        task_id='unessecary',
        python_callable=unessecary
    )

    t2 = PythonOperator(
        task_id='keep_specific',
        python_callable=keep_specific
    )

    t3 = PythonOperator(
        task_id='load_images_from_folder',
        python_callable=load_images_from_folder
    )

    t4 = PythonOperator(
        task_id='get_img_ann',
        python_callable=get_img_ann
    )

    t5 = PythonOperator(
        task_id='get_img',
        python_callable=get_img
    )

    t1 >> t2 >> t3 >> t4 >> t5