from typing import Dict, List, NamedTuple
from savant.deepstream.pyfunc import NvDsPyFuncPlugin
from savant.deepstream.meta.frame import NvDsFrameMeta
from savant.deepstream.auxiliary_stream import AuxiliaryStream
from savant.deepstream.opencv_utils import nvds_to_gpu_mat
from savant.meta.object import ObjectMeta
from savant.parameter_storage import param_storage

DETECTOR = param_storage()['detector']

class BirdsEyeClipper(NvDsPyFuncPlugin):
    """
    A simple pyfunc that checks whether a frame meets our condition 
    (e.g., 'birds-eye view' camera angle). If so, we rename the frame's source_id 
    to something unique so that the 'video-files' sink writes a new clip.
    Otherwise, rename to 'discard'.
    """

    def __init__(self, 
                 codec_params: Dict,
                 **kwargs):
        super().__init__(**kwargs)
        # Keep track of a numeric ID for each new clip.
        self.clip_id = 0
        # Keep track if we're “in” a birds-eye segment or not.
        self.active = False
        self.frame_count = 0
        self.codec_params = codec_params
        self.clip_id = 0

    def process_frame(self, buffer, frame_meta: NvDsFrameMeta):

        # if not recording and condition is met, start recording
        
        if not self.active and self.check_birds_eye_condition(frame_meta):
            self.active = True
            self.clip_id += 1
            # create new auxiliary stream
            self.aux_stream = self.auxiliary_stream(
                source_id=f"birds_eye_{self.clip_id}",
                width=1280,
                height=720,
                codec_params=self.codec_params,
            )
            print(f"Starting new clip: {self.clip_id}")

        elif self.active and not self.check_birds_eye_condition(frame_meta):
            self.active = False
            print(f"Ending clip: {self.clip_id}")
            self.aux_stream.eos()

        if self.active:
            stream = self.get_cuda_stream(frame_meta)
            with nvds_to_gpu_mat(buffer, frame_meta.frame_meta) as frame_mat:
                
                aux_frame, aux_buffer = self.aux_stream.create_frame(
                    pts=frame_meta.pts,
                    duration=frame_meta.duration
                )
                with nvds_to_gpu_mat(aux_buffer,batch_id=0) as aux_mat:
                    width = 1280
                    left_roi = aux_mat.colRange(0, width)
                    # right_roi = aux_mat.colRange(width, combined_width)

                    frame_mat.clone().copyTo(left_roi)

        # Example condition: every N frames, we end the current “clip.”
        # self.frame_count += 1
        # if self.frame_count % 300 == 0:
        #     # Suppose every 300 frames => new clip
        #     # Post an EOS event for this source
        #     self.post_source_eos(frame_meta.source_id)

    def check_birds_eye_condition(self, frame_meta):
        """
        Dummy code for your real condition. Possibly you found an object 
        'camera_angle=topdown' or do some geometry check, etc.
        """
        # Just a placeholder:
        # print("Checking for birds-eye view...")
        
        return list(frame_meta.objects)[0]\
            .get_attr_meta(DETECTOR, 'keypoints').value.shape[0] > 12 



         