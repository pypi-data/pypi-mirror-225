class Animation:
    """
    a = Animation()
    make_unicorn(pack)
    a.add_frame(pack)
    make_heart(pack)
    a.add_frame(pack)
    a.show()  # a.show(to_pack=pack)
    """

    def __init__(self) -> None:
        self.frames = []  # 每个都是 PIL 图片
        self._pack = DotPack()

    def add_frame(self, pack_instance, frame_name=None):
        if not frame_name:
            frame_name = self._pack._generate_name()
        self.frames.append((frame_name, pack_instance._img.copy()))  # 不然引用同个对象

    def show(
        self,
        to_pack=None,
        filename="animation",
        optimize=False,
        duration=0.1,
        loop=0,
        **kwargs,
    ):
        # duration
        if to_pack:
            _frames = [frame for _, frame in self.frames]
            # todo show gif
            gif_filename = f"{filename}.gif"
            _frames[0].save(
                gif_filename,
                save_all=True,
                append_images=_frames[1:],
                optimize=optimize,
                duration=duration * 1000,
                loop=loop,
            )

            if to_pack._ledpanel:
                to_pack._update_animation(filename, self.frames)
                to_pack._display_gif(1, filename)

            if to_pack._microblocks_client:
                if loop == 0:
                    loop = True
                else:
                    loop = False

                to_pack._microblocks_client.upload_animation(filename, _frames)
                to_pack._microblocks_client.display_animation(
                    filename, pausing=duration, loop=loop
                )
        else:
            for name, frame in self.frames:
                self._pack.show(frame, PILimage=True)
                time.sleep(duration)

    def show_frame(self, frame_name, to_pack=None):
        for name, frame in self.frames:
            print(name)
            if frame_name == name:
                if to_pack:
                    to_pack.show(frame, PILimage=True)
                    # raise NotImplementedError
                else:
                    self._pack.show(frame, PILimage=True)
                return

    def remove_frame(self, frame_name):
        for name, frame in self.frames.copy():
            if frame_name == name:
                self.frames.remove((name, frame))
                return

    def save(
        self, name=None, resize=True, optimize=False, duration=1, loop=0, **kwargs
    ):
        if not name:
            name = self._pack._generate_name()
        if resize:
            _frames = [self._pack._resize_to_save(frame) for _, frame in self.frames]
        else:
            _frames = [frame for _, frame in self.frames]
        _frames[0].save(
            f"{name}.gif",
            save_all=True,
            append_images=_frames[1:],
            optimize=optimize,
            duration=duration * 1000,
            loop=loop,
        )

    def load(self, gif_image):
        """load gif"""
        im = Image.open(gif_image)
        self.frames = self._resize_gif(im)

    def _resize_gif(self, im):
        frames = [
            (
                self._pack._generate_name(),
                frame.copy()
                .resize((self._pack.size, self._pack.size), Image.NEAREST)
                .convert("RGB"),
            )
            for frame in ImageSequence.Iterator(im)
        ]
        return frames

    def clear(self):
        self.frames = []

    def show_animation(self, speed, name, to_pack=None):
        to_pack._display_gif(speed, name)

    def get_animation_list(self, to_pack=None):
        to_pack._get_gif_list()

    def delete_animation(self, file_name=None, to_pack=None):
        to_pack._delete_gif(file_name)

    def rename_animation(self, oldname, newname, to_pack=None):
        to_pack._rename_gif(oldname, newname)
