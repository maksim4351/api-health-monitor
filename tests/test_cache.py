"""Tests for caching module."""

import pytest
import time
from api_monitor.cache import ResultCache, CacheEntry
from api_monitor.checker import CheckResult


class TestResultCache:
    """Tests for ResultCache."""
    
    def test_cache_init(self):
        """Test cache initialization."""
        cache = ResultCache(default_ttl=60.0)
        assert cache.default_ttl == 60.0
        assert cache.size() == 0
    
    def test_cache_set_get(self):
        """Test saving and retrieving from cache."""
        cache = ResultCache(default_ttl=60.0)
        result = CheckResult(
            name='Test API',
            url='https://test.com',
            status_code=200,
            latency_ms=100.5,
            success=True
        )
        
        cache.set(result)
        cached = cache.get('Test API', 'https://test.com')
        
        assert cached is not None
        assert cached.name == result.name
        assert cached.url == result.url
        assert cached.status_code == result.status_code
        assert cached.latency_ms == result.latency_ms
        assert cached.success == result.success
    
    def test_cache_expiration(self):
        """Test cache entry expiration."""
        cache = ResultCache(default_ttl=0.1)  # Very short TTL
        result = CheckResult(
            name='Test API',
            url='https://test.com',
            status_code=200,
            latency_ms=100.5,
            success=True
        )
        
        cache.set(result)
        assert cache.get('Test API', 'https://test.com') is not None
        
        # Wait for expiration
        time.sleep(0.2)
        assert cache.get('Test API', 'https://test.com') is None
    
    def test_cache_clear(self):
        """Test cache clearing."""
        cache = ResultCache()
        result = CheckResult('Test', 'https://test.com', 200, 100.0, True)
        
        cache.set(result)
        assert cache.size() == 1
        
        cache.clear()
        assert cache.size() == 0
    
    def test_cache_remove(self):
        """Test removing specific entry."""
        cache = ResultCache()
        result1 = CheckResult('API1', 'https://api1.com', 200, 100.0, True)
        result2 = CheckResult('API2', 'https://api2.com', 200, 100.0, True)
        
        cache.set(result1)
        cache.set(result2)
        assert cache.size() == 2
        
        cache.remove('API1', 'https://api1.com')
        assert cache.size() == 1
        assert cache.get('API1', 'https://api1.com') is None
        assert cache.get('API2', 'https://api2.com') is not None
    
    def test_cache_cleanup_expired(self):
        """Test cleanup of expired entries."""
        cache = ResultCache(default_ttl=10.0)  # Long default TTL
        result1 = CheckResult('API1', 'https://api1.com', 200, 100.0, True)
        result2 = CheckResult('API2', 'https://api2.com', 200, 100.0, True)
        
        cache.set(result1, ttl=0.1)  # Short TTL
        cache.set(result2, ttl=10.0)  # Long TTL
        
        time.sleep(0.2)
        
        removed = cache.cleanup_expired()
        assert removed == 1
        assert cache.size() == 1
        # API2 should remain, as it has long TTL
        cached = cache.get('API2', 'https://api2.com')
        assert cached is not None
    
    def test_cache_stats(self):
        """Test cache statistics."""
        cache = ResultCache(default_ttl=60.0)
        result = CheckResult('Test', 'https://test.com', 200, 100.0, True)
        
        cache.set(result)
        stats = cache.stats()
        
        assert stats['total'] == 1
        assert stats['valid'] == 1
        assert stats['expired'] == 0
        assert stats['default_ttl'] == 60.0
    
    def test_cache_different_methods(self):
        """Test cache with different HTTP methods."""
        cache = ResultCache()
        result_get = CheckResult('API', 'https://api.com', 200, 100.0, True)
        result_post = CheckResult('API', 'https://api.com', 201, 150.0, True)
        
        cache.set(result_get)
        cached_get = cache.get('API', 'https://api.com', 'GET')
        cached_post = cache.get('API', 'https://api.com', 'POST')
        
        # GET should be in cache, POST should not (different methods)
        assert cached_get is not None
        assert cached_post is None
    
    def test_cache_custom_ttl(self):
        """Test cache with custom TTL."""
        cache = ResultCache(default_ttl=60.0)
        result = CheckResult('Test', 'https://test.com', 200, 100.0, True)
        
        cache.set(result, ttl=0.1)  # Set short TTL
        assert cache.get('Test', 'https://test.com') is not None
        
        # Wait for TTL expiration
        time.sleep(0.2)
        # Now entry should expire
        cached = cache.get('Test', 'https://test.com')
        assert cached is None
