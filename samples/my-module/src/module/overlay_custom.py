"""Custom DrawFunc implementation."""

from savant.deepstream.drawfunc import NvDsDrawFunc
from savant.deepstream.meta.frame import NvDsFrameMeta
from savant.utils.artist import Artist
from savant.parameter_storage import param_storage
DETECTOR = param_storage()['detector']

class Overlay(NvDsDrawFunc):
    """Custom implementation of PyFunc for drawing on frame."""

    def draw_on_frame(self, frame_meta: NvDsFrameMeta, artist: Artist):
        """Draws on frame using the artist and the frame's metadata.

        :param frame_meta: Frame metadata.
        :param artist: Artist to draw on the frame.
        """
        # When the dev_mode is enabled in the module config
        # The draw func code changes are applied without restarting the module

        # super().draw_on_frame(frame_meta, artist)

        # for example, draw a white bounding box around persons
        # and a green bounding box around faces
        print("WE IN OVERLAY")
        print(frame_meta.frame_meta)
        # print(frame_meta.objects)
        for obj in frame_meta.objects:
            kp_attr = obj.get_attr_meta(DETECTOR, 'keypoints')
            print(obj.get_attr_meta(DETECTOR, 'keypoints'))
            if kp_attr is None:
                continue

            key_points = kp_attr.value
            print(key_points.shape)

            for pt in key_points:
                artist.add_circle(
                    center=(int(pt[0]), int(pt[1])),
                    radius=2,
                    color=(255, 0, 0, 255),
                    thickness=2,
                )
