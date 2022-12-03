import os
from PIL import ImageFont

if os.name == "posix":
    font = "/System/Library/Fonts/Supplemental/Tahoma.ttf"
else:
    font = "c:/Windows/Fonts/cambria.ttc"

title_font = ImageFont.truetype(font, 70)
text_font = ImageFont.truetype(font, 65)
point_fnt = ImageFont.truetype(font, 32)

CARD_WIDTH = 800
TITLE_LOCATION = CARD_WIDTH / 2, 85

RESOURCE_TEXT_LOCATION = CARD_WIDTH / 2, 230
RESOURCE_LOCATION = 140, 260
RESOURCE_SIZE = 40
RESOURCE_X_MARGIN = 18
RESOURCE_Y_MARGIN = 15

RECTANGLE = 1
CIRCLE = 2

REWARD_TEXT_LOCATION = CARD_WIDTH / 2, 550
REWARDS_LOCATION = 140, 580
