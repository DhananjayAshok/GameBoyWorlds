import warnings

warnings.filterwarnings("ignore", message=".*SDL2 binaries.*")
# To suppress pyBoy SDL2 warnings on some systems
from pyboy import PyBoy
from abc import ABC, abstractmethod
from poke_worlds.utils import log_error, log_warn, verify_parameters, show_frames


import numpy as np

import os
from typing import Dict, Tuple, Optional, List, Union
import cv2
from PIL import Image


class NamedScreenRegion:
    """
    Saves a reference to a named screen region (always a rectangle) for easy access.
    """

    def __init__(
        self,
        name: str,
        start_x: int,
        start_y: int,
        width: int,
        height: int,
        parameters: dict,
        *,
        target_path: Optional[str] = None,
        multi_target_paths: Optional[Dict[str, str]] = None,
    ):
        """
        Initializes a named screen region.

        Parameters:
            name (str): The name of the screen region.
            start_x (int): The starting x-coordinate of the region in pixel space of the full resolution game screen.
            start_y (int): The starting y-coordinate of the region in pixel space of the full resolution game screen.
            width (int): The width of the region in pixels.
            height (int): The height of the region in pixels.
            target (str): Optional path to a .npy file containing a screen capture of this region. Non-existent paths are only allowed if parameters['debug_mode'] (from configs/project_vars.yaml) is set to True.
            multi_target_paths (Optional[Dict[str, str]]): Optional dictionary containing multiple possible paths to .npy files for this region. Keys are arbitrary strings, values are paths to .npy files. If provided, this will override target_path and force it None. Allows using the same region for multiple target images.
        """
        if not isinstance(name, str):
            log_error(f"name must be a string. Found {type(name)}", parameters)
        if len(name.split()) > 1:
            log_error(
                f"name must be a single word with no spaces. Found {name}", parameters
            )
        if "," in name:
            log_error(f"name cannot contain commas. Found {name}", parameters)
        self.name = name
        """ Name of the screen region. """
        if (
            not isinstance(start_x, int)
            or not isinstance(start_y, int)
            or not isinstance(width, int)
            or not isinstance(height, int)
        ):
            log_error(
                f"start_x, start_y, width, and height must be integers. Found {type(start_x)}, {type(start_y)}, {type(width)}, {type(height)}",
                parameters,
            )
        self.start_x = start_x
        """ The starting x-coordinate of the region. """
        self.start_y = start_y
        """ The starting y-coordinate of the region. """
        self.width = width
        """ The width of the region. """
        self.height = height
        """ The height of the region. """
        self._parameters = parameters
        self.target_path = None
        """ Path to npy file of a screen capture that we will be comparing this region against. """
        self.target: Optional[np.ndarray] = None
        """ Numpy array of the target image for this region. """
        self.multi_target_paths = multi_target_paths
        self.multi_targets = None
        """ Dictionary of multiple target paths for this region. """
        if multi_target_paths is not None:
            self.multi_targets = {}
            for key, path in multi_target_paths.items():
                if not isinstance(key, str):
                    log_error(
                        f"multi_target_paths keys must be strings. Found {type(key)}",
                        parameters,
                    )
                if len(key.split()) > 1:
                    log_error(
                        f"multi_target_paths keys must be single words with no spaces. Found {key}",
                        parameters,
                    )
                if "," in key:
                    log_error(
                        f"multi_target_paths keys cannot contain commas. Found {key}",
                        parameters,
                    )
                self.multi_targets[key] = self._sanity_load_target(path)
        else:
            if target_path is not None:
                self.target_path = target_path
                self.target = self._sanity_load_target(target_path)

    def _sanity_load_target(self, target_path: str) -> Optional[np.ndarray]:
        """
        Loads the target image from the given path.

        :param target_path: Path to the .npy file containing the target image.
        :type target_path: str
        :return: The loaded target image as a numpy array, or None if the file does not exist and debug_mode is enabled.
        :rtype: ndarray[_AnyShape, dtype[Any]] | None
        """
        if not target_path.endswith(".npy"):
            target_path = target_path + ".npy"
        if not os.path.exists(target_path):
            if not self._parameters["debug_mode"]:
                log_error(
                    f"Target file {target_path} does not exist. This is only allowed in debug_mode (can be set in configs/project_vars.yaml)",
                    self._parameters,
                )
            else:
                log_warn(
                    f"Target file {target_path} does not exist. Continuing since debug_mode is enabled.",
                    self._parameters,
                )
            return None
        else:
            target = np.load(target_path)
            return target

    def get_end_x(self) -> int:
        """
        Returns the end x-coordinate of the named screen region.

        Returns:
            int: The end x-coordinate of the named screen region.
        """
        return self.start_x + self.width

    def get_end_y(self) -> int:
        """
        Returns the end y-coordinate of the named screen region.
        Returns:
            int: The end y-coordinate of the named screen region.
        """
        return self.start_y + self.height

    def get_corners(self) -> Tuple[int, int, int, int]:
        """
        Returns the corners of the named screen region as (start_x, start_y, end_x, end_y).

        :return: The corners of the named screen region.
        :rtype: Tuple[int, int, int, int]
        """
        return (self.start_x, self.start_y, self.get_end_x(), self.get_end_y())

    def __str__(self) -> str:
        return f"NamedScreenRegion(name={self.name}, start_x={self.start_x}, start_y={self.start_y}, width={self.width}, height={self.height})"

    def __repr__(self) -> str:
        return self.__str__()

    def compare_against_target(
        self, reference: np.ndarray, strict_shape: bool = True
    ) -> float:
        """
        Computes the Absolute Error (AE) between the given reference image and the target image.

        :param reference: The reference image to compare.
        :type reference: np.ndarray
        :param strict_shape: Whether to error out if the array shapes do not match.
        :type strict_shape: bool
        :return: The Absolute Error (AE) between the reference and target images.
        :rtype: float
        """
        if self.target is None:
            if self._parameters["debug_mode"]:
                return False
            log_error(
                f"No target image set for NamedScreenRegion {self.name}. Cannot compare.",
                self._parameters,
            )
        if reference.shape != self.target.shape:
            if strict_shape:
                log_error(
                    f"Reference image shape {reference.shape} does not match target image shape {self.target.shape} for NamedScreenRegion {self.name}.",
                    self._parameters,
                )
            else:
                return False
        diff = np.abs(reference.astype(np.float32) - self.target.astype(np.float32))
        mae = np.mean(diff)
        return mae

    def compare_against_multi_target(
        self, target_name: str, reference: np.ndarray, strict_shape: bool = True
    ) -> float:
        """
         Computes the Absolute Error (AE) between the given reference image and one of the multiple target images.

        :param self: Description
        :param target_name: The name of the target image to compare against.
        :type target_name: str
        :param reference: The reference image to compare.
        :type reference: np.ndarray
        :param strict_shape: Whether to error out if the array shapes do not match.
        :type strict_shape: bool
        :return: The Absolute Error (AE) between the reference and specified target images.
        :rtype: float
        """
        if self.multi_targets is None or target_name not in self.multi_targets:
            log_error(
                f"No multi target image set for NamedScreenRegion {self.name} with target name {target_name}. Cannot compare.",
                self._parameters,
            )
        self.target = self.multi_targets[target_name]
        mae = self.compare_against_target(reference, strict_shape)
        self.target = None
        return mae

    def matches_target(
        self, reference: np.ndarray, strict_shape: bool = True, epsilon=0.01
    ) -> bool:
        """
        Compares the given reference image to the target image using Absolute Error (AE).

        :param self: Description
        :param reference: The reference image to compare.
        :type reference: np.ndarray
        :param strict_shape: Whether to error out if the array shapes do not match.
        :type strict_shape: bool
        :param epsilon: The threshold for considering a match.
        :return: True if the AE is below the epsilon threshold, False otherwise.
        :rtype: bool
        """
        mae = self.compare_against_target(reference, strict_shape)
        if mae <= epsilon:
            return True
        return False

    def matches_multi_target(
        self, target_name: str, reference: np.ndarray, strict_shape: bool = True
    ) -> bool:
        """
        Compares the given reference image to one of the multiple target images using Absolute Error (AE).

        :param target_name: The name of the target image to compare against.
        :type target_name: str
        :param reference: The reference image to compare.
        :type reference: np.ndarray
        :param strict_shape: Whether to error out if the array shapes do not match.
        :type strict_shape: bool
        :return: True if the AE is below the epsilon threshold, False otherwise.
        :rtype: bool
        """
        if self.multi_targets is None or target_name not in self.multi_targets:
            log_error(
                f"No multi target image set for NamedScreenRegion {self.name} with target name {target_name}. Cannot compare.",
                self._parameters,
            )
        self.target = self.multi_targets[target_name]
        result = self.matches_target(reference, strict_shape)
        self.target = None
        return result


class StateParser(ABC):
    """
    Abstract base class for parsing game state variables from the GameBoy emulator.
    """

    def __init__(
        self,
        pyboy,
        parameters,
        named_screen_regions: Optional[List[NamedScreenRegion]] = None,
    ):
        """
        Initializes the StateParser. Child implementations should call super().__init__() after running their code.
            All children must create a self.rom_data_path variable
        Args:
            pyboy: An instance of the PyBoy emulator.
            parameters: A dictionary of parameters for configuration.
            named_screen_regions (Optional[list[NamedScreenRegion]]): A list of NamedScreenRegion objects for easy access to specific screen regions.
        """
        verify_parameters(parameters)
        self._parameters = parameters
        if not hasattr(self, "rom_data_path"):
            log_error(
                f"StateParsers must define a self.rom_data_path variable pointing to the rom data path for the game variant.",
                self._parameters,
            )
        self.rom_data_path: str = self.rom_data_path
        """ Path to the rom data directory for the game variant. """
        if not isinstance(pyboy, PyBoy):
            log_error("pyboy must be an instance of PyBoy", self._parameters)
        self._pyboy = pyboy
        self.named_screen_regions: dict[str, NamedScreenRegion] = {}
        """ Dictionary of NamedScreenRegion objects for easy access to specific screen regions. """
        if named_screen_regions is not None:
            for region in named_screen_regions:
                if not isinstance(region, NamedScreenRegion):
                    log_error(
                        f"named_screen_regions must be a list of NamedScreenRegion objects. Found {type(region)}",
                        self._parameters,
                    )
                if region.name in self.named_screen_regions:
                    log_error(
                        f"Duplicate named screen region: {region.name}",
                        self._parameters,
                    )
                self.named_screen_regions[region.name] = region
        self.image_references = {}
        """ Dictionary of image references loaded. """
        location = os.path.join(self.rom_data_path, "image_references")
        if os.path.exists(location):
            for file in os.listdir(location):
                image_path = os.path.join(location, file)
                if image_path.endswith((".png", ".jpg", ".jpeg")):
                    reference_name = file.rsplit(".", 1)[0]
                    image = Image.open(image_path)
                    self.image_references[reference_name] = image
                else:
                    log_warn(
                        f"Found unsupported image extension {file} in {location}. Only place image files in this folder.",
                        self._parameters,
                    )

    @staticmethod
    def bit_count(bits: int) -> int:
        """
        Counts the number of set bits (1s) in the given integer.
        Args:
            bits (int): The integer to count set bits in.
        Returns:
            int: The number of set bits.
        """
        return bin(bits).count("1")

    def read_m(self, addr: bytes) -> int:
        """
        Reads a byte from the specified memory address.
        Args:
            addr (int): The memory address to read from.
        Returns:
            int: The byte value at the specified memory address.
        """
        # return self.pyboy.get_memory_value(addr)
        return self._pyboy.memory[addr]

    def read_bits(self, addr) -> str:
        """
        Reads a memory address and returns the result as a binary string. Adds padding so that reading bit 0 works correctly.
        Args:
            addr (int): The memory address to read from.
        Returns:
            str: The binary string representation of the byte at the specified memory address.
        """
        # add padding so zero will read '0b100000000' instead of '0b0'
        return bin(256 + self.read_m(addr))

    def read_bit(self, addr, bit: int) -> bool:
        """
        Reads a specific bit from a memory address.
        Args:
            addr (int): The memory address to read from.
            bit (int): The bit position to read (0-7).
        Returns:
            bool: True if the bit is set (1), False otherwise.
        """
        # add padding so zero will read '0b100000000' instead of '0b0'
        return self.read_bits(addr)[-bit - 1] == "1"

    def read_m_bit(self, addr_bit: str) -> bool:
        """
        Reads a specific addr-bit string from a memory address.
        Args:
            addr_bit (str): The - concatenation of a memory address and the bit position (e.g. '0xD87D-5')
        Returns:
            bool: True if the bit at that memory address is set (1), False otherwise
        """
        if "-" not in addr_bit:
            log_error(f"Incorrect format addr_bit: {addr_bit}", self._parameters)
        addr, bit = addr_bit.split("-")
        flag = False
        try:
            addr = eval(addr)
        except:
            flag = True
        if flag:
            log_error(
                f"Could not eval byte string: {addr}. Check format", self._parameters
            )
        if not bit.isdigit():
            log_error(f"bit {bit} is not digit", self._parameters)
        bit = int(bit)
        return self.read_bit(addr, bit)

    def get_raised_flags(self, item_dict: dict) -> set:
        """
        Reads a dictionary of the form {flag_name: memory_address-bit} and returns a set of all flag names that are currently raised (i.e. the bit at the memory address is 1).
        Args:
            item_dict (dict): A dictionary mapping flag names to memory address-bit strings.
        Returns:
            set: A set of flag names that are currently raised.
        """
        items = set()
        for item_name, slot in item_dict.items():
            if self.read_m_bit(slot):
                items.add(item_name)
        return items

    def get_current_frame(self) -> np.ndarray:
        """
        Reads the pyboy screen and returns a full resolution numpy array

        Returns:
            np.ndarray: The rendered image as a numpy array.
        """
        screen = self._pyboy.screen.ndarray[
            :, :, 0:1
        ]  # (144, 160, 3) but force just greyscale
        return screen.copy()

    @staticmethod
    def capture_box(
        current_frame: np.ndarray,
        start_x: int,
        start_y: int,
        width: int,
        height: int,
    ) -> np.ndarray:
        """
        Captures a rectangular region from the current frame.

        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            start_x (int): The starting x-coordinate of the region.
            start_y (int): The starting y-coordinate of the region.
            width (int): The width of the region.
            height (int): The height of the region.
        Returns:
            np.ndarray: The captured rectangular region.
        """
        # first check that the box is within the frame
        end_x = start_x + width
        end_y = start_y + height
        if (
            start_x < 0
            or start_y < 0
            or end_x > current_frame.shape[1]
            or end_y > current_frame.shape[0]
        ):
            start_x = max(0, start_x)
            start_y = max(0, start_y)
            end_x = min(current_frame.shape[1], end_x)
            end_y = min(current_frame.shape[0], end_y)
        return current_frame[start_y:end_y, start_x:end_x, :]

    @staticmethod
    def capture_square_centered(
        current_frame: np.ndarray, center_x: int, center_y: int, box_size: int
    ) -> np.ndarray:
        """
        Captures a square region from the current frame centered at (center_x, center_y) with the given box size.

        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            center_x (int): The x-coordinate of the center of the square.
            center_y (int): The y-coordinate of the center of the square.
            box_size (int): The size of the square box to capture.

        Returns:
            np.ndarray: The captured square region.
        """
        half_box = box_size // 2
        start_x = max(center_x - half_box, 0)
        end_x = min(center_x + half_box, current_frame.shape[1])
        start_y = max(center_y - half_box, 0)
        end_y = min(center_y + half_box, current_frame.shape[0])
        return current_frame[start_y:end_y, start_x:end_x, :]

    @staticmethod
    def draw_box(
        current_frame: np.ndarray,
        start_x: int,
        start_y: int,
        width: int,
        height: int,
        color: tuple = (0, 0, 0),
        thickness: int = 1,
    ) -> np.ndarray:
        """
        Draws a rectangle on the current frame.

        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            start_x (int): The starting x-coordinate of the rectangle.
            start_y (int): The starting y-coordinate of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            color (tuple, optional): The color of the rectangle in BGR format.
            thickness (int, optional): The thickness of the rectangle border.

        Returns:
            np.ndarray: The frame with the drawn rectangle.
        """
        end_x = start_x + width
        end_y = start_y + height
        if (
            start_x < 0
            or start_y < 0
            or end_x > current_frame.shape[1]
            or end_y > current_frame.shape[0]
        ):
            start_x = max(0, start_x)
            start_y = max(0, start_y)
            end_x = min(current_frame.shape[1], end_x)
            end_y = min(current_frame.shape[0], end_y)
        frame_with_box = current_frame.copy()
        cv2.rectangle(
            frame_with_box, (start_x, start_y), (end_x, end_y), color, thickness
        )
        return frame_with_box

    @staticmethod
    def draw_square_centered(
        current_frame: np.ndarray,
        center_x: int,
        center_y: int,
        box_size: int,
        color: tuple = (0, 0, 0),
        thickness: int = 1,
    ) -> np.ndarray:
        """
        Draws a square on the current frame centered at (center_x, center_y) with the given box size.

        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            center_x (int): The x-coordinate of the center of the square.
            center_y (int): The y-coordinate of the center of the square.
            box_size (int): The size of the square box to draw.
            color (tuple, optional): The color of the square in BGR format.
            thickness (int, optional): The thickness of the square border.

        Returns:
            np.ndarray: The frame with the drawn square.
        """
        half_box = box_size // 2
        start_x = max(center_x - half_box, 0)
        end_x = min(center_x + half_box, current_frame.shape[1])
        start_y = max(center_y - half_box, 0)
        end_y = min(center_y + half_box, current_frame.shape[0])
        frame_with_square = current_frame.copy()
        cv2.rectangle(
            frame_with_square, (start_x, start_y), (end_x, end_y), color, thickness
        )
        return frame_with_square

    def capture_named_region(self, current_frame: np.ndarray, name: str) -> np.ndarray:
        """
        Captures a named region from the current frame.

        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            name (str): The name of the region to capture.

        Returns:
            np.ndarray: The captured region.
        """
        if name not in self.named_screen_regions:
            log_error(f"Named screen region {name} not found.", self._parameters)
        region = self.named_screen_regions[name]
        x, y, w, h = region.start_x, region.start_y, region.width, region.height
        return self.capture_box(current_frame, x, y, w, h)

    def compare_named_region_against_target(
        self, current_frame: np.ndarray, name: str, strict_shape: bool = True
    ) -> float:
        """
        Computes the Absolute Error (AE) between a named region from the current frame and its target image.

        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            name (str): The name of the region to compare.
            strict_shape (bool, optional): Whether to error out if the array shapes do not match.
        Returns:
            float: The Absolute Error (AE) between the named region and its target image.
        """
        if name not in self.named_screen_regions:
            log_error(f"Named screen region {name} not found.", self._parameters)
        region = self.named_screen_regions[name]
        captured_region = self.capture_named_region(current_frame, name)
        return region.compare_against_target(captured_region, strict_shape)

    def named_region_matches_target(self, current_frame: np.ndarray, name: str) -> bool:
        """
        Compares a named region from the current frame to its target image using Absolute Error (AE).

        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            name (str): The name of the region to compare.
        Returns:
            bool: True if the region matches the target image, False otherwise.
        """
        if name not in self.named_screen_regions:
            log_error(f"Named screen region {name} not found.", self._parameters)
        region = self.named_screen_regions[name]
        captured_region = self.capture_named_region(current_frame, name)
        return region.matches_target(captured_region)

    def compare_named_region_against_multi_target(
        self,
        current_frame: np.ndarray,
        name: str,
        target_name: str,
        strict_shape: bool = True,
    ) -> float:
        """
        Computes the Absolute Error (AE) between a named region from the current frame and one of its multiple target images.

        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            name (str): The name of the region to compare.
            target_name (str): The name of the target image to compare against.
            strict_shape (bool, optional): Whether to error out if the array shapes do not match.
        Returns:
            float: The Absolute Error (AE) between the named region and the specified target image.
        """
        if name not in self.named_screen_regions:
            log_error(f"Named screen region {name} not found.", self._parameters)
        region = self.named_screen_regions[name]
        captured_region = self.capture_named_region(current_frame, name)
        return region.compare_against_multi_target(
            target_name, captured_region, strict_shape
        )

    def named_region_matches_multi_target(
        self, current_frame: np.ndarray, name: str, target_name: str
    ) -> bool:
        """
        Compares a named region from the current frame to one of its multiple target images using Absolute Error (AE).

        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            name (str): The name of the region to compare.
            target_name (str): The name of the target image to compare against.
        Returns:
            bool: True if the region matches the specified target image, False otherwise.
        """
        if name not in self.named_screen_regions:
            log_error(f"Named screen region {name} not found.", self._parameters)
        region = self.named_screen_regions[name]
        captured_region = self.capture_named_region(current_frame, name)
        return region.matches_multi_target(target_name, captured_region)

    def draw_named_region(
        self,
        current_frame: np.ndarray,
        name: str,
        color: tuple = (0, 0, 0),
        thickness: int = 1,
    ) -> np.ndarray:
        """
        Draws a named region on the current frame.

        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            name (str): The name of the region to draw.
            color (tuple, optional): The color of the rectangle in BGR format.
            thickness (int, optional): The thickness of the rectangle border.

        Returns:
            np.ndarray: The frame with the drawn rectangle.
        """
        if name not in self.named_screen_regions:
            log_error(f"Named screen region {name} not found.", self._parameters)
        region = self.named_screen_regions[name]
        x, y, w, h = region.start_x, region.start_y, region.width, region.height
        return self.draw_box(current_frame, x, y, w, h, color, thickness)

    @staticmethod
    def draw_grid_overlay(
        current_frame: np.ndarray, grid_skip: int = 16, x_offset=0, y_offset=-2
    ) -> np.ndarray:
        """
        Draws a grid overlay on the current frame for easier region identification.
        Args:
            current_frame (np.ndarray): The current frame from the emulator.
            grid_skip (int, optional): The number of pixels between grid lines.
            x_offset (int, optional): The x-offset to apply when drawing the grid.
            y_offset (int, optional): The y-offset to apply when drawing the grid.
        Returns:
            np.ndarray: The frame with the grid overlay.
        """
        frame_with_grid = current_frame.copy()
        for x in range(0, current_frame.shape[1], grid_skip):
            cv2.line(
                frame_with_grid,
                (x + x_offset, 0),
                (x + x_offset, current_frame.shape[0]),
                (0, 0, 255),
                1,
                lineType=cv2.LINE_AA,
            )
        for y in range(0, current_frame.shape[0], grid_skip):
            cv2.line(
                frame_with_grid,
                (0, y + y_offset),
                (current_frame.shape[1], y + y_offset),
                (0, 0, 255),
                1,
                lineType=cv2.LINE_AA,
            )
        return frame_with_grid

    @staticmethod
    def capture_grid_cells(
        current_frame: np.ndarray,
        *,
        quadrant: str = None,
        grid_skip: int = 16,
        x_offset=0,
        y_offset=-2,
    ) -> Dict[Tuple[int, int], np.ndarray]:
        """
        Captures all grid cells from the current frame based on the specified grid skip.

        Example:
        ```python
        import matplotlib.pyplot as plt
        # ... run the state_parser in an env, example in dev_play.
        grid_cells = StateParser.capture_grid_cells(current_frame)
        keep_keys = [(0, 0), (0, 1)]
        new_cells = {}
        for cell in keep_keys:
            new_cells[cell] = grid_cells[cell]
        grid_cells = new_cells
        drawn_frame = self.state_parser.reform_image(grid_cells)
        quadrants = self.state_parser.get_quadrant_frame(grid_cells=grid_cells)
        plt.imshow(drawn_frame[:, :, 0], cmap="gray")
        plt.title(f"Full Screen with Grid Overlay")
        plt.show()
        merged = self.state_parser.reform_image(grid_cells)
        plt.imshow(merged[:, :, 0], cmap="gray")
        plt.show()
        ```

        :param current_frame: An emulator frame.
        :type current_frame: np.ndarray
        :param quadrant: If specified, only captures cells in the given quadrant ('TL', 'TR', 'BL', 'BR').
        :type quadrant: str
        :param grid_skip: The number of pixels between grid lines.
        :type grid_skip: int
        :param x_offset: The x-offset to apply when capturing cells.
        :param y_offset: The y-offset to apply when capturing cells.
        :return: A dictionary mapping grid cell coordinates to their captured images.
            The grid cells are with the central cell as (0,0)
        :rtype: Dict[Tuple[int, int], ndarray[_AnyShape, dtype[Any]]]
        """
        if quadrant is not None:
            if quadrant.lower() not in ["tl", "tr", "bl", "br"]:
                log_error(
                    f"Invalid quadrant: {quadrant}. Must be one of 'TL', 'TR', 'BL', 'BR'",
                )
        cells = {}
        if x_offset != 0:
            x_iter = [-x_offset] + list(range(0, current_frame.shape[1], grid_skip))
        else:
            x_iter = list(range(0, current_frame.shape[1], grid_skip))
        if y_offset != 0:
            y_iter = [-y_offset] + list(range(0, current_frame.shape[0], grid_skip))
        else:
            y_iter = list(range(0, current_frame.shape[0], grid_skip))

        def x_ind(x):
            index = x_iter.index(x)
            return (index - (len(x_iter)) // 2) + 1 * (x_offset == 0)

        def y_ind(y):
            index = y_iter.index(y)
            return -(index - len(y_iter) // 2) + 1 * (y_offset == 0)

        for x in x_iter:
            for y in y_iter:
                x_cell = x_ind(x)
                y_cell = y_ind(y)
                if quadrant is not None:
                    if quadrant.lower() == "tl" and (x_cell > 0 or y_cell < 0):
                        continue
                    elif quadrant.lower() == "tr" and (x_cell < 0 or y_cell < 0):
                        continue
                    elif quadrant.lower() == "bl" and (x_cell > 0 or y_cell > 0):
                        continue
                    elif quadrant.lower() == "br" and (x_cell < 0 or y_cell > 0):
                        continue
                cell_image = StateParser.capture_box(
                    current_frame, x + x_offset, y + y_offset, grid_skip, grid_skip
                )
                cells[(x_cell, y_cell)] = cell_image
        return cells

    @staticmethod
    def reform_image(grid_cells: Dict[Tuple[int, int], np.ndarray]) -> np.ndarray:
        """
        Reform the image from grid cells back into a single image.
        Expects the grid_cells to correspond to a rectangle.
        Args:
            grid_cells (Dict[Tuple[int, int], np.ndarray]): A dictionary mapping (x, y) coordinates to image cells.

        Returns:
            np.ndarray: The reformed image.
        """
        coords = grid_cells.keys()
        if len(coords) == 1:
            return list(grid_cells.values())[0]
        xs = list(set([coord[0] for coord in coords]))
        ys = list(set([coord[1] for coord in coords]))
        xs.sort()
        ys.sort()
        rows = []
        for y in ys:
            row_cells = []
            for x in xs:
                row_cells.append(grid_cells[(x, y)])
            row_image = np.concatenate(row_cells, axis=1)
            rows.append(row_image)
        new_rows = []

        if len(rows) == 1:
            new_rows.append(rows[0])
        else:
            # This part is super hacky.
            # Sometimes, the last and second last row are the exact same. In that case, skip the last row. I don't know man.
            # show_frames(rows)
            is_same = rows[-1].shape != rows[-2].shape
            back_offset = 2 if is_same else 1
            for item in range(len(rows) - back_offset, -1, -1):
                new_rows.append(rows[item])
        full_image = np.concatenate(new_rows, axis=0)
        return full_image

    def get_quadrant_frame(
        self, grid_cells: Dict[Tuple[int, int], np.ndarray] = None
    ) -> Dict[str, Dict[str, Union[np.ndarray, Dict[Tuple[int, int], np.ndarray]]]]:
        """
        Divides the current frame or subframe into quadrants and returns groups of quadrants

        :param grid_cells: Subset of grid cells to split. Must be a rectangular box in (x, y) space.
        :type grid_cells: Dict[Tuple[int, int], np.ndarray]
        :return: A dictionary where the keys are quadrant keys [tr, tl, br, bl] and values are:

            - screen: which maps to the single numpy array representing that quadrant as a screen
            - cells: A dictionary mapping cell grids to the specific screen region as numpy arrays.
        :rtype: Dict[str, Dict[str, Union[np.ndarray, Dict[Tuple[int, int], np.ndarray]]]]
        """
        if grid_cells is None:
            grid_cells = self.capture_grid_cells(self.get_current_frame())
        coords = grid_cells.keys()
        xs = list(set([coord[0] for coord in coords]))
        ys = list(set([coord[1] for coord in coords]))
        xs.sort()
        ys.sort()
        mid_x = xs[len(xs) // 2]
        mid_y = ys[len(ys) // 2]
        quadrants = {
            "tl": {"screen": None, "cells": {}},
            "tr": {"screen": None, "cells": {}},
            "bl": {"screen": None, "cells": {}},
            "br": {"screen": None, "cells": {}},
        }
        lower_x = [x for x in xs if x < mid_x]
        higher_x = [x for x in xs if x >= mid_x]
        lower_y = [y for y in ys if y < mid_y]
        higher_y = [y for y in ys if y >= mid_y]
        for x in lower_x:
            for y in higher_y:
                quadrants["tl"]["cells"][(x, y)] = grid_cells[(x, y)]
        quadrants["tl"]["screen"] = self.reform_image(quadrants["tl"]["cells"])
        for x in higher_x:
            for y in higher_y:
                quadrants["tr"]["cells"][(x, y)] = grid_cells[(x, y)]
        quadrants["tr"]["screen"] = self.reform_image(quadrants["tr"]["cells"])
        for x in lower_x:
            for y in lower_y:
                quadrants["bl"]["cells"][(x, y)] = grid_cells[(x, y)]
        quadrants["bl"]["screen"] = self.reform_image(quadrants["bl"]["cells"])
        for x in higher_x:
            for y in lower_y:
                quadrants["br"]["cells"][(x, y)] = grid_cells[(x, y)]
        quadrants["br"]["screen"] = self.reform_image(quadrants["br"]["cells"])
        return quadrants

    def get_image_reference(self, reference_name: str) -> Image.Image:
        """
        Gets an image reference from the loaded image references.
        Args:
            reference_name (str): The name of the image reference to load
        Returns:
            Image.Image: The loaded image reference.
        """
        if reference_name not in self.image_references:
            log_error(
                f"Image reference {reference_name} not found. Available options: {self.image_references.keys()}. If you want to add an image reference, add a file to the image_references folder.",
                self._parameters,
            )
        return self.image_references[reference_name]

    @abstractmethod
    def __repr__(self) -> str:
        """
        Name of the parser for logging purposes.
        :return: string name of the parser
        """
        raise NotImplementedError


class DummyParser(StateParser):
    def __repr__(self) -> str:
        return "DummyParser"
