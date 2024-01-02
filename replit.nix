{ pkgs }: {
  deps = [
    pkgs.systemdStage1Network
    pkgs.docker
  ];
}