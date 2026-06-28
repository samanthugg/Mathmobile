"""This module contains UI helper functions for drawing buttons and text"""
import math

import pygame


def draw_button(screen, rect, text, font):
    """Draw the button with hover effect and text.

    :param screen: pygame display surface
    :param rect: defines button position and size
    :param text: defines text
    :param font: defines font"""

    # check mouse position for hover animation
    mouse = pygame.mouse.get_pos()
    hover = rect.collidepoint(mouse)

    # adjust color and border thickness based on hover state
    color = 200 if hover else 100
    border = 3 if hover else 2

    # draw semi-transparent button background
    button = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    button.fill((0, 0, 0, color))
    screen.blit(button, rect.topleft)

    # draw button border with rounded corners
    pygame.draw.rect(screen, "white", rect, border, border_radius=8)

    # render text
    text_surface = font.render(text, True, "white")
    text_rect = text_surface.get_rect(center=rect.center)

    # shadow offset for text
    shadow = font.render(text, True, "black")
    screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
    screen.blit(text_surface, text_rect)


def draw_text_with_shadow(
        screen,
        text,
        font,
        position,
        color="white",
        shadow_color="black"):
    """Draw centered text with shadow effect.

    :param screen: pygame display surface
    :param text: defines text
    :param font: defines font
    :param position: defines position
    :param color: defines color
    :param shadow_color: defines shadow color"""
    text_surface = font.render(text, True, color)
    shadow_surface = font.render(text, True, shadow_color)

    # calculate center based on provided position
    rect = text_surface.get_rect(center=position)

    # blit shadow first (offset by 3px), then main text
    screen.blit(shadow_surface, (rect.x + 3, rect.y + 3))
    screen.blit(text_surface, rect)


def draw_title(screen, text, font, center_pos, colors=None, letter_width=None):
    """Draw rainbow title text with a soft glow.

    :param letter_width:
    :param colors:
    :param screen: pygame display surface
    :param text: title text to draw
    :param font: pygame font object
    :param center_pos: (x, y) center position for the full title
    """

    if colors is None:
        colors = [
            (255, 153, 204), (255, 204, 153), (255, 255, 153),
            (153, 255, 204), (153, 255, 255), (153, 204, 255), (204, 153, 255)
        ]

    # width used for spacing each letter
    if letter_width is None:
        letter_width = 42

    # total width of the whole title
    total_width = len(text) * letter_width

    # starting x so the full word is centered
    x_start = center_pos[0] - (total_width // 2)

    # y position for all letters
    y = center_pos[1]

    # draw one letter at a time
    for index, character in enumerate(text):
        # pick a color from the color list
        color = colors[index % len(colors)]

        # darker version of the color for the glow
        glow_color = (
            color[0] // 2,
            color[1] // 2,
            color[2] // 2
        )

        # render the main letter and glow letter
        letter_main = font.render(character, True, color)
        letter_glow = font.render(character, True, glow_color)

        # x position for this letter
        x = x_start + index * letter_width

        # draw glow first
        screen.blit(letter_glow, (x + 2, y + 2))
        screen.blit(letter_glow, (x - 2, y - 2))

        # draw main letter on top
        screen.blit(letter_main, (x, y))


def draw_button_text(
        screen, text, rect, font, normal_color=(
                220, 200, 110), hover_color=(
                255, 255, 255)):
    """Draw button text with shadow, outline, and hover effects including animated corner highlights.

    :param screen: pygame display surface
    :param text: text to render
    :param rect: rectangle defining position and alignment
    :param font: pygame font used to render text
    :param normal_color: default text color
    :param hover_color: text color when hovered
    """

    mouse = pygame.mouse.get_pos()
    hover = rect.collidepoint(mouse)

    color = hover_color if hover else normal_color
    t_surf = font.render(text, True, color)
    t_rect = t_surf.get_rect(center=rect.center)

    shadow = font.render(text, True, (0, 0, 0))
    screen.blit(shadow, (t_rect.x + 3.5, t_rect.y + 3.5))

    outline_color = (0, 0, 0)
    for x_offset, y_offset in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        outline_surface = font.render(text, True, outline_color)
        screen.blit(
            outline_surface,
            (t_rect.x + x_offset,
             t_rect.y + y_offset))

    screen.blit(t_surf, t_rect)

    # hover effect
    if hover:
        rainbow_color = get_rainbow_color()
        draw_corners(screen, t_rect, rainbow_color)


def get_rainbow_color():
    """Generate a smoothly transitioning pastel rainbow color for animations.

    :return: RGB tuple representing the current interpolated color
    """
    ticks = pygame.time.get_ticks()
    # 0.005 controls the speed of the transition
    blend_cycle = (math.sin(ticks * 0.005) + 1) / 2
    color_position = blend_cycle * 3

    i = int(color_position)
    j = (i + 1) % 4
    t = color_position - i

    palette = [
        (255, 180, 220), (220, 180, 255),
        (180, 255, 255), (180, 255, 180)
    ]

    c1, c2 = palette[i], palette[j]

    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def draw_corners(screen, rect, color=None, offset=12, size=10, width=2, animated=False):
    """Draw four corner brackets around a rectangle, with optional animation.

    :param screen: pygame display surface
    :param rect: rectangle to surround
    :param color: color of the corner lines
    :param offset: distance from the rectangle edges
    :param size: length of each corner segment
    :param width: thickness of the lines
    :param animated: whether to use animated rainbow coloring
    """
    if animated:
        color = get_rainbow_color()
    elif color is None:
        color = (255, 255, 255)

    l, r = rect.left - offset, rect.right + offset
    t, b = rect.top - offset, rect.bottom + offset

    # TL
    pygame.draw.line(screen, color, (l, t), (l + size, t), width)
    pygame.draw.line(screen, color, (l, t), (l, t + size), width)
    # TR
    pygame.draw.line(screen, color, (r, t), (r - size, t), width)
    pygame.draw.line(screen, color, (r, t), (r, t + size), width)
    # BL
    pygame.draw.line(screen, color, (l, b), (l + size, b), width)
    pygame.draw.line(screen, color, (l, b), (l, b - size), width)
    # BR
    pygame.draw.line(screen, color, (r, b), (r - size, b), width)
    pygame.draw.line(screen, color, (r, b), (r, b - size), width)
