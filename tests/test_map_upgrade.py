import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image
from map_catalog import ALL_LAYOUTS
from setup_maps import install_recognition


class MapUpgradeTests(unittest.TestCase):
    def test_upgrade_preserves_existing_maps_and_adds_every_difficulty_and_outdoor_reference(self):
        image=io.BytesIO();Image.new('RGB',(32,32),(100,100,100)).save(image,format='WEBP')
        with tempfile.TemporaryDirectory() as folder,patch('setup_maps.fetch',return_value=image.getvalue()):
            path=Path(folder)
            old=b'existing-reference';(path/'map-32.webp').write_bytes(old)
            install_recognition(path,progress=lambda message:None)
            self.assertEqual((path/'map-32.webp').read_bytes(),old)
            self.assertEqual((path/'outdoor-minimap.webp').read_bytes(),image.getvalue())
            self.assertTrue(all((path/f'map-{layout}.webp').is_file() for layout in ALL_LAYOUTS))

    def test_expanded_layouts_use_matching_floor_renders_without_moaniimo_references(self):
        def download(url):
            if '/sanctum_61.webp' in url or '/sanctum_62.webp' in url:
                raise AssertionError('These references are not published by MOANIIMO')
            return b'floor-render' if '/200' in url else b'existing-source'
        with tempfile.TemporaryDirectory() as folder, patch('setup_maps.fetch', side_effect=download):
            path=Path(folder)
            (path/'map-61.webp').write_bytes(b'old-mismatched-crop')
            install_recognition(path,progress=lambda message:None)
            for layout in (31,33,38,61,62):
                self.assertEqual((path/f'map-{layout}.webp').read_bytes(),b'floor-render')
