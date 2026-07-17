# README.md

## Forçar parada

```bash
loginctl list-sessions
loginctl terminate-session #
```

## Deligar tela sem bloquera PC

```bash
gsettings set org.gnome.desktop.session idle-delay 300
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver ubuntu-lock-on-suspend false
gsettings set org.gnome.desktop.screensaver lock-delay 0
```

### Verificar se Funcionou

```bash
gsettings get org.gnome.desktop.session idle-delay
gsettings get org.gnome.desktop.screensaver lock-enabled
gsettings get org.gnome.desktop.screensaver lock-delay
```

## [Remote Constrol Config](https://www.youtube.com/watch?v=l6oq5IuUEts)

### Se ainda não tiver instalado
```bash
wget https://dl.google.com/linux/direct/ch...
```

### Passo 1
```bash
sudo apt install ./chrome-remote-desktop_current_amd64.deb
sudo apt --fix-broken install
```

### Abrir o site e pegar o comando do LINUX
[remotedesktop.google.com/headless](remotedesktop.google.com/headless)

### Passo 2
```bash
ls /usr/share/xsessions/
echo "exec /etc/X11/Xsession /usr/bin/gnome-session" - ~/.chrome-remote-desktop-session
sudo systemctl restart chrome-remote-desktop@$USER
sudo apt install xfce4 desktop-base dbus-x11 xscreensaver
echo "exec /etc/X11/Xsession /usr/bin/xfce4-session" - ~/.chrome-remote-desktop-session
sudo systemctl Reinicie o chrome-remote-desktop@$USER
```

### Fé



