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
  };
}
