# Some image augmentation tools for yolov5

## pip install tools4yolo 

#### Tested against Windows 10 / Python 3.10 / Anaconda 

```python
# instally Pytorch
# install https://github.com/ultralytics/yolov5
# install https://pypi.org/project/rembg/

# How preprocess the images:

from tools4yolo import remove_background_and_resize

remove_background_and_resize(
    folder=r"C:\Users\hansc\Downloads\metallicalogo",
    folderout=r"C:\Users\hansc\Downloads\metallicalogonobackground",
    maxwidth=640,
    maxheight=640,
)

# How to generate images and train them:
from tools4yolo import start_yolov5_training

if __name__ == "__main__": # necessary - multiprocessing
    start_yolov5_training(

        cfgfile=r"C:\classconfig.ini",
        ptfile=r"C:\Users\Gamer\anaconda3\envs\dfdir\yolov5\yolov5m.pt",
        generate_images=True,
        train_model=True,
        model_file="yolov5m.yaml",
        hypfile="hyp.scratch-low.yaml",
        batch=15,
        epochs=50,
        workers=5,
        save_period=3,
        cache="disk",
    )

# Example of classconfig.ini - all otpions have to be declared for each class
r"""
[class1]
classnumber:0
classname:acdc
random_background_folder:C:\Users\hansc\Downloads\Backgrounds
class_pictures:C:\musicmodel\acdc
personal_yaml_file:acdocmodelnew.yaml
outputfolder:c:\acdocmodelnew
howmany:5000
background_qty:500
processes:4
image_size_width:640
image_size_height:640
needle_size_percentage_min:0.4
needle_size_percentage_max:0.8
blur_image_kernel_min:3
blur_image_kernel_max:10
blur_image_frequency:30
sharpen_image_kernel_min:3
sharpen_image_kernel_max:15
sharpen_image_frequency:30
distorted_resizing_add_min_x:0.01
distorted_resizing_add_max_x:0.2
distorted_resizing_add_min_y:0.01
distorted_resizing_add_max_y:0.2
distorted_resizing_frequency:30
blur_borders_min_x0:0.01
blur_borders_max_x0:0.15
blur_borders_min_x1:0.01
blur_borders_max_x1:0.15
blur_borders_min_y0:0.01
blur_borders_max_y0:0.15
blur_borders_min_y1:0.01
blur_borders_max_y1:0.15
blur_borders_kernel_min:5
blur_borders_kernel_max:10
blur_borders_frequency:30
pixelborder_min:1
pixelborder_max:30
pixelborder_loop_min:1
pixelborder_loop_max:2
pixelborder_frequency:30
perspective_distortion_min_x:0.01
perspective_distortion_max_x:0.15
perspective_distortion_min_y:0.01
perspective_distortion_max_y:0.15
perspective_distortion_percentage:30
transparency_distortion_min:200
transparency_distortion_max:255
transparency_distortion_frequency:30
canny_edge_blur_thresh_lower_min:10
canny_edge_blur_thresh_lower_max:20
canny_edge_blur_thresh_upper_min:80
canny_edge_blur_thresh_upper_max:90
canny_edge_blur_kernel_min:3
canny_edge_blur_kernel_max:20
canny_edge_blur_frequency:30
random_crop_min_x:0.01
random_crop_max_x:0.2
random_crop_min_y:0.01
random_crop_max_y:0.2
random_crop_frequency:30
hue_shift_min:1
hue_shift_max:120
hue_shift_frequency:30
change_contrast_min:0.1
change_contrast_max:2.5
change_contrast_frequency:30
rotate_image_min:2
rotate_image_max:359
rotate_image_frequency:30
colors_to_change_percentage_max:10
colors_to_change_percentage_min:5
colors_to_change_frequency:30
colors_to_change_r_min:20
colors_to_change_r_max:200
colors_to_change_g_min:20
colors_to_change_g_max:200
colors_to_change_b_min:20
colors_to_change_b_max:200
flip_image_left_right_frequency:5
flip_image_up_down_frequency:5
verbose:True

[class2]
classnumber:1
classname:metallica
random_background_folder:C:\Users\hansc\Downloads\Backgrounds
class_pictures:C:\musicmodel\metallica
personal_yaml_file:acdocmodelnew.yaml
outputfolder:c:\acdocmodelnew
howmany:5000
background_qty:50
processes:4
image_size_width:640
image_size_height:640
needle_size_percentage_min:0.3
needle_size_percentage_max:0.8
blur_image_kernel_min:3
blur_image_kernel_max:10
blur_image_frequency:30
sharpen_image_kernel_min:3
sharpen_image_kernel_max:15
sharpen_image_frequency:30
distorted_resizing_add_min_x:0.01
distorted_resizing_add_max_x:0.2
distorted_resizing_add_min_y:0.1
distorted_resizing_add_max_y:0.2
distorted_resizing_frequency:30
blur_borders_min_x0:0.01
blur_borders_max_x0:0.15
blur_borders_min_x1:0.01
blur_borders_max_x1:0.15
blur_borders_min_y0:0.01
blur_borders_max_y0:0.15
blur_borders_min_y1:0.01
blur_borders_max_y1:0.15
blur_borders_kernel_min:5
blur_borders_kernel_max:10
blur_borders_frequency:30
pixelborder_min:1
pixelborder_max:30
pixelborder_loop_min:1
pixelborder_loop_max:2
pixelborder_frequency:30
perspective_distortion_min_x:0.01
perspective_distortion_max_x:0.2
perspective_distortion_min_y:0.01
perspective_distortion_max_y:0.2
perspective_distortion_percentage:30
transparency_distortion_min:100
transparency_distortion_max:255
transparency_distortion_frequency:30
canny_edge_blur_thresh_lower_min:10
canny_edge_blur_thresh_lower_max:20
canny_edge_blur_thresh_upper_min:80
canny_edge_blur_thresh_upper_max:90
canny_edge_blur_kernel_min:3
canny_edge_blur_kernel_max:20
canny_edge_blur_frequency:30
random_crop_min_x:0.01
random_crop_max_x:0.2
random_crop_min_y:0.01
random_crop_max_y:0.2
random_crop_frequency:30
hue_shift_min:1
hue_shift_max:120
hue_shift_frequency:30
change_contrast_min:0.1
change_contrast_max:2.5
change_contrast_frequency:30
rotate_image_min:2
rotate_image_max:359
rotate_image_frequency:30
colors_to_change_percentage_max:60
colors_to_change_percentage_min:10
colors_to_change_frequency:30
colors_to_change_r_min:20
colors_to_change_r_max:200
colors_to_change_g_min:20
colors_to_change_g_max:200
colors_to_change_b_min:20
colors_to_change_b_max:200
flip_image_left_right_frequency:5
flip_image_up_down_frequency:5
verbose:True

"""


# How to use the trained model: ##########################################

from tools4yolo import Yolov5Detect

ptfile = [r"C:\acdocmodelnew\dataset\splitset\acdocmodelnew4\weights\best.pt"]

yv = Yolov5Detect(
    modelfiles=ptfile, repo_or_dir="./yolov5", model="custom", source="local"
)
li = yv.detect(
    images=[
        r"C:\Users\hansc\Desktop\moha.png",
        r"C:\Users\hansc\Desktop\bax.png",
        r"C:\Users\hansc\Desktop\acada.png",
        r"C:\Users\hansc\Desktop\ba.png",
        r"C:\Users\hansc\Desktop\baxxxx.png",
        r"C:\Users\hansc\Desktop\bild.png",
        r"C:\Users\hansc\Downloads\highwa.jpg",
        r"C:\Users\hansc\Desktop\meta.png",
        r"C:\Users\hansc\Desktop\acd.png",
        r"C:\Users\hansc\Desktop\xxx.png",
    ],
    confidence_thresh=0.01,
    bgr_to_rgb=False,
    draw_output=True,
    save_folder="c:\\outputfolderyolo3v",
)

```