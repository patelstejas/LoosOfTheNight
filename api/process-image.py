# api/process-image.py
from PIL import Image
import sys

from PIL import Image
import numpy as np

class ImageLuminanceAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path).convert('RGB')
        self.luminance_array = self.calculate_luminance_array()
        self.median_luminance = self.calculate_median_luminance()
        self.average_luminance = self.calculate_average_luminance()
        self.max_luminace = self.calculate_max_luminance()  
        self.min_luminance = self.calculate_min_luminance()
        self.light_level = self.calculate_light_level()
        

    def calculate_luminance(self, rgb):
        # Extract RGB components
        red, green, blue = rgb[0], rgb[1], rgb[2]

        # Calculate luminance using standard coefficients
        return 0.299 * red + 0.587 * green + 0.114 * blue

    def calculate_luminance_array(self):
        width, height = self.image.size
        luminance_array = np.zeros((height, width))

        for y in range(height):
            for x in range(width):
                rgb = self.image.getpixel((x, y))
                luminance_array[y, x] = self.calculate_luminance(rgb)

        return luminance_array

    def calculate_median_luminance(self):
        return np.median(self.luminance_array)

    def calculate_average_luminance(self):
        return np.mean(self.luminance_array)

    def calculate_max_luminance(self):
        return np.max(self.luminance_array)

    def calculate_min_luminance(self):
        return np.min(self.luminance_array)
    def calculate_light_level(self):
        if(self.average_luminance > 123.21122354195543):
            return "high"
        elif(self.average_luminance > 94.60196085630591):
            return "medium-high"
        elif(self.average_luminance >78.07874663608563):
            return "medium"
        elif(self.average_luminance > 60.351494592163824):
            return "medium-low"
        else:
            return "low"
    def getAverage(self):
        return self.average_luminance
    def getMedian(self):
        return self.median_luminance
    def getMax(self):
        return self.max_luminace
    def getLightLevel(self):
        return self.light_level
        
        

# if __name__ == "__main__":
#     # Example usage
#     image_path = "Darkest.jpg"
#     analyzer = ImageLuminanceAnalyzer(image_path)

#     print("Median Luminance:", analyzer.calculate_median_luminance())
#     print("Average Luminance:", analyzer.calculate_average_luminance())
#     print("Max Luminance:", analyzer.calculate_max_luminance())
#     print("Min Luminance:", analyzer.calculate_min_luminance())


if __name__ == "__main__":
    image_name = sys.argv[1]
    location = sys.argv[2]

    image_path = f'/tmp/{image_name}'
    analyzer = ImageLuminanceAnalyzer(image_path)

    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "location": location,
        "median_luminance": analyzer.calculate_median_luminance(),
        "average_luminance": analyzer.calculate_average_luminance(),
        "max_luminance": analyzer.calculate_max_luminance(),
        "min_luminance": analyzer.calculate_min_luminance(),
        "light_level": analyzer.calculate_light_level(),
    }

    # Write data to a text file
    output_file_path = f'/tmp/{datetime.now().strftime("%Y%m%d%H%M%S")}-output.txt'
    with open(output_file_path, 'w') as file:
        json.dump(data, file)

    print(f'Data saved successfully. Image processed. Results written to: {output_file_path}')
