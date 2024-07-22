import array
import gc
class Array2D:
    def __init__(self, nrows, ncols):
        self._buf = array.array("I", (0 for _ in range(nrows * ncols)))
        self._ncols = ncols
        self._nrows = nrows

    def __getitem__(self, *args):
        if isinstance(args[0], tuple):  # ar[i,k]
            row, col = args[0][0], args[0][1]
            return self._buf[col + row * self._ncols]

        elif isinstance(args[0], slice):  # arr[i:k] # get row slice

            return self._buf[args[0].start : args[0].stop]

        elif isinstance(args[0], int):  # arr[i]   row like

            return self._buf[
                (args[0] * self._ncols) : (args[0] * self._ncols + self._ncols)
            ]

    def __setitem__(self, *args):
        row, col, value = args[0][0], args[0][1], args[1]
        self._buf[col + row * self._ncols] = value

class BMPReader(object):
    def __init__(self, filename):
        self._filename = filename
        self._read_img_data()

    def get_pixels(self):
        """
        Returns a multi-dimensional array of the RGB values of each pixel in the
        image, arranged by rows and columns from the top-left.  Access any pixel
        by its location, eg:

        pixels = BMPReader(filename).get_pixels()
        top_left_px = pixels[0][0] # [255, 0, 0]
        bottom_right_px = pixels[8][8] # [0, 255, 255]
        """
        gc.collect()
        pixel_grid = Array2D(self.width,self.height)
        for x in range(self.height):
            row = []
            self.pixel_data = self.pixel_data[0:len(self.pixel_data)-self.width%4]
            for y in range(self.width):
                pixint = self.pixel_data[len(self.pixel_data)-3] + (self.pixel_data[len(self.pixel_data)-2] << 8) + (self.pixel_data[len(self.pixel_data)-1] << 16)
                self.pixel_data = self.pixel_data[0:len(self.pixel_data)-3]
                row.append(pixint)

            row.reverse()
            for i in range(self.width):
                pixel_grid[i,x] = row[i]


        return pixel_grid

    def _read_img_data(self):
        def lebytes_to_int(bytes):
            return int.from_bytes(bytes,"little")
        gc.collect()
        with open(self._filename, 'rb') as f:
            img_bytes=f.read()
        # Before we proceed, we need to ensure certain conditions are met
        assert list(img_bytes[0:2]) == [66,77], "Not a valid BMP file"
        assert lebytes_to_int(img_bytes[30:34]) == 0, \
            "Compression is not supported"
        assert lebytes_to_int(img_bytes[0x1c:0x1c+2]) == 24, \
            "Only 24-bit colour depth is supported"



        self.width = lebytes_to_int(img_bytes[18:22])
        self.height = lebytes_to_int(img_bytes[22:26])
        start_pos = lebytes_to_int(img_bytes[10:14])
        end_pos = start_pos + lebytes_to_int(img_bytes[34:38])
        self.pixel_data = img_bytes[start_pos:end_pos]
