import os
import pickle
from abc import ABC, abstractmethod


class TrajectoryBase(ABC):
    def __init__(self, **kwargs):
        """Base class for all trajectories and distributions used in GravNN"""
        # positions
        self.file_directory = (
            os.path.splitext(__file__)[0] + "/../../Files/Trajectories/"
        )
        self.generate_full_file_directory()
        self.load(override=kwargs.get("override", [False])[0])
        return

    def save(self):
        """Save the distribution positions in the directory generated by `generate_full_file_directory`."""
        if not os.path.exists(self.file_directory):
            os.makedirs(self.file_directory, exist_ok=True)
        with open(self.file_directory + "trajectory.data", "wb") as f:
            pickle.dump(self.positions, f)
            try:
                pickle.dump(self.times, f)
            except:
                pass
        return

    def load(self, override=False):
        """Load the distribution if it exists, or generate (and then save) a new distribution

        Args:
            override (bool, optional): Flag to determine if the existing file should be overridden. Defaults to False.

        Returns:
            np.array: cartesian position vectors of distribution
        """
        # Check if the file exists and either load the positions or generate the position
        if os.path.exists(self.file_directory + "trajectory.data") and not override:
            with open(self.file_directory + "trajectory.data", "rb") as f:
                self.positions = pickle.load(f)
                try:
                    self.times = pickle.load(f)
                except:
                    pass
            return self.positions

        else:
            self.generate()
            self.save()
            return self.positions

    @abstractmethod
    def generate_full_file_directory(self):
        """Generate the file directory path in which the distribution will be saved"""
        pass

    @abstractmethod
    def generate(self):
        """Generate the cartesian positions of the distribution"""
        pass
