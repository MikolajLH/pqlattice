from typing import overload

from ..typing import Matrix, Vector


class LWR:
    def __init__(self):
        """_summary_

        Raises
        ------
        NotImplementedError
            _description_
        """
        raise NotImplementedError()

    @overload
    def __call__(self, n: int) -> Matrix: ...

    @overload
    def __call__(self, n: None) -> Vector: ...

    def __call__(self, n: int | None = None) -> Matrix | Vector:
        """_summary_

        Parameters
        ----------
        n : int | None, optional
            _description_, by default None

        Returns
        -------
        Matrix | Vector
            _description_

        Raises
        ------
        NotImplementedError
            _description_
        """
        raise NotImplementedError()
