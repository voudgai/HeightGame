import random
import numpy as np
import numpy as np
from scipy.ndimage import gaussian_filter
from collections import deque
from xml.etree.ElementTree import tostring

from game.sprites.archipelago import *

"""
ONLY PART OF CODE GENERATED WITH LLM, 
THIS WAS FOR CODE TESTING WHEN THERE WAS NO INTERNET CONNECTION
AVAILABLE. IT WOULD GENERATE ARCHIPELAGOS THAT MADE SENSE AND NOT
JUST RANDOM HEIGHTS MATRIX.

"""
class RandomIslandGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_island_map(size=30, max_height=1000):
        """
        Generates a random island map with realistic-looking terrain.

        Args:
            size (int): Size of the square map (default: 30)
            max_height (int): Maximum terrain height (default: 1000)

        Returns:
            numpy.ndarray: 2D array representing the height map
        """

        def generate_perlin_like_noise(size):
            # Generate base noise
            scale = 4
            octaves = 6
            persistence = 0.5

            noise = np.zeros((size, size))
            amplitude = 1.0
            frequency = 1.0
            max_value = 0

            for _ in range(octaves):
                # Generate noise at current frequency
                smaller_size = max(1, int(size / frequency))
                noise_layer = np.random.rand(smaller_size, smaller_size)

                # Resize to full size using zoom
                from scipy.ndimage import zoom
                zoom_factor = size / smaller_size
                noise_layer = zoom(noise_layer, zoom_factor)

                # Ensure noise_layer has exact target shape
                noise_layer = noise_layer[:size, :size]

                # Now the shapes match for addition
                noise += amplitude * noise_layer
                max_value += amplitude
                amplitude *= persistence
                frequency *= 2

            return noise / max_value

        # Generate base terrain using noise
        terrain = generate_perlin_like_noise(size)

        # Create radial gradient for island shape
        x = np.linspace(-1, 1, size)
        y = np.linspace(-1, 1, size)
        X, Y = np.meshgrid(x, y)
        distance = np.sqrt(X ** 2 + Y ** 2)

        # Create island mask
        island_mask = 1 - np.clip(distance * 1.5, 0, 1)
        island_mask = gaussian_filter(island_mask, sigma=1)

        # Apply mask to terrain
        terrain = terrain * island_mask

        # Normalize and scale to max height
        terrain = ((terrain - terrain.min()) / (terrain.max() - terrain.min()) * max_height)

        # Apply threshold to ensure we have some water level
        water_level = 0.2 * max_height
        terrain[terrain < water_level] = 0

        # Round to integers
        terrain = np.round(terrain).astype(int)

        return terrain

    @staticmethod
    def generate_archipelago_map(size=30, max_height=1000, num_islands=4, min_radius=0.1, max_radius=0.25):
        """
        Generates a random archipelago map with multiple realistic-looking islands.

        Args:
            size (int): Size of the square map (default: 30)
            max_height (int): Maximum terrain height (default: 1000)
            num_islands (int): Number of islands to generate (default: 4)
            min_radius (float): Minimum radius of islands as fraction of map size (default: 0.1)
            max_radius (float): Maximum radius of islands as fraction of map size (default: 0.25)

        Returns:
            numpy.ndarray: 2D array representing the height map
        """


        def generate_perlin_like_noise(size):
            octaves = 6
            persistence = 0.5

            noise = np.zeros((size, size))
            amplitude = 1.0
            frequency = 1.0
            max_value = 0

            for _ in range(octaves):
                smaller_size = max(1, int(size / frequency))
                noise_layer = np.random.rand(smaller_size, smaller_size)

                from scipy.ndimage import zoom
                zoom_factor = size / smaller_size
                noise_layer = zoom(noise_layer, zoom_factor)
                noise_layer = noise_layer[:size, :size]

                noise += amplitude * noise_layer
                max_value += amplitude
                amplitude *= persistence
                frequency *= 2

            return noise / max_value

        # Generate base terrain using noise
        terrain = generate_perlin_like_noise(size)

        # Create empty mask for all islands
        combined_mask = np.zeros((size, size))

        # Generate random positions for islands
        # Using rejection sampling to ensure islands aren't too close
        min_distance = size * 0.2  # Minimum distance between island centers
        centers = []
        attempts = 0
        max_attempts = 1000

        while len(centers) < num_islands and attempts < max_attempts:
            # Generate random center
            x = np.random.uniform(0, size)
            y = np.random.uniform(0, size)

            # Check distance from other centers
            if not centers or all(np.sqrt((x - cx) ** 2 + (y - cy) ** 2) > min_distance for cx, cy in centers):
                centers.append((x, y))
            attempts += 1

        # Create individual islands
        x_coords = np.linspace(0, size - 1, size)
        y_coords = np.linspace(0, size - 1, size)
        X, Y = np.meshgrid(x_coords, y_coords)

        for center_x, center_y in centers:
            # Random radius for this island
            radius = np.random.uniform(min_radius * size, max_radius * size)

            # Calculate distance from center
            distance = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)

            # Create island mask with random variations
            island_mask = 1 - np.clip(distance / radius, 0, 1)

            # Add some randomness to the coastline
            noise = generate_perlin_like_noise(size) * 0.3
            island_mask = island_mask + noise
            island_mask = np.clip(island_mask, 0, 1)

            # Smooth the mask
            island_mask = gaussian_filter(island_mask, sigma=1)

            # Combine with existing mask, taking maximum value
            combined_mask = np.maximum(combined_mask, island_mask)

        # Apply combined mask to terrain
        terrain = terrain * combined_mask

        # Normalize and scale to max height
        terrain = ((terrain - terrain.min()) / (terrain.max() - terrain.min()) * max_height)

        # Apply threshold to ensure we have some water level
        water_level = 0.15 * max_height
        terrain[terrain < water_level] = 0

        # Round to integers
        terrain = np.round(terrain).astype(int)

        return terrain

    @staticmethod
    def format_map(terrain):
        """
        Formats the terrain array as a string with the specified format.
        """
        return '\n'.join(' '.join(str(cell) for cell in row) for row in terrain)

    @staticmethod
    def generate_distinct_islands_map(size=30, max_height=1000, num_islands=4):
        """
        Generates a map with distinct, complete islands where each island cell
        must be part of a group of at least 10 connected cells.

        Args:
            size (int): Size of the square map (default: 30)
            max_height (int): Maximum terrain height (default: 1000)
            num_islands (int): Number of islands to generate (default: 4)

        Returns:
            str: Formatted string representing the height map
        """

        def generate_noise(size, octaves=4):
            noise = np.zeros((size, size))
            amplitude = 1.0
            frequency = 1.0
            max_value = 0

            for _ in range(octaves):
                smaller_size = max(1, int(size / frequency))
                noise_layer = np.random.rand(smaller_size, smaller_size)

                from scipy.ndimage import zoom
                zoom_factor = size / smaller_size
                noise_layer = zoom(noise_layer, zoom_factor)
                noise_layer = noise_layer[:size, :size]

                noise += amplitude * noise_layer
                max_value += amplitude
                amplitude *= 0.5
                frequency *= 2

            return noise / max_value

        def find_connected_components(terrain, min_group_size=10):
            """
            Finds connected components in the terrain and removes groups smaller than min_group_size.
            Two cells are connected if they share a side.
            """

            def bfs(start_x, start_y, visited):
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-directional connectivity
                component = set()
                queue = deque([(start_x, start_y)])
                component.add((start_x, start_y))
                visited.add((start_x, start_y))

                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        new_x, new_y = x + dx, y + dy
                        if (0 <= new_x < terrain.shape[0] and
                                0 <= new_y < terrain.shape[1] and
                                terrain[new_x, new_y] > 0 and
                                (new_x, new_y) not in visited):
                            queue.append((new_x, new_y))
                            component.add((new_x, new_y))
                            visited.add((new_x, new_y))
                return component

            visited = set()
            terrain_copy = terrain.copy()

            # Find all connected components
            for i in range(terrain.shape[0]):
                for j in range(terrain.shape[1]):
                    if terrain[i, j] > 0 and (i, j) not in visited:
                        component = bfs(i, j, visited)
                        # If component is too small, remove it
                        if len(component) < min_group_size:
                            for x, y in component:
                                terrain_copy[x, y] = 0

            return terrain_copy

        # Define island positions
        regions = [
                      (0.25, 0.25),  # top-left
                      (0.25, 0.75),  # top-right
                      (0.75, 0.25),  # bottom-left
                      (0.75, 0.75),  # bottom-right
                      (0.5, 0.5)  # center (for 5 islands)
                  ][:num_islands]

        # Add some randomness to positions
        positions = []
        for base_x, base_y in regions:
            offset = 0.15
            x = base_x * size + np.random.uniform(-offset * size, offset * size)
            y = base_y * size + np.random.uniform(-offset * size, offset * size)
            positions.append((x, y))

        # Create the terrain
        terrain = np.zeros((size, size))

        # Generate individual islands
        x_coords = np.linspace(0, size - 1, size)
        y_coords = np.linspace(0, size - 1, size)
        X, Y = np.meshgrid(x_coords, y_coords)

        for center_x, center_y in positions:
            distance = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)

            # Make islands slightly larger to ensure enough connected cells
            radius = np.random.uniform(0.18 * size, 0.22 * size)

            island_mask = 1 - np.clip(distance / radius, 0, 1)
            coast_noise = generate_noise(size) * 0.3

            island_mask = island_mask + coast_noise
            island_mask = np.clip(island_mask, 0, 1)
            island_mask = gaussian_filter(island_mask, sigma=0.8)

            height_variation = generate_noise(size)
            island_terrain = height_variation * island_mask

            terrain = np.maximum(terrain, island_terrain)

        # Normalize and scale to max height
        terrain = ((terrain - terrain.min()) / (terrain.max() - terrain.min()) * max_height)

        # Apply threshold to ensure we have some water level
        water_level = 0.2 * max_height
        terrain[terrain < water_level] = 0

        # Round to integers
        terrain = np.round(terrain).astype(int)

        # Remove small disconnected components
        terrain = find_connected_components(terrain, min_group_size=10)

        # Format the map as a string
        return '\n'.join(' '.join(str(cell) for cell in row) for row in terrain)

    # Example usage:
    terrain = generate_archipelago_map(size=30, max_height=1000, num_islands=4)
    formatted_map = format_map(terrain)
    print(formatted_map)

    # Generate and format a map