# Note that this is NOT a relocatable package
%define ver      1.0.6
%define rel      1
%define prefix   /usr

Summary:   Alizarin Tetris
Name:      atris
Version:   %ver
Release:   %rel
Copyright: GPL
Group:     Amusements/Games
Source:    http://www.cs.berkeley.edu/~weimer/atris/atris-%{PACKAGE_VERSION}.tar.gz
#Source0:   atris-%{PACKAGE_VERSION}.tar.gz
URL:       http://www.cs.berkeley.edu/~weimer/atris/
BuildRoot: /tmp/atris-%{PACKAGE_VERSION}-root
Packager:  Wes Weimer <weimer@cs.berkeley.edu>
Icon:      icon.xpm

%description
Alizarin Tetris is a tetris clone with a twist: tiles with similar colors 
merge together. Multiple sound effects, graphic styles, piece styles
(including the planar pentominoes) and play styles are included. Play
by yourself, with a friend, across the network or against the AI. 
Written by Kiri Wagstaff and Wes Weimer <weimer@cs.berkeley.edu>

%prep

%setup

%build
# Needed for snapshot releases.
if [ ! -f configure ]; then
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=%prefix
else
  CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%prefix
fi

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make
else
  make
fi

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{prefix} install

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Add desktop menu bar items
function Add_DeskTop_MenuItem
{
    desktop=$1; deskfile=$2
    if [ -d "$desktop" ]; then
        desktop="$desktop/Games"
        if [ ! -d "$desktop" ]; then
            mkdir "$desktop" 2>/dev/null
        fi
        if [ -w "$desktop" ]; then
            echo "Creating $desktop/$deskfile"
            cat >"$desktop/$deskfile" <<__EOF__
# KDE Config File
[KDE Desktop Entry]
Name=Atris
Comment=Alizarin Tetris
Exec=/usr/bin/atris
Icon=/usr/games/atris/icon.xpm
Terminal=0
Type=Application
__EOF__
        fi
    fi
}
echo "============================================================="
echo "Adding desktop menu items ..."
for gnomedir in "/opt/gnome" "/usr/share/gnome" "$HOME/.gnome"
do Add_DeskTop_MenuItem "$gnomedir/apps" "atris.desktop"
done
for kdedir in "/opt/kde" "/usr/share/kde" "$HOME/.kde"
do Add_DeskTop_MenuItem "$kdedir/share/applnk" "atris.kdelnk"
done

%postun
echo "============================================================="
echo "Removing desktop menu items ..."
for gnomedir in "/opt/gnome" "/usr/share/gnome" "$HOME/.gnome"
do rm -f "$gnomedir/apps/Games/atris.desktop"
done
for kdedir in "/opt/kde" "/usr/share/kde" "$HOME/.kde"
do rm -f "$kdedir/share/applnk/Games/atris.kdelnk"
done

%files
%defattr(-, root, root)
%doc COPYING* CREDITS README* AUTHORS* NEWS ChangeLog Docs
%{prefix}/bin/atris
%{prefix}/games/atris

%changelog
* Sat Oct 28 2000 Wes Weimer <weimer@cs.berkeley.edu>

- first attempt at a spec file

