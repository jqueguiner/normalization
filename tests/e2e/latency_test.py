import time

import pytest

from normalization.languages.registry import get_language_registry
from normalization.pipeline.loader import load_pipeline

_ITERATIONS = 300
_MAX_TOTAL_SECONDS = 5.0
_SAMPLE_TEXT = "I love gladia S.T.T."

_LANGUAGE_CODES = sorted(code for code in get_language_registry())


@pytest.mark.parametrize("language", _LANGUAGE_CODES)
def test_gladia_3_latency(language: str) -> None:
    pipeline = load_pipeline("gladia-3", language)

    start_time = time.time()
    for _ in range(_ITERATIONS):
        pipeline.normalize(_SAMPLE_TEXT)
        if time.time() - start_time > _MAX_TOTAL_SECONDS:
            break
    elapsed = time.time() - start_time

    print(
        f"\nLatency ({language}): {elapsed:.3f}s for {_ITERATIONS} iterations "
        f"({elapsed / _ITERATIONS * 1000:.2f}ms/call)"
    )
    assert elapsed < _MAX_TOTAL_SECONDS, (
        f"[{language}] {_ITERATIONS} normalizations took {elapsed:.2f}s "
        f"(limit: {_MAX_TOTAL_SECONDS}s)"
    )
