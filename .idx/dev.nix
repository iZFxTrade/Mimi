{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Packages to be installed
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
  ];

  # Environment variables
  env = { };

  idx = {
    # Extensions for the IDE
    extensions = [
      "ms-python.python"
    ];

    # Enable previews and define the web server
    previews = {
      enable = true;
      command = [ "python3" "-m" "uvicorn" "MCP-Server.main:app" "--host" "0.0.0.0" "--port" "$PORT" ];
      manager = "web";
    };

    # Workspace lifecycle hooks
    workspace = {
      onCreate = {
        "install-deps" = "python3 -m pip install --user -r MCP-Server/requirements.txt";
      };
      onStart = { };
    };
  };
}
