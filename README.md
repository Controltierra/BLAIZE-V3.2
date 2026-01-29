# BLAIZE-V3.2
MOD BLAIZE PROCESSING

## Overview

BLAIZE-V3.2 is a modular processing framework designed for flexible data processing operations. The system provides a plugin-based architecture that allows you to register and execute multiple processing modules in sequence.

**Note**: This is a framework skeleton. The current implementation provides the module management infrastructure and processing pipeline. Module-specific processing logic can be extended by subclassing `BlaizeMod` and overriding the `_process_module` method to implement custom processing operations.

## Features

- **Modular Architecture**: Register and manage multiple processing modules
- **Configuration Support**: JSON-based configuration for modules and settings
- **Processing Pipeline**: Sequential processing through enabled modules
- **Logging System**: Comprehensive logging of all processing operations
- **Status Monitoring**: Real-time status information about registered modules

## Installation

No special installation required. Simply ensure you have Python 3.6+ installed:

```bash
python3 --version
```

## Quick Start

### Basic Usage

Run the BLAIZE MOD processor with default configuration:

```bash
python3 blaize_mod.py
```

### Using Custom Configuration

1. Create or modify `config.json` with your module settings
2. The configuration file will automatically register modules when loaded:

```python
from blaize_mod import BlaizeMod

# Initialize and load config (modules are auto-registered)
processor = BlaizeMod()
processor.load_config('config.json')

# Process your data - modules from config are ready
results = processor.process(your_data)
```

## Configuration

The system uses a JSON configuration file (`config.json`) to define:

- **Modules**: Processing modules and their configurations
- **Settings**: System-wide settings like logging level
- **Module Configs**: Module-specific parameters

Example configuration structure:

```json
{
  "blaize_mod": {
    "version": "3.2",
    "modules": [
      {
        "name": "DataValidator",
        "enabled": true,
        "config": {}
      }
    ],
    "settings": {
      "log_level": "INFO",
      "enable_logging": true
    }
  }
}
```

## Module System

### Registering Modules

```python
processor = BlaizeMod()
processor.register_module("CustomModule", {"param": "value"})
```

### Available Default Modules

1. **DataValidator**: Validates input data
2. **DataTransformer**: Transforms data format
3. **DataExporter**: Exports processed data

## API Reference

### BlaizeMod Class

#### Methods

- `__init__(config=None)`: Initialize processor with optional config dictionary
- `load_config(config_file)`: Load configuration from file and auto-register modules
- `register_module(name, config)`: Manually register a processing module
- `process(data)`: Process data through all enabled modules
- `get_status()`: Get current system status
- `export_log(filename)`: Export processing log to file

## Processing Flow

1. Initialize BlaizeMod processor
2. Register processing modules (or load from config)
3. Submit data for processing
4. Data flows through each enabled module sequentially
5. Results are returned with module outputs and metadata

## Example

```python
from blaize_mod import BlaizeMod

# Create processor
processor = BlaizeMod()

# Register modules
processor.register_module("DataValidator")
processor.register_module("DataTransformer")

# Process data
data = {"content": "test data"}
results = processor.process(data)

# Check status
status = processor.get_status()
print(status)
```

## Version

Current version: **3.2**

## License

This project is part of the BLAIZE processing system.
