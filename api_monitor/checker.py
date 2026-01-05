"""Module for checking API availability."""

import time
import requests
from typing import Dict, Any, Optional, List, TYPE_CHECKING
from dataclasses import dataclass
from .loader import APIConfig

# Import for type hints
if TYPE_CHECKING:
    from .cache import ResultCache


@dataclass
class CheckResult:
    """Result of checking a single API."""
    name: str
    url: str
    status_code: Optional[int]
    latency_ms: float
    success: bool
    error: Optional[str] = None
    timeout: bool = False


def check_api(api_config: APIConfig) -> CheckResult:
    """
    Checks API availability.
    
    Args:
        api_config: API configuration to check
        
    Returns:
        CheckResult with check results
    """
    start_time = time.time()
    status_code = None
    error = None
    timeout_occurred = False
    
    try:
        response = requests.request(
            method=api_config.method,
            url=api_config.url,
            headers=api_config.headers,
            timeout=api_config.timeout
        )
        status_code = response.status_code
        latency_ms = (time.time() - start_time) * 1000
        
        success = status_code == api_config.expected_status
        
    except requests.exceptions.Timeout:
        latency_ms = (time.time() - start_time) * 1000
        timeout_occurred = True
        error = f"Timeout after {api_config.timeout}s"
        success = False
        
    except requests.exceptions.ConnectionError:
        latency_ms = (time.time() - start_time) * 1000
        error = "Connection error"
        success = False
        
    except requests.exceptions.RequestException as e:
        latency_ms = (time.time() - start_time) * 1000
        error = str(e)
        success = False
        
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        error = f"Unexpected error: {str(e)}"
        success = False
    
    return CheckResult(
        name=api_config.name,
        url=api_config.url,
        status_code=status_code,
        latency_ms=round(latency_ms, 2),
        success=success,
        error=error,
        timeout=timeout_occurred
    )


def check_all_apis(api_configs: List[APIConfig], cache: Optional['ResultCache'] = None, use_async: bool = False) -> List[CheckResult]:
    """
    Checks all APIs from the configuration list.
    
    Args:
        api_configs: List of API configurations
        cache: Optional cache for results (ResultCache)
        use_async: Use async requests (requires additional dependencies)
        
    Returns:
        List of check results
    """
    if use_async:
        return _check_all_apis_async(api_configs, cache)
    
    results = []
    for api_config in api_configs:
        # Check cache
        if cache:
            cached_result = cache.get(api_config.name, api_config.url, api_config.method)
            if cached_result:
                results.append(cached_result)
                continue
        
        # Perform check
        result = check_api(api_config)
        results.append(result)
        
        # Save to cache (only successful results)
        if cache and result.success:
            cache.set(result)
    
    return results


def _check_all_apis_async(api_configs: List[APIConfig], cache: Optional['ResultCache'] = None) -> List[CheckResult]:
    """
    Async check of all APIs (uses threading for parallelism).
    
    Args:
        api_configs: List of API configurations
        cache: Optional cache for results
        
    Returns:
        List of check results
    """
    import concurrent.futures
    from threading import Lock
    
    results = []
    results_lock = Lock()
    
    def check_with_cache(api_config: APIConfig) -> CheckResult:
        """Checks one API considering cache."""
        # Check cache
        if cache:
            cached_result = cache.get(api_config.name, api_config.url, api_config.method)
            if cached_result:
                return cached_result
        
        # Perform check
        result = check_api(api_config)
        
        # Save to cache (only successful results)
        if cache and result.success:
            cache.set(result)
        
        return result
    
    # Use ThreadPoolExecutor for parallel requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, len(api_configs))) as executor:
        future_to_api = {executor.submit(check_with_cache, api_config): api_config for api_config in api_configs}
        
        for future in concurrent.futures.as_completed(future_to_api):
            try:
                result = future.result()
                with results_lock:
                    results.append(result)
            except Exception as e:
                api_config = future_to_api[future]
                error_result = CheckResult(
                    name=api_config.name,
                    url=api_config.url,
                    status_code=None,
                    latency_ms=0.0,
                    success=False,
                    error=f"Error during check: {str(e)}"
                )
                with results_lock:
                    results.append(error_result)
    
    # Sort results in the same order as input configurations
    result_map = {r.name: r for r in results}
    sorted_results = [result_map.get(api.name) for api in api_configs if api.name in result_map]
    
    return sorted_results if sorted_results else results

