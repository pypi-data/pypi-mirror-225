import argparse
import math

from PIL import Image


def tile(input_file: str, output_file: str, output_res: str, multiplier: float):
    """Tile image."""
    img = Image.open(input_file).convert("RGB")

    inwpx, inhpx = img.size
    outwpx, outhpx = [int(x) for x in output_res.split("x")]

    n = math.ceil(multiplier)
    new_img = Image.new("RGB", (n * inwpx, n * inhpx))
    for w in [ix * inwpx for ix in range(n)]:
        for h in [jx * inhpx for jx in range(n)]:
            new_img.paste(img, (w, h))

    new_img = new_img.crop(
        (0, 0, math.ceil(inwpx * multiplier), math.ceil(inhpx * multiplier))
    )

    new_img = new_img.resize((outwpx, outhpx))
    new_img.save(output_file)


def main():
    parser = argparse.ArgumentParser(
        description="Tile (w, h) image to (m * w, m * h) image given multiplier m and "
        "then resize to output_resolution."
    )
    parser.add_argument("--input", required=True, help="Path to input image", type=str)
    parser.add_argument(
        "--output", required=True, help="Path to output image", type=str
    )
    parser.add_argument(
        "--multiplier", required=True, help="Size multiplier for image", type=float
    )
    parser.add_argument(
        "--output_res",
        required=True,
        help="Output resolution",
        default="768x768",
        type=str,
    )

    args = parser.parse_args()
    tile(
        input_file=args.input,
        output_file=args.output,
        multiplier=args.multiplier,
        output_res=args.output_res,
    )


if __name__ == "__main__":
    main()
