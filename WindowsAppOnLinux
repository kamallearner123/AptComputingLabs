1) Install Wine:
https://www.youtube.com/watch?v=yCxBUy7S4Ks
https://gitlab.winehq.org/wine/wine/-/wikis/Debian-Ubuntu

  If your system is 64 bit, enable 32 bit architecture:
  
  - sudo dpkg --add-architecture i386
  
  Make a note of your distribution name:
  Look for the line with either UBUNTU_CODENAME or VERSION_CODENAME. If both are present, use the name after UBUNTU_CODENAME.
  
  - cat /etc/os-release
  
  Add the repository
  
  
  Download and add the repository key:
  
  - sudo mkdir -pm755 /etc/apt/keyrings
  - sudo wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key

  jammyUbuntu 22.04Linux Mint 21.x
  
  - sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources

  - sudo apt update

  Stable branch
  - sudo apt install --install-recommends winehq-stable
 
  
  Development branch
  sudo apt install --install-recommends winehq-devel 
  
  Staging branch
  sudo apt install --install-recommends winehq-staging

2) Install MS-365-Electron fron Ubuntu Application Manager
