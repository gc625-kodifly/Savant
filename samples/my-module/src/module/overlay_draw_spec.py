"""Custom DrawFunc implementation."""

from savant_rs.draw_spec import BoundingBoxDraw, ColorDraw, ObjectDraw, PaddingDraw
from savant.utils.artist import Artist
from savant.deepstream.drawfunc import NvDsDrawFunc
from savant.deepstream.meta.frame import NvDsFrameMeta
from savant.meta.object import ObjectMeta


KP_CONFIDENCE_THRESHOLD = 0.4

class Overlay(NvDsDrawFunc):
    """Custom implementation of PyFunc for drawing on frame."""
def draw_on_frame(self, frame_meta: NvDsFrameMeta, artist: Artist):
        # uncomment the following line to draw bounding boxes
        # super().draw_on_frame(frame_meta, artist)
        for obj in frame_meta.objects:
            if obj.label != 'person':
                continue

            
            

            for pair, color in skeleton:
                if (
                    key_points[pair[0]][2] > KP_CONFIDENCE_THRESHOLD
                    and key_points[pair[1]][2] > KP_CONFIDENCE_THRESHOLD
                ):
                    artist.add_line(
                        pt1=(
                            int(key_points[pair[0]][0]),
                            int(key_points[pair[0]][1]),
                        ),
                        pt2=(
                            int(key_points[pair[1]][0]),
                            int(key_points[pair[1]][1]),
                        ),
                        color=color,
                        thickness=2,
                    )
            for i, (x, y, conf) in enumerate(key_points):
                if conf > KP_CONFIDENCE_THRESHOLD:
                    artist.add_circle(
                        center=(int(x), int(y)),
                        radius=2,
                        color=(255, 0, 0, 255),
                        thickness=2,
                    )
                    # show label
                    # artist.add_text(
                    #     text=KP_LABELS[i],
                    #     anchor=(int(key_point[0]), int(key_point[1])),
                    # )

    # def override_draw_spec(
    #     self, object_meta: ObjectMeta, draw_spec: ObjectDraw
    # ) -> ObjectDraw:
    #     """Override draw spec for objects."""
    #     # When the dev_mode is enabled in the module config
    #     # The draw func code changes are applied without restarting the module

    #     if object_meta.label == 'person':
    #         # For example, change the border color of the bounding box
    #         # by specifying the new RGBA color in the draw spec
    #         bbox_draw = BoundingBoxDraw(
    #             border_color=ColorDraw(255, 255, 255, 255),
    #             background_color=ColorDraw(0, 0, 0, 0),
    #             thickness=1,
    #             padding=PaddingDraw(),
    #         )

    #         draw_spec = ObjectDraw(
    #             bounding_box=bbox_draw,
    #             label=draw_spec.label,
    #             central_dot=draw_spec.central_dot,
    #             blur=draw_spec.blur,
    #         )

    #     elif object_meta.label == 'face':
    #         # For example, switch face blur on or off
    #         draw_spec = ObjectDraw(
    #             bounding_box=draw_spec.bounding_box,
    #             label=draw_spec.label,
    #             central_dot=draw_spec.central_dot,
    #             blur=True,
    #         )
    #     return draw_spec
