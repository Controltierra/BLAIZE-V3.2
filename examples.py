#!/usr/bin/env python3
"""
Example usage of BLAIZE MOD Processing System
Demonstrates various features and capabilities
"""

from blaize_mod import BlaizeMod
import json


def example_basic_usage():
    """Basic usage example."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    processor = BlaizeMod()
    processor.register_module("Validator")
    processor.register_module("Processor")
    
    data = {"message": "Hello BLAIZE!", "value": 42}
    results = processor.process(data)
    
    print(json.dumps(results, indent=2))


def example_with_config():
    """Example using configuration file."""
    print("\n" + "=" * 60)
    print("Example 2: Using Configuration File")
    print("=" * 60)
    
    processor = BlaizeMod()
    processor.load_config("config.json")
    
    # Process multiple items
    items = [
        {"id": 1, "data": "First item"},
        {"id": 2, "data": "Second item"},
        {"id": 3, "data": "Third item"}
    ]
    
    for item in items:
        print(f"\nProcessing item {item['id']}...")
        results = processor.process(item)
        print(f"Status: {results['status']}")


def example_custom_modules():
    """Example with custom module configuration."""
    print("\n" + "=" * 60)
    print("Example 3: Custom Module Configuration")
    print("=" * 60)
    
    processor = BlaizeMod()
    
    # Register modules with custom configs
    processor.register_module("DataCleaner", {
        "remove_nulls": True,
        "trim_whitespace": True
    })
    
    processor.register_module("DataEnricher", {
        "add_timestamp": True,
        "add_metadata": True
    })
    
    processor.register_module("DataValidator", {
        "strict_mode": True,
        "validate_types": True
    })
    
    data = {
        "user": "test_user",
        "action": "process",
        "payload": {"key": "value"}
    }
    
    results = processor.process(data)
    print(json.dumps(results, indent=2))
    
    # Show status
    print("\nProcessor Status:")
    print(json.dumps(processor.get_status(), indent=2))


def example_log_export():
    """Example showing log export."""
    print("\n" + "=" * 60)
    print("Example 4: Log Export")
    print("=" * 60)
    
    processor = BlaizeMod()
    processor.register_module("Logger")
    
    # Process some data
    processor.process({"test": "data1"})
    processor.process({"test": "data2"})
    processor.process({"test": "data3"})
    
    # Export log
    processor.export_log("processing_log.json")
    print("Log exported to processing_log.json")


if __name__ == "__main__":
    print("BLAIZE MOD v3.2 - Example Usage")
    print("=" * 60)
    
    try:
        example_basic_usage()
        example_with_config()
        example_custom_modules()
        example_log_export()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()
