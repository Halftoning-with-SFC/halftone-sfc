import glob

from PIL import Image


def make_gif(frame_folder):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.jpeg")]
    frame_one = frames[0]
    frame_one.save(
        "my_awesome.gif",
        format="GIF",
        append_images=frames,
        save_all=True,
        duration=100,
        loop=0,
    )


if __name__ == "__main__":
    make_gif("image_gif")
