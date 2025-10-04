{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "unstable";

  # Packages to be installed in the environment.
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
  ];

  # Environment variables
  env = { };

  idx = {
    # Recommended extensions for this project
    extensions = [
      "ms-python.python"
    ];

    # Workspace lifecycle hooks
    workspace = {
      # On start of the workspace, create a virtual environment and install dependencies
      onCreate = {
        # Using a raw string to avoid issues with backslashes
        python = ''
          if [ ! -d ".venv" ]; then
            ${pkgs.python311}/bin/python3 -m venv .venv
          fi
          . .venv/bin/activate
          pip install -r MCP-Server/requirements.txt
        '';
      };

      # On file change, re-run the installation
      onFileChange = {
        # Using a raw string to avoid issues with backslashes
        python = ''
          . .venv/bin/activate
          pip install -r MCP-Server/requirements.txt
        '';
      };
    };
    
    # Previews configuration
    previews = [
      {
        command = [
          ". .venv/bin/activate && python3 -m uvicorn MCP-Server.main:app --host 0.0.0.0 --port 8000"
        ];
        manager = "web";
        id = "mcp-server";
        name = "MCP Server";
      }
    ];
  };
}
