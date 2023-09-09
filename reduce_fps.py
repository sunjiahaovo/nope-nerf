import os
import numpy as np
import shutil
import glob

# reduce fps in data
def reduce_fps(image_path, scene, reduce_rate):
    # load the data
    image_data = glob.glob(os.path.join(image_path, scene, "images/*.jpg"))
    depth_data = glob.glob(os.path.join(image_path, scene, "dpt/*.png"))
    depth_npz_data = glob.glob(os.path.join(image_path, scene, "dpt/*.npz"))
    image_list = sorted([os.path.basename(image) for image in image_data])
    depth_list = sorted([os.path.basename(depth) for depth in depth_data])
    depth_npz_list = sorted([os.path.basename(depth) for depth in depth_npz_data])

    # reduce image_list lenth to target
    image_list = image_list[::reduce_rate]
    depth_list = depth_list[::reduce_rate]
    depth_npz_list = depth_npz_list[::reduce_rate]
    
    # copy the image to new folder
    reduce_image_path = os.path.join(image_path, scene+"_{:03d}".format(reduce_rate), "images")
    reduce_depth_path = os.path.join(image_path, scene+"_{:03d}".format(reduce_rate), "dpt")
    if not os.path.exists(reduce_image_path):
        os.makedirs(reduce_image_path)
    if not os.path.exists(reduce_depth_path):
        os.makedirs(reduce_depth_path)
    for image in image_list:
        shutil.copy(os.path.join(image_path, scene, "images", image), reduce_image_path)
    for depth in depth_list:
        shutil.copy(os.path.join(image_path, scene, "dpt", depth), reduce_depth_path)
    for depth_npz in depth_npz_list:
        shutil.copy(os.path.join(image_path, scene, "dpt", depth_npz), reduce_depth_path)
    
    # reduce poses
    poses = np.load(os.path.join(image_path, scene, "poses_bounds.npy"))
    poses = poses[::reduce_rate]
    np.save(os.path.join(image_path, scene+"_{:03d}".format(reduce_rate), "poses_bounds.npy"), poses)  
    

if __name__ == '__main__':
    image_path = "data/Tanks"
    scene = "Ignatius"
    reduce_rate = 9
    reduce_fps(image_path = image_path, scene = scene, reduce_rate = reduce_rate)