import unittest
import tempfile
import os
import json
from cv2 import imread, imwrite
import numpy as np
import sys
import csv

SRC_DIR = os.path.dirname(os.path.abspath("./src/utils.py"))
print(SRC_DIR)
sys.path.append(SRC_DIR)
import utils


class TestUtils(unittest.TestCase):
    def test_save_new_annotations_file(self):
        output_filepath = tempfile.mkstemp()[1]
        data = {"test": [0, 1, 5, 4]}
        try:
            utils.save_new_annotations_file(output_filepath, data)
            with open(output_filepath + "annotations.json") as json_file:
                result = json.load(json_file)
        finally:
            os.remove(output_filepath)
        self.assertEqual(result, data)

    def test_get_image_and_info(self):
        test_image = np.array([[[1, 2, 3], [2, 3, 4]], [[3, 4, 5], [4, 5, 6]]])
        image_filepath = tempfile.mkstemp(suffix=".png")[1]
        try:
            imwrite(image_filepath, test_image)
            image, image_width, image_height = utils.get_image_and_info(image_filepath)
        finally:
            os.remove(image_filepath)
        self.assertEqual(image.all(), test_image.all())
        self.assertEqual((image_width, image_height), (2, 2))

    def test_get_altitude(self):
        fake_data = [
            {
                "image_name": "fakename",
                "header1": 5,
                "header2": 10,
                "header3": 48,
                "header4": 23,
                "header5": 0,
                "header6": 1,
                "header7": 7,
                "header8": 3,
                "header9": 4,
                "header10": 1,
                "header11": "6.5"
            }
        ]
        output_filepath = tempfile.mkstemp(suffix=".csv")[1]
        try:
            with open(output_filepath, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fake_data[0].keys())
                writer.writeheader()
                for data in fake_data:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
        altitude = utils.get_altitude("fakename", output_filepath)
        self.assertEqual(altitude, "6.5")


if __name__ == "__main__":
    unittest.main()
