# MCP Protocol IoT Control Usage Guide

> This document describes how to implement IoT control of ESP32 devices based on the MCP protocol. For a detailed protocol flow, please refer to [`mcp-protocol.md`](./mcp-protocol.md).

## Introduction

MCP (Model Context Protocol) is a new generation protocol recommended for IoT control. It enables flexible device control by discovering and invoking "Tools" between the backend and the device using the standard JSON-RPC 2.0 format.

## Typical Usage Flow

1. After the device starts, it establishes a connection with the backend through a base protocol (e.g., WebSocket/MQTT).
2. The backend initializes the session using the `initialize` method of the MCP protocol.
3. The backend uses `tools/list` to get all the tools (functions) and their parameter descriptions supported by the device.
4. The backend calls specific tools using `tools/call` to control the device.

For detailed protocol format and interaction, please see [`mcp-protocol.md`](./mcp-protocol.md).

## Device-side Tool Registration Method

The device registers "tools" that can be called by the backend using the `McpServer::AddTool` method. Its common function signature is as follows:

```cpp
void AddTool(
    const std::string& name,           // Tool name, recommended to be unique and hierarchical, e.g., self.dog.forward
    const std::string& description,    // Tool description, a brief explanation of the function for easy understanding by large models
    const PropertyList& properties,    // List of input parameters (can be empty), supported types: boolean, integer, string
    std::function<ReturnValue(const PropertyList&)> callback // Callback implementation when the tool is called
);
```
- `name`: Unique identifier for the tool. A "module.function" naming style is recommended.
- `description`: A natural language description for easy understanding by AI/users.
- `properties`: A list of parameters. Supported types are boolean, integer, and string. Ranges and default values can be specified.
- `callback`: The actual execution logic when a call request is received. The return value can be bool/int/string.

## Typical Registration Example (Using ESP-Hi as an example)

```cpp
void InitializeTools() {
    auto& mcp_server = McpServer::GetInstance();
    // Example 1: No parameters, control the robot to move forward
    mcp_server.AddTool("self.dog.forward", "Move the robot forward", PropertyList(), [this](const PropertyList&) -> ReturnValue {
        servo_dog_ctrl_send(DOG_STATE_FORWARD, NULL);
        return true;
    });
    // Example 2: With parameters, set the RGB color of the light
    mcp_server.AddTool("self.light.set_rgb", "Set RGB color", PropertyList({
        Property("r", kPropertyTypeInteger, 0, 255),
        Property("g", kPropertyTypeInteger, 0, 255),
        Property("b", kPropertyTypeInteger, 0, 255)
    }), [this](const PropertyList& properties) -> ReturnValue {
        int r = properties["r"].value<int>();
        int g = properties["g"].value<int>();
        int b = properties["b"].value<int>();
        led_on_ = true;
        SetLedColor(r, g, b);
        return true;
    });
}
```

## Common Tool Call JSON-RPC Examples

### 1. Get Tool List
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": { "cursor": "" },
  "id": 1
}
```

### 2. Control Chassis to Move Forward
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.chassis.go_forward",
    "arguments": {}
  },
  "id": 2
}
```

### 3. Switch Light Mode
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.chassis.switch_light_mode",
    "arguments": { "light_mode": 3 }
  },
  "id": 3
}
```

### 4. Flip Camera
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.camera.set_camera_flipped",
    "arguments": {}
  },
  "id": 4
}
```

## Notes
- The tool names, parameters, and return values are subject to the registration on the device side via `AddTool`.
- It is recommended that all new projects use the MCP protocol for IoT control.
- For detailed protocol and advanced usage, please refer to [`mcp-protocol.md`](./mcp-protocol.md).
