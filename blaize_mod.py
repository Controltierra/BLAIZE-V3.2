#!/usr/bin/env python3
"""
BLAIZE MOD Processing System
Version 3.2

A modular processing framework for BLAIZE operations.
"""

import json
import sys
from typing import Dict, List, Any
from datetime import datetime


class BlaizeMod:
    """Main BLAIZE MOD processor class."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize BLAIZE MOD processor.
        
        Args:
            config: Configuration dictionary for MOD settings
        """
        self.config = config or {}
        self.version = "3.2"
        self.modules = []
        self.processing_log = []
        self.enable_console_logging = True
        self.max_log_entries = 1000
        
    def load_config(self, config_file: str):
        """
        Load configuration from a JSON file and register modules.
        
        Args:
            config_file: Path to configuration file
        """
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            # Extract BLAIZE MOD configuration
            if 'blaize_mod' in config_data:
                blaize_config = config_data['blaize_mod']
                self.config = blaize_config
                
                # Apply settings
                if 'settings' in blaize_config:
                    settings = blaize_config['settings']
                    self.enable_console_logging = settings.get('enable_logging', True)
                    self.max_log_entries = settings.get('max_log_entries', 1000)
                
                # Register modules from config
                if 'modules' in blaize_config:
                    for module_def in blaize_config['modules']:
                        if module_def.get('enabled', True):
                            self.register_module(
                                module_def['name'],
                                module_def.get('config', {})
                            )
            else:
                self.config = config_data
                
            self.log(f"Configuration loaded from {config_file}")
            
        except FileNotFoundError:
            self.log(f"Configuration file not found: {config_file}", level="ERROR")
        except json.JSONDecodeError as e:
            self.log(f"Invalid JSON in configuration file: {e}", level="ERROR")
        except PermissionError:
            self.log(f"Permission denied reading configuration file: {config_file}", level="ERROR")
        except Exception as e:
            self.log(f"Error loading configuration: {e}", level="ERROR")
            
    def register_module(self, module_name: str, module_config: Dict[str, Any] = None):
        """
        Register a processing module.
        
        Args:
            module_name: Name of the module
            module_config: Module-specific configuration
        """
        module = {
            "name": module_name,
            "config": module_config or {},
            "enabled": True,
            "registered_at": datetime.now().isoformat()
        }
        self.modules.append(module)
        self.log(f"Module '{module_name}' registered")
        
    def process(self, data: Any) -> Dict[str, Any]:
        """
        Process data through all enabled modules.
        
        Args:
            data: Input data to process
            
        Returns:
            Processing results
        """
        self.log("Starting BLAIZE MOD processing")
        results = {
            "status": "success",
            "version": self.version,
            "input": data,
            "module_results": [],
            "timestamp": datetime.now().isoformat()
        }
        
        if not self.modules:
            self.log("No modules registered", level="WARNING")
            results["status"] = "warning"
            results["message"] = "No modules registered for processing"
            return results
            
        for module in self.modules:
            if module["enabled"]:
                self.log(f"Processing through module: {module['name']}")
                module_result = self._process_module(module, data)
                results["module_results"].append(module_result)
                
        self.log("BLAIZE MOD processing completed")
        return results
        
    def _process_module(self, module: Dict[str, Any], data: Any) -> Dict[str, Any]:
        """
        Process data through a specific module.
        
        Args:
            module: Module configuration
            data: Input data
            
        Returns:
            Module processing result
        """
        # Placeholder for module-specific processing logic
        return {
            "module": module["name"],
            "status": "processed",
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
    def log(self, message: str, level: str = "INFO"):
        """
        Log a processing event.
        
        Args:
            message: Log message
            level: Log level (INFO, WARNING, ERROR)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        self.processing_log.append(log_entry)
        
        # Enforce max log entries limit
        if len(self.processing_log) > self.max_log_entries:
            self.processing_log.pop(0)
        
        # Print to console if enabled
        if self.enable_console_logging:
            print(f"[{level}] {message}")
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get current processor status.
        
        Returns:
            Status information
        """
        return {
            "version": self.version,
            "modules_registered": len(self.modules),
            "modules_enabled": sum(1 for m in self.modules if m["enabled"]),
            "modules": [{"name": m["name"], "enabled": m["enabled"]} for m in self.modules],
            "log_entries": len(self.processing_log)
        }
        
    def export_log(self, filename: str):
        """
        Export processing log to a file.
        
        Args:
            filename: Output filename
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.processing_log, f, indent=2)
            # Log after export to avoid recursive logging in the exported file
            if self.enable_console_logging:
                print(f"[INFO] Log exported to {filename}")
        except FileNotFoundError:
            self.log(f"Directory not found for log export: {filename}", level="ERROR")
        except PermissionError:
            self.log(f"Permission denied writing log file: {filename}", level="ERROR")
        except Exception as e:
            self.log(f"Error exporting log: {e}", level="ERROR")


def main():
    """Main entry point for BLAIZE MOD processing."""
    print("=" * 50)
    print("BLAIZE MOD Processing System v3.2")
    print("=" * 50)
    
    # Initialize processor
    processor = BlaizeMod()
    
    # Register default modules
    processor.register_module("DataValidator")
    processor.register_module("DataTransformer")
    processor.register_module("DataExporter")
    
    # Example processing
    sample_data = {
        "type": "sample",
        "content": "BLAIZE MOD test data",
        "version": "3.2"
    }
    
    # Process data
    results = processor.process(sample_data)
    
    # Display results
    print("\n" + "=" * 50)
    print("Processing Results:")
    print("=" * 50)
    print(json.dumps(results, indent=2))
    
    # Display status
    print("\n" + "=" * 50)
    print("System Status:")
    print("=" * 50)
    print(json.dumps(processor.get_status(), indent=2))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
