import cv2 as cv
import ezdxf
import numpy as np
from ezdxf import units

series = [
    [(0, 1, 2, 3, 4), 4, 2]
]

for aruco_ids, marker_bits, marker_size_mm in series:
    for aruco_id in aruco_ids:
        field_size_mm = marker_size_mm / (marker_bits + 2)
        field_size_bits = marker_bits + 2

        doc = ezdxf.new()
        doc.units = units.MM
        # Set color for each layer.
        black_layer = doc.layers.add("black")
        black_layer.color = 0
        white_layer = doc.layers.add("white")
        white_layer.color = 255
        msp = doc.modelspace()

        aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_1000)
        marker = np.zeros((field_size_bits, field_size_bits, 1), dtype="uint8")
        cv.aruco.generateImageMarker(aruco_dict, aruco_id, field_size_bits, marker, 1)

        for row_idx, row in enumerate(reversed(marker)):
            row = row.flatten()
            for col_idx, col in enumerate(row):
                # Order for ezdxf solid is 1, 2, 4, 3.
                points = [
                    (col_idx * field_size_mm, row_idx * field_size_mm),
                    ((col_idx + 1) * field_size_mm, row_idx * field_size_mm),
                    (col_idx * field_size_mm, (row_idx + 1) * field_size_mm),
                    ((col_idx + 1) * field_size_mm, (row_idx + 1) * field_size_mm),
                ]
                # Get color by layer.
                if col == 0:
                    msp.add_solid(points, dxfattribs={"color": 256, "layer": "black"})

                # Check if white colored fields are needed for use case.
                # else:
                #    msp.add_solid(points, dxfattribs={"color": 256, "layer": "white"})

        doc.saveas(
            f"aruco_{marker_bits}x{marker_bits}_{marker_size_mm}_id-{aruco_id}.dxf"
        )
