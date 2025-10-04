{ pkgs, ... }: {
  # Which nixpkgs channel to use. Using unstable for more recent packages.
  channel = "unstable";

  # Packages to be installed in the environment.
  packages = [
    # Create a Python environment with fastapi and uvicorn
    (pkgs.python3.withPackages (ps: [
      ps.fastapi
      ps.uvicorn
    ]))
  ];

  # Environment variables
  env = { };

  idx = {
    # Recommended extensions for this project
    extensions = [
      "ms-python.python"
    ];

    # Previews configuration to auto-start the server
    previews = {
      "mcp-server" = {
        name = "MCP Server";
        command = "uvicorn MCP-Server.main:app --host 0.0.0.0 --port 8000";
        manager = "web";
        port = 8000;
      };
    };
    
    # Workspace lifecycle hooks
    workspace = {
      # The onCreate hook is no longer needed as Nix now manages the packages directly.
    };
  };
}
