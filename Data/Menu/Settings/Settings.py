import pygame
import pickle
import os
import Data.settings as default_settings


class Settings:
    def __init__(self, default_x=default_settings.DISPLAY_X, default_y=default_settings.DISPLAY_Y):
        self.res_x = default_x
        self.res_y = default_y
        self.fullscreen = False
        self.settings_file = 'Data/Menu/Data/SaveData/settings.pkl'

        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'rb') as f:
                data = pickle.load(f)
                self.fullscreen = data.get('fullscreen', False)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            infoObject = pygame.display.Info()
            self.res_x = infoObject.current_w
            self.res_y = infoObject.current_h
        else:
            self.res_x = default_settings.DISPLAY_X
            self.res_y = default_settings.DISPLAY_Y

        self.save_settings()

    def save_settings(self):
        with open(self.settings_file, 'wb') as f:
            pickle.dump({'fullscreen': self.fullscreen}, f)
