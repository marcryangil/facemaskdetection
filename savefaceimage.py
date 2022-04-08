import cv2
import math
import numpy as np
import os
import tensorflow
import time

from face_alignment import FaceMaskDetection
from tools import model_restore_from_pb

if tensorflow.__version__.startswith('1.'):
    import tensorflow as tf
else:
    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()
print("Tensorflow version: ",tf.__version__)

img_format = {'png','jpg','bmp'}

def video_init(camera_source=0,resolution="480",to_write=False,save_dir=None):
    '''

    :param camera_source:
    :param resolution: '480', '720', '1080'. Set None for videos.
    :param to_write: to record or not
    :param save_dir: the folder to save your recording
    :return: cap,height,width,writer
    '''
    #----var
    writer = None
    resolution_dict = {"480":[480,640],"720":[720,1280],"1080":[1080,1920]}

    #----camera source connection
    cap = cv2.VideoCapture(camera_source)

    #----resolution decision
    if resolution_dict.get(resolution) is not None:
    # if resolution in resolution_dict.keys():
        width = resolution_dict[resolution][1]
        height = resolution_dict[resolution][0]
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    else:
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)#default 480
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)#default 640
        print("video size is auto set")

    '''
    ref:https://docs.opencv.org/master/dd/d43/tutorial_py_video_display.html
    FourCC is a 4-byte code used to specify the video codec. 
    The list of available codes can be found in fourcc.org. 
    It is platform dependent. The following codecs work fine for me.
    In Fedora: DIVX, XVID, MJPG, X264, WMV1, WMV2. (XVID is more preferable. MJPG results in high size video. X264 gives very small size video)
    In Windows: DIVX (More to be tested and added)
    In OSX: MJPG (.mp4), DIVX (.avi), X264 (.mkv).
    FourCC code is passed as `cv.VideoWriter_fourcc('M','J','P','G')or cv.VideoWriter_fourcc(*'MJPG')` for MJPG.
    '''
    if to_write is True:
        #fourcc = cv2.VideoWriter_fourcc('x', 'v', 'i', 'd')
        #fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        save_path = 'demo.avi'
        if save_dir is not None:
            save_path = os.path.join(save_dir,save_path)
        writer = cv2.VideoWriter(save_path, fourcc, 30, (int(width), int(height)))

    return cap,height,width,writer

def stream(pb_path, node_dict,ref_dir,camera_source=0,resolution="480",to_write=False,save_dir=None):


    #----var
    frame_count = 0
    FPS = "loading"
    face_mask_model_path = r'face_mask_detection.pb'
    margin = 40
    id2class = {0: 'Mask', 1: 'NoMask'}
    batch_size = 32
    threshold = 0.8
    display_mode = 0
    label_type = 0

    #----Video streaming initialization
    cap,height,width,writer = video_init(camera_source=camera_source, resolution=resolution, to_write=to_write, save_dir=save_dir)

    # ----face detection init
    fmd = FaceMaskDetection(face_mask_model_path, margin, GPU_ratio=None)

    # ----face recognition init
    sess, tf_dict = model_restore_from_pb(pb_path, node_dict, GPU_ratio=None)
    tf_input = tf_dict['input']
    tf_embeddings = tf_dict['embeddings']

    #----get the model shape
    if tf_input.shape[1].value is None:
        model_shape = (None, 160, 160, 3)
    else:
        model_shape = (None, tf_input.shape[1].value, tf_input.shape[2].value, 3)
    print("The mode shape of face recognition:",model_shape)

    #----set the feed_dict
    feed_dict = dict()
    if 'keep_prob' in tf_dict.keys():
        tf_keep_prob = tf_dict['keep_prob']
        feed_dict[tf_keep_prob] = 1.0
    if 'phase_train' in tf_dict.keys():
        tf_phase_train = tf_dict['phase_train']
        feed_dict[tf_phase_train] = False

    #----read images from the database
    d_t = time.time()
    paths = list()
    for dirname, subdirname, filenames in os.walk(ref_dir):
        if len(filenames) > 0:
            for filename in filenames:
                if filename.split(".")[-1] in img_format:
                    file_path = os.path.join(dirname, filename)
                    paths.append(file_path)

    #     paths = [file.path for file in os.scandir(ref_dir) if file.name[-3:] in img_format]
    len_ref_path = len(paths)
    if len_ref_path == 0:
        print("No images in ", ref_dir)
    else:
        ites = math.ceil(len_ref_path / batch_size)
        embeddings_ref = np.zeros([len_ref_path, tf_embeddings.shape[-1]], dtype=np.float32)

        for i in range(ites):
            num_start = i * batch_size
            num_end = np.minimum(num_start + batch_size, len_ref_path)

            batch_data_dim =[num_end - num_start]
            batch_data_dim.extend(model_shape[1:])
            batch_data = np.zeros(batch_data_dim,dtype=np.float32)

            for idx,path in enumerate(paths[num_start:num_end]):
                # img = cv2.imread(path)
                img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), 1)
                if img is None:
                    print("read failed:",path)
                else:
                    #print("model_shape:",model_shape[1:3])
                    img = cv2.resize(img,(model_shape[2],model_shape[1]))
                    img = img[:,:,::-1]#change the color format
                    batch_data[idx] = img
            batch_data /= 255
            feed_dict[tf_input] = batch_data

            embeddings_ref[num_start:num_end] = sess.run(tf_embeddings,feed_dict=feed_dict)

        d_t = time.time() - d_t

        print("ref embedding shape",embeddings_ref.shape)
        print("It takes {} secs to get {} embeddings".format(d_t, len_ref_path))

    # ----tf setting for calculating distance
    if len_ref_path > 0:
        with tf.Graph().as_default():
            tf_tar = tf.placeholder(dtype=tf.float32, shape=tf_embeddings.shape[-1])
            tf_ref = tf.placeholder(dtype=tf.float32, shape=tf_embeddings.shape)
            tf_dis = tf.sqrt(tf.reduce_sum(tf.square(tf.subtract(tf_ref, tf_tar)), axis=1))
            # ----GPU setting
            config = tf.ConfigProto(log_device_placement=False,
                                    allow_soft_placement=True,
                                    )
            config.gpu_options.allow_growth = True
            sess_cal = tf.Session(config=config)
            sess_cal.run(tf.global_variables_initializer())

        feed_dict_2 = {tf_ref: embeddings_ref}


    #----Get an image
    while(cap.isOpened()):
        ret, img = cap.read()
        img_copy = img.copy()

        if ret is True:

            #----image processing
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_rgb = img_rgb.astype(np.float32)
            img_rgb /= 255

            #----face detection
            img_fd = cv2.resize(img_rgb, fmd.img_size)
            img_fd = np.expand_dims(img_fd, axis=0)

            bboxes, re_confidence, re_classes, re_mask_id = fmd.inference(img_fd, height, width)
            if len(bboxes) > 0:
                for num, bbox in enumerate(bboxes):
                    class_id = re_mask_id[num]
                    if class_id == 0:
                        color = (0, 255, 0)  # (B,G,R) --> Green(with masks)
                    else:
                        color = (0, 0, 255)  # (B,G,R) --> Red(without masks)

                    cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 2)

            #----image display
            cv2.namedWindow("UFMDS", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("UFMDS", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("UFMDS", img)

            #----image writing
            if writer is not None:
                writer.write(img)

            #----keys handle
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                if len(bboxes) > 0:
                    img_temp = img_copy[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2], :]
                    save_path = "img_crop.jpg"
                    save_path = os.path.join(ref_dir,save_path)
                    cv2.imwrite(save_path,img_temp)
                    print("An image is saved to ",save_path)
            if cv2.getWindowProperty("UFMDS", cv2.WND_PROP_VISIBLE) < 1:
                break

        else:
            print("get images failed")
            break

    #----release
    cap.release()
    cv2.destroyAllWindows()
    if writer is not None:
        writer.release()

def start():
    camera_source = 0
    pb_path = r"pb_model_select_num=15.pb"

    node_dict = {'input': 'input:0',
                 'keep_prob': 'keep_prob:0',
                 'phase_train': 'phase_train:0',
                 'embeddings': 'embeddings:0',
                 }
    ref_dir = r"C:\Users\gilma\Documents\UdemyThesis\test_database"

    stream(pb_path, node_dict, ref_dir, camera_source=camera_source, resolution="720", to_write=False, save_dir=None)
