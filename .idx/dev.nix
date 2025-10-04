{ pkgs, ... }: {
  # Which nixpkgs channel to use. Using unstable for more recent packages.
  channel = "unstable";

  # Packages to be installed in the environment.
  packages = [
    # Python environment for the MCP-Server backend
    pkgs.python3
  ];

  # Environment variables
  env = { };

  idx = {
    # Recommended extensions for this project
    extensions = [
      "ms-python.python"
    ];

    # Web preview for the MCP-Server
    previews = {
      main = {
        enable = true;
        command = [ "python3" "-m" "uvicorn" "MCP-Server.main:app" "--host" "0.0.0.0" "--port" "$PORT" ];
        manager = "web";
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Run on workspace creation
      onCreate = {
        "install-python-deps" = "python3 -m pip install --user -r MCP-Server/requirements.txt";
      };
    };
  };
}
