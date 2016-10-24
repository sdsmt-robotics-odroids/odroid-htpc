Name:           odroid-htpc
Version:        0.2.3
Release:        1%{?dist}
Summary:        Configures an ODROID to act as an HTPC using Kodi

Group:          Applications/Multimedia
License:        BSD
URL:            http://hardkernel.com
Source0:        kodi.service
Source1:        htpc.target
Source2:        kodi_shutdown.pkla
Source3:        kodi.xml
Source4:        htpc.xml

BuildArch:      noarch

BuildRequires:  systemd
Requires:       dbus-x11
Requires:       firewalld-filesystem
Requires:       kodi
Requires:       xorg-x11-xinit
Requires(pre):  shadow-utils
Requires(post): firewalld-filesystem
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This package installs various configurations needed for an ODROID to act as
an HTPC. After enabling the kodi service and defaulting to the htpc target,
the system will automatically start Kodi on boot.

Use this command to enable the service:
systemctl enable kodi

Use this commands to default to htpc:
ln -sf /usr/lib/systemd/system/htpc.target /etc/systemd/system/default.target

%prep
%build

%install
install -p -m0644 -D %{SOURCE0} %{buildroot}%{_unitdir}/kodi.service
install -p -m0644 -D %{SOURCE1} %{buildroot}%{_unitdir}/htpc.target
install -p -m0640 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/kodi_shutdown.pkla
install -p -m0644 -D %{SOURCE3} %{buildroot}%{_prefix}/lib/firewalld/services/kodi.xml
install -p -m0644 -D %{SOURCE4} %{buildroot}%{_prefix}/lib/firewalld/zones/htpc.xml

%pre
getent group kodi >/dev/null || groupadd -r kodi
getent passwd kodi >/dev/null || \
    useradd -g kodi \
    -c "Kodi Media Center Standalone User" kodi
gpasswd -a kodi audio >/dev/null
gpasswd -a kodi video >/dev/null

%post
%firewalld_reload
%systemd_post kodi.service

%preun
%systemd_preun kodi.service

%postun
%systemd_postun_with_restart kodi.service

%files
%{_unitdir}/kodi.service
%{_unitdir}/htpc.target
%config(noreplace) %attr(0640, root, polkitd) %{_sysconfdir}/polkit-1/localauthority/50-local.d/kodi_shutdown.pkla
%{_prefix}/lib/firewalld/services/kodi.xml
%{_prefix}/lib/firewalld/zones/htpc.xml

%changelog
* Sun Oct 23 2016 Scott K Logan <logans@cottsay.net> - 0.2.3-1
- Add firewalld service and zone

* Sun Dec 27 2015 Scott K Logan <logans@cottsay.net> - 0.2.2-1
- Switch away from tty1 because it disables shutdown/reboot buttons

* Sat Dec 12 2015 Scott K Logan <logans@cottsay.net> - 0.2.1-1
- Update kodi.service to use tty1

* Tue Dec 08 2015 Scott K Logan <logans@cottsay.net> - 0.2.0-1
- Remove xinit shenanigans

* Sun Dec 06 2015 Scott K Logan <logans@cottsay.net> - 0.1.0-1
- Initial package
