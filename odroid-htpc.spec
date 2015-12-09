Name:           odroid-htpc
Version:        0.2.0
Release:        1%{?dist}
Summary:        Configures an ODROID to act as an HTPC using KODI

Group:          Applications/Multimedia
License:        BSD
URL:            http://hardkernel.com
Source0:        kodi.service
Source1:        htpc.target
Source2:        kodi_shutdown.pkla

BuildArch:      noarch

BuildRequires:  systemd
Requires:       kodi
Requires:       xorg-x11-xinit
Requires:       dbus-x11
Requires(pre):  shadow-utils
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

%pre
getent group kodi >/dev/null || groupadd -r kodi
getent passwd kodi >/dev/null || \
    useradd -g kodi \
    -c "Kodi Media Center Standalone User" kodi
gpasswd -a kodi audio >/dev/null
gpasswd -a kodi video >/dev/null

%post
%systemd_post kodi.service

%preun
%systemd_preun kodi.service

%postun
%systemd_postun_with_restart kodi.service

%files
%{_unitdir}/kodi.service
%{_unitdir}/htpc.target
%config(noreplace) %attr(0640, root, polkitd) %{_sysconfdir}/polkit-1/localauthority/50-local.d/kodi_shutdown.pkla

%changelog
* Tue Dec 08 2015 Scott K Logan <logans@cottsay.net> - 0.2.0-1
- Remove xinit shenanigans

* Sun Dec 06 2015 Scott K Logan <logans@cottsay.net> - 0.1.0-1
- Initial package
