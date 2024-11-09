{
  inputs = {
    nixpkgs.url      = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url  = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python312
            python312Packages.python-lsp-server
            python312Packages.flask
            python312Packages.mechanicalsoup
            python312Packages.selenium

            chromedriver
            chromium

            nodePackages.create-react-app
            nodejs
            yarn
          ];
        };
      }
    );
}

