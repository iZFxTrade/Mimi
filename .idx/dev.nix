{ pkgs, ... }: {
  # Which nixpkgs channel to use. Using unstable for more recent packages.
  channel = "unstable";

  # Packages to be installed in the environment.
  packages = [
    # Python environment for the MCP-Server backend
    pkgs.python311
    pkgs.python311Packages.pip

    # ESP-IDF toolchain for the firmware
    pkgs."esp-idf"
    pkgs.esptool
    pkgs.cmake
    pkgs.ninja
    pkgs."dfu-util"
    pkgs.gcc
  ];

  # Environment variables
  env = { };

  idx = {
    # Recommended extensions for this project
    extensions = [
      "ms-python.python"
      "espressif.esp-idf-extension"
    ];

    # Web preview for the MCP-Server
    previews = {
      enable = true;
      command = [ "python3" "-m" "uvicorn" "MCP-Server.main:app" "--host" "0.0.0.0" "--port" "$PORT" ];
      manager = "web";
    };

    # Workspace lifecycle hooks
    workspace = {
      # Run on workspace creation
      onCreate = {
        "install-python-deps" = "python3 -m pip install --user -r MCP-Server/requirements.txt";
      };

      # Run on workspace start
      onStart = {
        # Source the ESP-IDF export script to configure the environment for firmware development
        "source-esp-idf" = ". $ESP_IDF/export.sh";
      };
    };
  };
}
