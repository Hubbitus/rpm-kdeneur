# Review request: https://bugzilla.redhat.com/show_bug.cgi?id=kdeneur

Summary:       KDE frontend for X Neural Switcher (xneur)
Summary(ru):   KDE интерфейс для X Neural Switcher (xneur)
Name:          kdeneur
Version:       0.20.0
Release:       1%{?dist}

Group:         User Interface/Desktops
License:       GPLv2+
URL:           http://www.xneur.ru
# Unfortunately there no traditional TAGs in repository, and I can't use recommended way to provide URL, link from official site:
Source:        https://github.com/AndrewCrewKuznetsov/xneur-devel/blob/master/dists/%{version}/kdeneur_%{version}.orig.tar.gz?raw=true#/kdeneur_%{version}.orig.tar.gz
Source1:       kdeneur.desktop

BuildRequires: desktop-file-utils, pcre-devel, qt5-qtbase-devel, kdelibs-devel
BuildRequires: xneur-devel = %{version}
BuildRequires: libtool

# Require explicit full versione because not only labriry used. This is only GUI to xneur config daemon and relies on
# concrete xneur futures, including concrete revision fixes if that SCM build.
Requires:      xneur = %{version}

%description
KDE front-end for X Neural Switcher (xneur).

%description -l ru
KDE интерфейс для Интеллектуального переключателя клавиатурных раскладок (xneur)

%prep
%autosetup

%build
%configure
make %{?_smp_mflags} CXXFLAGS=" -I%{_kde4_includedir}/ -L%{_kde4_libdir}/kde4/devel/ -lkdecore %{optflags}"

%install
make DESTDIR=%{buildroot} install

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE1}

%find_lang %{name} --with-qt --with-kde

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS ABOUT-NLS COPYING ChangeLog
%{_bindir}/%{name}
%{_datadir}/%{name}
# To do not list files twice it must be listed by find_lang helper
%exclude %{_datadir}/%{name}/i18n/*.qm
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*

%changelog
* Sat Nov 11 2017 Pavel Alexeev <Pahan@Hubbitus.info> - 0.20.0-1
- Update to version 0.20.0
- Upstream project moved to github
- Step to use %%autosetup

* Mon Oct 10 2016 Pavel Alexeev <Pahan@Hubbitus.info> - 0.19.0-1
- Update to version 0.19.0.

* Sat Oct 25 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 0.17.0-2
- Require versioned xneur but without release part to do not account any rebuilds.

* Mon Dec 2 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 0.17.0-1
- Initial attempt package new frontend for xneur
