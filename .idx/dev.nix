{ pkgs, ... }: {
  # Which nixpkgs channel to use. Using unstable for more recent packages.
  channel = "unstable";

  # Packages to be installed in the environment.
  packages = [
    # Create a Python 3.11 environment
    pkgs.python311
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
      # The onCreate hook is no longer needed as Nix now manages the packages directly.
    };
  };
}
