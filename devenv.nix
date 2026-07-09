{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:
{
  # --- 1. Global Base Configuration ---
  # Variables and settings that apply absolutely everywhere (Dev & Prod)
  env = {
    GREET = "devenv";
  };

  dotenv.enable = true;

  packages = with pkgs; [
    docker
    podman
    docker-buildx
  ];

  imports = [
    ./devenv # Loads ./devenv/default.nix
  ];

  scripts.hello.exec = ''
    echo hello from $GREET
  '';

  # --- 2. Profile Definitions ---
  profiles = {
    # Development Environment Profile
    dev.module = { config, ... }: {
      env = {
        UV_SYSTEM_PYTHON = "0";
        OCO_AI_PROVIDER = "ollama";
        OCO_PROMPT_MODULE = "conventional-commit";
        OCO_MODEL = "qwen2.5-coder:3b";
        DOCKER_HOST = "tcp://docker-in-docker:2375";
      };

      packages = with pkgs; [
        git
        git-cliff
        opencommit
        jupyter
        podman
        nixpkgs-fmt
        docker
        docker-buildx
      ];

      enterShell = ''
        hello
        git --version
        export OCO_API_CUSTOM_HEADERS="{\"Authorization\": \"Bearer $OLLAMA_API_KEY\"}"
      '';

      enterTest = ''
        echo "Running tests"
        git --version | grep --color=auto "${pkgs.git.version}"
      '';
    };

    # Container / Production Environment Profile
    container-build.module = {
      env = {
        UV_SYSTEM_PYTHON = "1";
        NODE_ENV = "production";
        DOCKER_HOST = "tcp://docker-in-docker:2375";
        # Add any other production-specific environment variables here
      };

      packages = with pkgs; [
        docker
        podman
        docker-buildx
      ];

      languages.python.uv.sync.enable = false;
      languages.python.lsp.enable = false;
    };
  };
}
