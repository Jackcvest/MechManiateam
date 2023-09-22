def assert_blob_has_key_of_type(blob, key, expected_type):
    assert key in blob and isinstance(
        blob[key], expected_type
    ), f"{key} should be of type {expected_type.__name__} in blob: {blob}"
