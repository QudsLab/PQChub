"""
PQChub Python Wrapper - Main PQC Library Interface
"""

import ctypes
import os
from pathlib import Path
from typing import Optional, Tuple

from .utils import (
    find_binary_path, 
    PQCError, 
    PQCLibraryError,
    get_platform_info
)


class PQCLibrary:
    """Main interface to the PQC native library"""
    
    def __init__(self, binary_path: Optional[str] = None):
        """
        Initialize the PQC library wrapper
        
        Args:
            binary_path: Optional custom path to the native library
        """
        self.binary_path = find_binary_path(binary_path)
        self._lib = None
        self._load_library()
    
    def _load_library(self):
        """Load the native PQC library"""
        try:
            self._lib = ctypes.CDLL(self.binary_path)
        except OSError as e:
            raise PQCLibraryError(
                f"Failed to load PQC library from {self.binary_path}: {e}"
            ) from e
    
    @property
    def lib(self):
        """Get the loaded ctypes library"""
        if self._lib is None:
            raise PQCLibraryError("Library not loaded")
        return self._lib
    
    def get_version(self) -> str:
        """Get the library version"""
        try:
            func = self.lib.pqchub_get_version
            func.restype = ctypes.c_char_p
            result = func()
            return result.decode('utf-8') if result else "Unknown"
        except AttributeError:
            return "Unknown (function not available)"
    
    def get_algorithms(self) -> str:
        """Get supported algorithms"""
        try:
            func = self.lib.pqchub_get_algorithms
            func.restype = ctypes.c_char_p
            result = func()
            return result.decode('utf-8') if result else "Unknown"
        except AttributeError:
            return "Unknown (function not available)"
    
    def get_platform_info(self) -> dict:
        """Get platform and library information"""
        system, arch = get_platform_info()
        return {
            'system': system,
            'architecture': arch,
            'binary_path': self.binary_path,
            'version': self.get_version(),
            'algorithms': self.get_algorithms().split(','),
        }


# Global library instance
_global_lib: Optional[PQCLibrary] = None


def get_library(binary_path: Optional[str] = None) -> PQCLibrary:
    """Get the global library instance"""
    global _global_lib
    
    if _global_lib is None or binary_path is not None:
        _global_lib = PQCLibrary(binary_path)
    
    return _global_lib


def check_library_function(lib: PQCLibrary, func_name: str) -> bool:
    """Check if a library function is available"""
    try:
        getattr(lib.lib, func_name)
        return True
    except AttributeError:
        return False


class BasePQC:
    """Base class for all PQC algorithms"""
    
    def __init__(self, binary_path: Optional[str] = None):
        self.lib = get_library(binary_path)
        self._check_functions()
    
    def _check_functions(self):
        """Check that required functions are available"""
        for func_name in self.get_required_functions():
            if not check_library_function(self.lib, func_name):
                raise PQCLibraryError(
                    f"Required function '{func_name}' not found in library. "
                    f"Make sure you have the correct binary for your platform."
                )
    
    def get_required_functions(self) -> list:
        """Get list of required function names (to be overridden)"""
        return []
    
    def _call_function(self, func_name: str, *args, **kwargs):
        """Call a library function with error handling"""
        try:
            func = getattr(self.lib.lib, func_name)
            return func(*args, **kwargs)
        except AttributeError as e:
            raise PQCLibraryError(f"Function {func_name} not found") from e
        except OSError as e:
            raise PQCLibraryError(f"Error calling {func_name}: {e}") from e