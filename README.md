# docker-tools
My Docker tools

For now just one tool, names "bootstrap-docker.py".

## Requirements

Besides Python 2.x, you will need "simplejson" module.

## bootstrap-docker.py

A tool is very primitive.  In the future, I will normalize sys.argv part.

Presently, it works just with debootstrap, meaning that you can relatively
easily to upgrade it for all Debian-based distributions. However, at the
moment, the script as-is supports just Debian jessie, testing, unstable and
experimental. In the future I'll add support for RPM-based distributions.

If you find this micro-tool useful and want to contribute or comment, please
let me know: millosh@gmail.com.

### Arguments

    --bootstrap-release. Conditionally optional. If the varialbe has been
      defined inside of the "distros config", then you do not need to use
      it.  Otherwise you have to define it.  The initial usage was for
      Debian experimental, which is Debian unstable with experimenal
      repository and thus requires "unstable" here.  However, it could be
      useful if you want to create your own non-default additions into the
      filesystem.

      In other words, it's useful for grouping types of Docker
      containers. "This is Apache docker container and it requres Apache
      /etc structure." -- and similar. In that case, you will say that the
      variable --release is not "jessie" or "testing", but, for example,
      "apache2.4", create the filesystem structure inside of
      system/debian/apache2.4, while you will define --bootstrap-release as
      "jessie" or "testing".

    --distro: Mandatory.  Distribution.  It works just with Debian-based
      distributions.  As debootstrap doesn't use this, you could use
      whichever string you want.

    --distros-config: Optional.  Two arguments inside of the JSON file which
      define Docker repository and "bootstrap release" (see
      --bootstrap-release).  You have the example inside of the file
      "distros.json". Will be used for more variables in the future. If you
      do not define it, arguments --docker-repository and
      --bootstrap-release will be mandatory.

    --docker-repository: Conditionally optional. If the variable has been
      defined inside of the "distros config", then you do not need to use
      it. If you are not uploading the docker container into the repository, 
      this variable is mandatory, but it could be an arbitrary string.
      Defines docker repository where you want to upload your image.

    --full-init: Optional.  If you are fine with program not doing anything;
      otherwise conditionally optional: one of the following commands should
      be invoked: --full-init, --init, --full-update, --update.

      This options is doing the following: system_install (debootstrap
      installation in chroot), config_update (minimal config update,
      including copying the files from system/<distribution>/<release>/
      path), update_software (apt-get update, aptget-upgrade -y),
      install_software (install additional software; at the moment, the
      script itself is defining installation of vim-nox, tcpdump, nmap,
      net-tools; in the future, a separate configuration file will be used
      for that), create_docker_image (imports the content of particular
      chroot directory into docker image), push_to_cloud (pushing docker to
      docker repository), run_docker (run docker image).

    --full-update: Optional.  If you are fine with program not doing
      anything; otherwise conditionally optional: one of the following
      commands should be invoked: --full-init, --init, --full-update,
      --update.

      This options is doing the following: update_software (apt-get update,
      aptget-upgrade -y), create_docker_image (imports the content of
      particular chroot directory into docker image), push_to_cloud (pushing
      docker to docker repository).

    --init: Optional.  If you are fine with program not doing anything;
      otherwise conditionally optional: one of the following commands should
      be invoked: --full-init, --init, --full-update, --update.

      This options is doing the following: system_install (debootstrap
      installation in chroot), config_update (minimal config update,
      including copying the files from system/<distribution>/<release>/
      path), update_software (apt-get update, aptget-upgrade -y),
      install_software (install additional software; at the moment, the
      script itself is defining installation of vim-nox, tcpdump, nmap,
      net-tools; in the future, a separate configuration file will be used
      for that), create_docker_image (imports the content of particular
      chroot directory into docker image), run_docker (run docker image).

    --noexec: Optional.  Dry run.  Default is to execute the commands.

    --noprint: Optional.  Do not print the commands.  Default is to print
      the commands.

    --root: Optional. Root dir, where you can find "system" directory and where
      "chroots" directory will be created.  If not defined, will be current
      directory.

    --release: Mandatory. Distribution release, like "jessie", "testing". It
      will be sent to debootstrap, so everything what debootstrap support,
      this program supports, as well (Ubuntu, Mint etc.  releases).

    --tag: Optional.  Will tag docker image and docker container.  If not
      defined, it will be "default".

    --update: Optional.  If you are fine with program not doing anything;
      otherwise conditionally optional: one of the following commands should
      be invoked: --full-init, --init, --full-update, --update.

      This options is doing the following: update_software (apt-get update,
      aptget-upgrade -y), create_docker_image (imports the content of
      particular chroot directory into docker image).

### Approach

This tool creates and updates chroot'd Debian installation and imports it
into the Docker image.  The main reason for this approach is to make as less
images layers as it's possible.

I suggest the following approach:
* Initialize the container and push it into the repository (--full-init).
* Update chroot periodically and push into the repository (--full-update).
