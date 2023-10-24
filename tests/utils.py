import os
import os.path
import unittest

from PIL import Image

import imagehash

CHECK_HASH_DEFAULT = range(2, 21)
CHECK_HASH_SIZE_DEFAULT = range(-1, 2)


class TestImageHash(unittest.TestCase):
	@staticmethod
	def get_data_image(fname=None):
		if fname is None:
			fname = 'imagehash.png'
		dname = os.path.abspath(os.path.dirname(__file__))
		target = os.path.join(dname, 'data', fname)
		if not os.path.isfile(target):
			emsg = 'Unknown test image file: {!r}'
			raise ValueError(emsg.format(target))
		return Image.open(target)

	def check_hash_algorithm(self, func, image):
		original_hash = func(image)
		rotate_image = image.rotate(-1)
		rotate_hash = func(rotate_image)
		distance = original_hash - rotate_hash
		emsg = (f'slightly rotated image should have similar hash {original_hash} {rotate_hash} {distance}')
		self.assertTrue(distance <= 10, emsg)
		rotate_image = image.rotate(-90)
		rotate_hash = func(rotate_image)
		emsg = (f'rotated image should have different hash {original_hash} {rotate_hash}')
		self.assertNotEqual(original_hash, rotate_hash, emsg)
		distance = original_hash - rotate_hash
		emsg = (f'rotated image should have larger different hash {original_hash} {rotate_hash} {distance}')
		self.assertTrue(distance > 10, emsg)

	def check_hash_length(self, func, image, sizes=CHECK_HASH_DEFAULT):
		for hash_size in sizes:
			image_hash = func(image, hash_size=hash_size)
			emsg = f'hash_size={hash_size} is not respected'
			self.assertEqual(image_hash.hash.size, hash_size**2, emsg)

	def check_hash_stored(self, func, image, sizes=CHECK_HASH_DEFAULT):
		for hash_size in sizes:
			image_hash = func(image, hash_size)
			other_hash = imagehash.hex_to_hash(str(image_hash))
			emsg = f'stringified hash {other_hash} != original hash {image_hash}'
			self.assertEqual(image_hash, other_hash, emsg)
			distance = image_hash - other_hash
			emsg = (f'unexpected hamming distance {distance}: original hash {image_hash} - stringified hash {other_hash}')
			self.assertEqual(distance, 0, emsg)

	def check_hash_size(self, func, image, sizes=CHECK_HASH_SIZE_DEFAULT):
		for hash_size in sizes:
			with self.assertRaises(ValueError):
				func(image, hash_size)
