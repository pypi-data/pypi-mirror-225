from processview.core.dataset import Dataset


class TomwerObject(Dataset):
    """Common tomwer object"""

    def __init__(self) -> None:
        super().__init__()
        self._cast_volume = None

    def _clear_heavy_cache(self):
        """util function to clear some heavy object from the cache"""
        raise NotImplementedError()

    def clear_caches(self):
        pass

    @property
    def cast_volume(self):
        # for now this is used as an east way to cache the identifier and provide it to the remaining of the orange canvas.
        # but this is a wrong designa and should be removed at one point.
        return self._cast_volume

    @cast_volume.setter
    def cast_volume(self, volume):
        from tomwer.core.volume.volumebase import TomwerVolumeBase

        if not isinstance(volume, TomwerVolumeBase):
            from tomwer.core.volume.volumefactory import (
                VolumeFactory,
            )  # avoid cyclic import

            volume = VolumeFactory.create_tomo_object_from_identifier(identifier=volume)
        self._cast_volume = volume
