"""Module for caching API check results."""

import time
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from .checker import CheckResult


@dataclass
class CacheEntry:
    """Cache entry."""
    result: CheckResult
    timestamp: float
    ttl: float  # Time to live in seconds


class ResultCache:
    """
    Cache for API check results.
    
    Used to reduce the number of API requests
    and improve performance.
    """
    
    def __init__(self, default_ttl: float = 60.0):
        """
        Initializes cache.
        
        Args:
            default_ttl: Default time to live for cache entries (seconds)
        """
        self._cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
    
    def _make_key(self, name: str, url: str, method: str) -> str:
        """Creates cache key."""
        return f"{method}:{url}:{name}"
    
    def get(self, name: str, url: str, method: str = "GET", ttl: Optional[float] = None) -> Optional[CheckResult]:
        """
        Gets result from cache.
        
        Args:
            name: API name
            url: API URL
            method: HTTP method
            ttl: Time to live for entry (if None, uses TTL from entry or default_ttl)
            
        Returns:
            CheckResult if entry found and not expired, None otherwise
        """
        key = self._make_key(name, url, method)
        entry = self._cache.get(key)
        
        if entry is None:
            return None
        
        # Check if entry expired (use TTL from entry)
        cache_ttl = ttl if ttl is not None else entry.ttl
        if time.time() - entry.timestamp > cache_ttl:
            # Entry expired, remove it
            del self._cache[key]
            return None
        
        return entry.result
    
    def set(self, result: CheckResult, ttl: Optional[float] = None) -> None:
        """
        Saves result to cache.
        
        Args:
            result: API check result
            ttl: Time to live for entry (if None, uses default_ttl)
        """
        key = self._make_key(result.name, result.url, "GET")  # TODO: add method to CheckResult
        cache_ttl = ttl if ttl is not None else self.default_ttl
        
        self._cache[key] = CacheEntry(
            result=result,
            timestamp=time.time(),
            ttl=cache_ttl
        )
    
    def clear(self) -> None:
        """Clears entire cache."""
        self._cache.clear()
    
    def remove(self, name: str, url: str, method: str = "GET") -> None:
        """
        Removes specific entry from cache.
        
        Args:
            name: API name
            url: API URL
            method: HTTP method
        """
        key = self._make_key(name, url, method)
        self._cache.pop(key, None)
    
    def cleanup_expired(self) -> int:
        """
        Removes expired entries from cache.
        
        Returns:
            Number of removed entries
        """
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self._cache.items():
            if current_time - entry.timestamp > entry.ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self._cache[key]
        
        return len(expired_keys)
    
    def size(self) -> int:
        """Returns number of entries in cache."""
        return len(self._cache)
    
    def stats(self) -> Dict[str, any]:
        """
        Returns cache statistics.
        
        Returns:
            Dictionary with statistics
        """
        current_time = time.time()
        expired_count = 0
        valid_count = 0
        
        for entry in self._cache.values():
            if current_time - entry.timestamp > entry.ttl:
                expired_count += 1
            else:
                valid_count += 1
        
        return {
            'total': len(self._cache),
            'valid': valid_count,
            'expired': expired_count,
            'default_ttl': self.default_ttl
        }
