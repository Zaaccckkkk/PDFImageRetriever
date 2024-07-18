from PIL import Image


class ColorDetector:
    """Detect the colors of an image."""

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.rgb_image = self.image.convert('RGB')
        self.pixels = self.rgb_image.load()

    def analyze(self):
        """Analyze the RGB image, and get the colors in the image."""
        width, height = self.rgb_image.size
        colors = {}

        # Look at every pixels in the rgb image
        for x in range(width):
            for y in range(height):
                pixel = self.pixels[x, y]
                if pixel in colors:
                    colors[pixel] += 1
                else:
                    colors[pixel] = 1

        # Sort colors by frequency
        sorted_colors = sorted(colors.items(), key=lambda item: item[1], reverse=True)
        return sorted_colors

    def get_top_color(self):
        """Return the most common color."""

        sorted_colors = self.analyze()
        return sorted_colors[0][0]

    def print_top_colors(self, num_colors=10):
        """Print the top 10 most common colors."""
        sorted_colors = self.analyze()
        for color, count in sorted_colors[:num_colors]:
            print(f"Color: {color}, Count: {count}")
