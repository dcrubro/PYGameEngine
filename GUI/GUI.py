import imgui
from imgui.integrations.pygame import PygameRenderer


class GUI:
    def __init__(self):
        pass

    def start(self):
        imgui.create_context()
        imgui.get_io().display_size = 100, 100
        imgui.get_io().fonts.get_tex_data_as_rgba32()

        imgui.new_frame()
        imgui.begin("ImGUI Window", True)
        imgui.text("Hello, World!")
        imgui.end()

        imgui.render()
        imgui.end_frame()
