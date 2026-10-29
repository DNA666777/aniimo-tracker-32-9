import tempfile
import unittest
from unittest.mock import patch
from app import App


class FloatingOverlayTests(unittest.TestCase):
    def test_fresh_install_starts_with_overlay_disabled(self):
        with tempfile.TemporaryDirectory() as directory, patch('sanctum_panel.game_is_foreground', return_value=False):
            app = App(directory, hotkeys=False)
            try:
                self.assertFalse(app.sanctum.overlay_enabled.get())
                app.begin_run(without_balance=True)
                app.sanctum.always_status.set(True)
                app.busy_capture=True
                app.sanctum.tick()
                self.assertFalse(app.sanctum.overlay.visible)
            finally:
                app.close()

    def test_floating_bar_survives_missing_game_and_keeps_its_position(self):
        with tempfile.TemporaryDirectory() as directory, patch('sanctum_panel.game_is_foreground', return_value=False):
            app = App(directory, hotkeys=False)
            try:
                panel = app.sanctum
                panel.overlay_enabled.set(True)
                panel.always_status.set(True)
                panel.overlay_size.set(350)
                panel.config['overlay_position'] = [80, 100]
                app.busy_capture = True
                with patch('sanctum_panel.monitors', return_value=[dict(bbox=(0,0,1920,1080),primary=True)]), patch('sanctum_panel.capture_bounds', side_effect=ValueError('Game not found')):
                    panel.tick()
                    self.assertTrue(panel.overlay.visible)
                    self.assertEqual(panel.overlay.position, (80,100))
                with patch('sanctum_panel.capture_bounds', side_effect=[(100,100,1380,820),(300,180,1580,900)]):
                    panel.capture_geometry()
                    panel.capture_geometry()
                self.assertEqual(panel.overlay.position, (80,100))
                panel.overlay_enabled.set(False)
                panel.preview_overlay.set(True)
                panel.tick()
                self.assertFalse(panel.overlay.visible)
            finally:
                app.close()

    def test_placement_and_visibility_preferences_survive_restart(self):
        with tempfile.TemporaryDirectory() as directory, patch('sanctum_panel.game_is_foreground', return_value=False):
            app = App(directory, hotkeys=False)
            try:
                panel = app.sanctum
                self.assertEqual(panel.overlay_mode.get(), 'floating')
                panel.overlay_mode.set('follow_game')
                panel.overlay_enabled.set(True)
                panel.always_status.set(True)
                panel.save_preferences()
                panel.tick()
                self.assertFalse(panel.overlay.visible)
            finally:
                app.close()
            reopened = App(directory, hotkeys=False)
            try:
                self.assertEqual(reopened.sanctum.overlay_mode.get(), 'follow_game')
                self.assertTrue(reopened.sanctum.overlay_enabled.get())
            finally:
                reopened.close()
