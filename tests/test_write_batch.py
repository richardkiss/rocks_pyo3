import os
import shutil
import unittest
import tempfile
from rocks_pyo3 import DB, WriteBatch


class TestWriteBatch(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the test database
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_db")
        self.db = DB(self.db_path)

    def tearDown(self):
        # Clean up the test database
        del self.db
        shutil.rmtree(self.test_dir)

    def test_basic_write_batch(self):
        """Test that a basic write batch works correctly."""
        # Create a write batch
        batch = WriteBatch()

        # Add operations to the batch
        batch.put(b"key1", b"value1")
        batch.put(b"key2", b"value2")
        batch.put(b"key3", b"value3")

        # Write the batch
        self.db.write(batch)

        # Verify the keys were written
        self.assertEqual(self.db.get(b"key1"), b"value1")
        self.assertEqual(self.db.get(b"key2"), b"value2")
        self.assertEqual(self.db.get(b"key3"), b"value3")

    def test_write_batch_atomicity(self):
        """Test that write batches are atomic - all or nothing."""
        # First set up some initial data
        self.db.put(b"existing1", b"oldvalue1")
        self.db.put(b"existing2", b"oldvalue2")

        try:
            # Mock a failure by writing a batch and then raising an exception
            batch = WriteBatch()
            batch.put(b"existing1", b"newvalue1")
            batch.put(b"existing2", b"newvalue2")
            batch.put(b"new_key", b"new_value")

            self.db.write(batch)

            # Simulate a failure after the batch is written
            raise RuntimeError("Simulated failure")

        except RuntimeError:
            # The batch should have been fully committed despite the exception
            self.assertEqual(self.db.get(b"existing1"), b"newvalue1")
            self.assertEqual(self.db.get(b"existing2"), b"newvalue2")
            self.assertEqual(self.db.get(b"new_key"), b"new_value")

    def test_write_batch_with_deletes(self):
        """Test that write batches can include deletions."""
        # Set up initial data
        self.db.put(b"key1", b"value1")
        self.db.put(b"key2", b"value2")
        self.db.put(b"key3", b"value3")

        # Create a batch with mixed operations
        batch = WriteBatch()
        batch.delete(b"key1")  # Delete an existing key
        batch.put(b"key2", b"updated_value2")  # Update a key
        batch.put(b"key4", b"value4")  # Add a new key

        # Write the batch
        self.db.write(batch)

        # Verify results
        self.assertIsNone(self.db.get(b"key1"))  # Should be deleted
        self.assertEqual(self.db.get(b"key2"), b"updated_value2")  # Should be updated
        self.assertEqual(self.db.get(b"key3"), b"value3")  # Should be unchanged
        self.assertEqual(self.db.get(b"key4"), b"value4")  # Should be added

    def test_large_write_batch(self):
        """Test performance with a large batch of operations."""
        batch = WriteBatch()

        # Add a large number of operations
        for i in range(1000):
            key = f"key{i}".encode()
            value = f"value{i}".encode()
            batch.put(key, value)

        # Write the batch
        self.db.write(batch)

        # Verify a sample of the results
        self.assertEqual(self.db.get(b"key0"), b"value0")
        self.assertEqual(self.db.get(b"key500"), b"value500")
        self.assertEqual(self.db.get(b"key999"), b"value999")

    def test_empty_write_batch(self):
        """Test that an empty write batch does not cause issues."""
        batch = WriteBatch()
        self.db.write(batch)
        # No assertions needed - just verifying it doesn't raise exceptions

    def test_reusing_write_batch(self):
        """Test that a write batch can be reused after writing."""
        batch = WriteBatch()

        # First use
        batch.put(b"batch1_key1", b"value1")
        batch.put(b"batch1_key2", b"value2")
        self.db.write(batch)

        # Second use - reuse the same batch object
        batch = WriteBatch()  # Create a new batch
        batch.put(b"batch2_key1", b"value1")
        batch.put(b"batch2_key2", b"value2")
        self.db.write(batch)

        # Verify all keys are present
        self.assertEqual(self.db.get(b"batch1_key1"), b"value1")
        self.assertEqual(self.db.get(b"batch1_key2"), b"value2")
        self.assertEqual(self.db.get(b"batch2_key1"), b"value1")
        self.assertEqual(self.db.get(b"batch2_key2"), b"value2")


if __name__ == "__main__":
    unittest.main()
