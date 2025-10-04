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

    # Workspace lifecycle hooks
    workspace = {
      # Run on workspace creation
      onCreate = {
        "install-python-deps" = "python3 -m pip install --user -r MCP-Server/requirements.txt";
      };
    };
  };
}
